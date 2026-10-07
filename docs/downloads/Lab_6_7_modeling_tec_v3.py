"""Consistent one- and two-lump TEC control simulation for Module 6.

The program uses the same dimensional variables and controller definitions as
``Lab_6_pi_contribution_rolling_demo.py``.

One-lump process:

    C*dT/dt = P_u(u)*u - H*(T - T_amb),    C = C_T + C_m

Two-lump process:

    C_T*dT/dt   = P_u(u)*u - G*(T - T_m)
    C_m*dT_m/dt = G*(T - T_m) - H*(T_m - T_amb)

The controller always uses the measured temperature: T for the one-lump model
and T_m for the two-lump model.

The TEC coefficient is piecewise: P_u = P_u,h for heating and P_u = P_u,c for
cooling.  Their ratio r = P_u,h/P_u,c = chi_h/chi_c defaults to 2.

    open loop: u = u_user
    P:         u = Kp*e
    PI:        u = Kp*e + Ki*integral(e dt)
    e = T_set - T_measured

Run the desktop GUI from the Phys39F26 repository root:

    .venv/bin/python python/Lab_6_7_modeling_tec_v3.py

Run a non-interactive two-lump demonstration and save a PNG:

    .venv/bin/python python/Lab_6_7_modeling_tec_v3.py --demo

No Arduino is needed. This is a mathematical model, not a hardware controller.
"""

from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass, replace
import io
import math
import os
from pathlib import Path
import tempfile
import tkinter as tk
from tkinter import messagebox, ttk


UPDATE_INTERVAL_MS = 50
MAX_TEC_VOLTAGE_V = 10.0


@dataclass(frozen=True)
class ModelConfig:
    """Physical, controller, display, and numerical parameters with units."""

    ambient_c: float = 22.0
    initial_c: float = 22.0
    setpoint_c: float = 30.0
    total_capacitance_j_per_c: float = 90.93492469451549
    tec_capacitance_fraction: float = 0.35
    coupling_w_per_c: float = 2.0
    heat_loss_w_per_c: float = 1.1366865586814436
    tec_power_w_per_pwm: float = 0.261437908496732
    heating_to_cooling_ratio: float = 2.0
    measured_cooling_chi_c_per_pwm: float = 0.23
    measured_heating_chi_c_per_pwm: float = 0.46
    measured_tau_s: float = 80.0
    tec_voltage_v: float = 10.0
    tec_resistance_ohm: float = 1.50
    open_loop_pwm: float = 100.0
    kp_pwm_per_c: float = 18.0
    ki_pwm_per_c_s: float = 0.08
    pwm_limit: float = 255.0
    dt_s: float = 0.05
    window_s: float = 180.0
    simulation_speed: float = 10.0
    anti_windup: bool = True

    @property
    def one_lump_capacitance_j_per_c(self) -> float:
        return self.total_capacitance_j_per_c

    @property
    def tec_capacitance_j_per_c(self) -> float:
        return self.tec_capacitance_fraction * self.total_capacitance_j_per_c

    @property
    def measured_capacitance_j_per_c(self) -> float:
        return (1.0 - self.tec_capacitance_fraction) * self.total_capacitance_j_per_c


@dataclass(frozen=True)
class DerivedConstants:
    """One-lump constants inferred from measured susceptibility and time scale."""

    total_capacitance_j_per_c: float
    heat_loss_w_per_c: float
    cooling_power_w_per_pwm: float
    heating_to_cooling_ratio: float


def constants_from_measurements(
    cooling_chi_c_per_pwm: float,
    heating_chi_c_per_pwm: float,
    tau_s: float,
    tec_voltage_v: float,
    tec_resistance_ohm: float,
    full_scale_pwm: float = 255.0,
) -> DerivedConstants:
    """Infer C, H, P_u,c, and r using the simplified TEC heat balance.

    The voltage is the on-state voltage across the TEC. Joule heating at the
    object face is V^2/(2R). Heating/cooling asymmetry separates that term
    from the reversible Peltier term.
    """

    if cooling_chi_c_per_pwm <= 0.0:
        raise ValueError("Measured cooling susceptibility chi_c must be positive.")
    if heating_chi_c_per_pwm <= cooling_chi_c_per_pwm:
        raise ValueError(
            "Measured heating susceptibility chi_h must be greater than chi_c "
            "for this simplified TEC inversion."
        )
    if tau_s <= 0.0:
        raise ValueError("Measured time constant tau must be positive.")
    if not 0.0 < tec_voltage_v <= MAX_TEC_VOLTAGE_V:
        raise ValueError(f"TEC voltage must be between 0 and {MAX_TEC_VOLTAGE_V:g} V.")
    if tec_resistance_ohm <= 0.0:
        raise ValueError("TEC resistance must be positive.")

    ratio = heating_chi_c_per_pwm / cooling_chi_c_per_pwm
    joule_power_w = tec_voltage_v**2 / (2.0 * tec_resistance_ohm)
    peltier_power_w = joule_power_w * (ratio + 1.0) / (ratio - 1.0)
    cooling_power_w = peltier_power_w - joule_power_w
    cooling_power_w_per_pwm = cooling_power_w / full_scale_pwm
    heat_loss_w_per_c = cooling_power_w_per_pwm / cooling_chi_c_per_pwm
    total_capacitance_j_per_c = heat_loss_w_per_c * tau_s
    return DerivedConstants(
        total_capacitance_j_per_c=total_capacitance_j_per_c,
        heat_loss_w_per_c=heat_loss_w_per_c,
        cooling_power_w_per_pwm=cooling_power_w_per_pwm,
        heating_to_cooling_ratio=ratio,
    )


@dataclass
class ModelState:
    """Temperatures and controller memory at the current model time."""

    time_s: float
    tec_temperature_c: float
    measured_temperature_c: float
    integral_error_c_s: float = 0.0


@dataclass(frozen=True)
class StepResult:
    """Values produced by one forward-Euler update."""

    time_s: float
    tec_temperature_c: float
    measured_temperature_c: float
    error_c: float
    p_pwm: float
    i_pwm: float
    applied_pwm: float
    saturated: bool


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def measured_temperature(state: ModelState, process_mode: str) -> float:
    if process_mode == "one_lump":
        return state.tec_temperature_c
    if process_mode == "two_lump":
        return state.measured_temperature_c
    raise ValueError("process_mode must be 'one_lump' or 'two_lump'")


def controller_command(
    state: ModelState,
    config: ModelConfig,
    process_mode: str,
    controller_mode: str,
    advance_integral: bool = True,
) -> tuple[float, float, float, float, bool]:
    """Return error, P term, I term, applied command, and saturation state."""

    error = controller_target_temperature(
        config, controller_mode
    ) - measured_temperature(state, process_mode)

    if controller_mode == "open_loop":
        raw_command = config.open_loop_pwm
        p_term = 0.0
        i_term = 0.0
    elif controller_mode in {"p", "pi"}:
        p_term = config.kp_pwm_per_c * error
        if controller_mode == "pi":
            if advance_integral:
                proposed_integral = state.integral_error_c_s + error * config.dt_s
                proposed_i = config.ki_pwm_per_c_s * proposed_integral
                proposed_command = p_term + proposed_i
                drives_farther_into_saturation = (
                    proposed_command > config.pwm_limit and error > 0.0
                ) or (
                    proposed_command < -config.pwm_limit and error < 0.0
                )
                if not (config.anti_windup and drives_farther_into_saturation):
                    state.integral_error_c_s = proposed_integral
            i_term = config.ki_pwm_per_c_s * state.integral_error_c_s
        else:
            state.integral_error_c_s = 0.0
            i_term = 0.0
        raw_command = p_term + i_term
    else:
        raise ValueError("controller_mode must be 'open_loop', 'p', or 'pi'")

    applied = clamp(raw_command, -config.pwm_limit, config.pwm_limit)
    return error, p_term, i_term, applied, not math.isclose(raw_command, applied)


def advance_model(
    state: ModelState,
    config: ModelConfig,
    process_mode: str,
    controller_mode: str,
) -> StepResult:
    """Advance the selected dimensional thermal model by one Euler step."""

    error, p_term, i_term, command, saturated = controller_command(
        state, config, process_mode, controller_mode
    )
    tec_power_w = active_tec_coefficient(config, command) * command

    if process_mode == "one_lump":
        capacitance = config.one_lump_capacitance_j_per_c
        heat_loss_w = config.heat_loss_w_per_c * (
            state.tec_temperature_c - config.ambient_c
        )
        dtemperature_dt = (tec_power_w - heat_loss_w) / capacitance
        next_temperature = state.tec_temperature_c + config.dt_s * dtemperature_dt
        state.tec_temperature_c = next_temperature
        state.measured_temperature_c = next_temperature
    else:
        coupling_w = config.coupling_w_per_c * (
            state.tec_temperature_c - state.measured_temperature_c
        )
        measured_heat_loss_w = config.heat_loss_w_per_c * (
            state.measured_temperature_c - config.ambient_c
        )
        dtec_dt = (
            tec_power_w - coupling_w
        ) / config.tec_capacitance_j_per_c
        dmeasured_dt = (
            coupling_w - measured_heat_loss_w
        ) / config.measured_capacitance_j_per_c
        state.tec_temperature_c += config.dt_s * dtec_dt
        state.measured_temperature_c += config.dt_s * dmeasured_dt

    state.time_s += config.dt_s
    return StepResult(
        time_s=state.time_s,
        tec_temperature_c=state.tec_temperature_c,
        measured_temperature_c=state.measured_temperature_c,
        error_c=controller_target_temperature(
            config, controller_mode
        ) - measured_temperature(state, process_mode),
        p_pwm=p_term,
        i_pwm=i_term,
        applied_pwm=command,
        saturated=saturated,
    )


def cooling_tec_coefficient(config: ModelConfig) -> float:
    return config.tec_power_w_per_pwm


def heating_tec_coefficient(config: ModelConfig) -> float:
    return config.heating_to_cooling_ratio * cooling_tec_coefficient(config)


def active_tec_coefficient(config: ModelConfig, command: float) -> float:
    if command >= 0.0:
        return heating_tec_coefficient(config)
    return cooling_tec_coefficient(config)


def predicted_open_loop_steady_temperature(config: ModelConfig) -> float:
    """Return the measured steady temperature for the open-loop command."""

    return config.ambient_c + (
        active_tec_coefficient(config, config.open_loop_pwm)
        * config.open_loop_pwm
        / config.heat_loss_w_per_c
    )


def controller_target_temperature(config: ModelConfig, controller_mode: str) -> float:
    """Return the temperature reference used for display and error."""

    if controller_mode == "open_loop":
        return predicted_open_loop_steady_temperature(config)
    return config.setpoint_c


def cooling_susceptibility(config: ModelConfig) -> float:
    return cooling_tec_coefficient(config) / config.heat_loss_w_per_c


def heating_susceptibility(config: ModelConfig) -> float:
    return heating_tec_coefficient(config) / config.heat_loss_w_per_c


def open_loop_susceptibility(config: ModelConfig) -> float:
    """Return the susceptibility for the selected setpoint direction."""

    if config.setpoint_c >= config.ambient_c:
        return heating_susceptibility(config)
    return cooling_susceptibility(config)


def one_lump_time_constant(config: ModelConfig) -> float:
    return config.one_lump_capacitance_j_per_c / config.heat_loss_w_per_c


def two_lump_time_constants(config: ModelConfig) -> tuple[float, float]:
    """Return the fast and slow passive decay times of the two-lump model."""

    rate_sum = (
        config.coupling_w_per_c / config.tec_capacitance_j_per_c
        + (config.coupling_w_per_c + config.heat_loss_w_per_c)
        / config.measured_capacitance_j_per_c
    )
    rate_product = (
        config.coupling_w_per_c
        * config.heat_loss_w_per_c
        / (
            config.tec_capacitance_j_per_c
            * config.measured_capacitance_j_per_c
        )
    )
    discriminant = max(0.0, rate_sum**2 - 4.0 * rate_product)
    fast_rate = 0.5 * (rate_sum + math.sqrt(discriminant))
    slow_rate = 0.5 * (rate_sum - math.sqrt(discriminant))
    return 1.0 / fast_rate, 1.0 / slow_rate


def predicted_p_droop(config: ModelConfig) -> float:
    loop_gain = open_loop_susceptibility(config) * config.kp_pwm_per_c
    return (config.setpoint_c - config.ambient_c) / (1.0 + loop_gain)


def predicted_p_time_constant(config: ModelConfig) -> float:
    tec_coefficient = (
        heating_tec_coefficient(config)
        if config.setpoint_c >= config.ambient_c
        else cooling_tec_coefficient(config)
    )
    return config.one_lump_capacitance_j_per_c / (
        config.heat_loss_w_per_c + tec_coefficient * config.kp_pwm_per_c
    )


def one_lump_pi_damping_ratio(config: ModelConfig) -> float:
    tec_coefficient = (
        heating_tec_coefficient(config)
        if config.setpoint_c >= config.ambient_c
        else cooling_tec_coefficient(config)
    )
    denominator = 2.0 * math.sqrt(
        config.one_lump_capacitance_j_per_c
        * tec_coefficient
        * config.ki_pwm_per_c_s
    )
    if denominator == 0.0:
        return math.inf
    return (
        config.heat_loss_w_per_c
        + tec_coefficient * config.kp_pwm_per_c
    ) / denominator


def damping_description(value: float) -> str:
    if math.isinf(value):
        return "no integral action"
    if value < 1.0 - 1e-9:
        return "underdamped"
    if value > 1.0 + 1e-9:
        return "overdamped"
    return "critically damped"


def validate_config(config: ModelConfig) -> None:
    positive = {
        "total capacitance C": config.total_capacitance_j_per_c,
        "coupling G": config.coupling_w_per_c,
        "heat-loss conductance H": config.heat_loss_w_per_c,
        "PWM limit": config.pwm_limit,
        "Euler time step": config.dt_s,
        "rolling window": config.window_s,
        "simulation speed": config.simulation_speed,
    }
    for label, value in positive.items():
        if value <= 0.0:
            raise ValueError(f"{label} must be positive.")
    if not 0.0 < config.tec_capacitance_fraction < 1.0:
        raise ValueError("The TEC capacitance fraction C_T/C must be between 0 and 1.")
    if config.tec_power_w_per_pwm < 0.0:
        raise ValueError("TEC coefficient P_u cannot be negative.")
    if config.heating_to_cooling_ratio <= 0.0:
        raise ValueError("Heating/cooling susceptibility ratio r must be positive.")
    if config.kp_pwm_per_c < 0.0 or config.ki_pwm_per_c_s < 0.0:
        raise ValueError("Kp and Ki must be zero or positive.")

    fastest_time = min(
        config.one_lump_capacitance_j_per_c / config.heat_loss_w_per_c,
        config.tec_capacitance_j_per_c / config.coupling_w_per_c,
        config.measured_capacitance_j_per_c
        / (config.coupling_w_per_c + config.heat_loss_w_per_c),
    )
    if config.dt_s > fastest_time / 5.0:
        raise ValueError("Use a time step no larger than one fifth of the fastest thermal time scale.")


def simulate(
    config: ModelConfig,
    process_mode: str,
    controller_mode: str,
    duration_s: float,
) -> list[StepResult]:
    """Return a complete simulation for tests and the non-interactive demo."""

    validate_config(config)
    state = ModelState(0.0, config.initial_c, config.initial_c)
    results: list[StepResult] = []
    while state.time_s < duration_s:
        results.append(advance_model(state, config, process_mode, controller_mode))
    return results


def run_demo(output: Path) -> None:
    """Save a reproducible two-lump PI demonstration plot."""

    os.environ.setdefault(
        "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "phys39_matplotlib_cache")
    )
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    config = ModelConfig()
    results = simulate(config, "two_lump", "pi", duration_s=600.0)
    times = [row.time_s for row in results]
    tec = [row.tec_temperature_c for row in results]
    measured = [row.measured_temperature_c for row in results]
    commands = [row.applied_pwm for row in results]
    errors = [row.error_c for row in results]

    figure, axes = plt.subplots(3, 1, figsize=(7, 9), sharex=True)
    axes[0].plot(times, tec, color="tab:red", label=r"TEC-side $T$")
    axes[0].plot(times, measured, color="tab:blue", label=r"measured $T_m$")
    axes[0].axhline(config.setpoint_c, color="black", linestyle="--", label="setpoint")
    axes[0].set_ylabel(r"temperature ($^\circ$C)")
    axes[0].legend(loc="best")
    axes[1].plot(times, commands, color="black")
    axes[1].axhline(0.0, color="gray", linewidth=0.8)
    axes[1].set_ylabel("signed PWM")
    axes[2].plot(times, errors, color="tab:green")
    axes[2].axhline(0.0, color="gray", linewidth=0.8)
    axes[2].set_ylabel(r"error ($^\circ$C)")
    axes[2].set_xlabel("time (s)")
    for axis in axes:
        axis.grid(True, alpha=0.25)

    figure.suptitle("Module 6 Part II v3: dimensional two-lump PI model")
    figure.tight_layout(rect=(0, 0, 1, 0.97))
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=160)
    print(f"Saved demo plot: {output}")
    print(
        "Final state: "
        f"T={tec[-1]:.3f} C; T_m={measured[-1]:.3f} C; "
        f"error={errors[-1]:.3f} C; u={commands[-1]:.3f} PWM"
    )


class ModelingTECv3Gui:
    """Rolling-window GUI for consistent one- and two-lump TEC models."""

    FIELD_SPECS = (
        (r"T_{\mathrm{amb}}", "Ambient temperature", "ambient_c", "°C", -10.0, 60.0, 0.5),
        (r"T_0", "Initial temperature", "initial_c", "°C", -10.0, 60.0, 0.5),
        (r"T_{\mathrm{set}}", "Setpoint", "setpoint_c", "°C", -10.0, 60.0, 0.5),
        (r"\chi_c", "Measured cooling susceptibility", "measured_cooling_chi_c_per_pwm", "°C/PWM", 0.01, 0.50, 0.005),
        (r"\chi_h", "Measured heating susceptibility", "measured_heating_chi_c_per_pwm", "°C/PWM", 0.01, 0.75, 0.005),
        (r"\tau", "Measured time constant", "measured_tau_s", "s", 5.0, 500.0, 5.0),
        (r"V_{\mathrm{TEC}}", "On-state voltage across TEC", "tec_voltage_v", "V", 0.1, MAX_TEC_VOLTAGE_V, 0.1),
        (r"R_M", "TEC module resistance", "tec_resistance_ohm", "Ω", 0.1, 5.0, 0.05),
        (r"C", "Total thermal capacitance", "total_capacitance_j_per_c", "J/K", 5.0, 500.0, 5.0),
        (r"C_T/C", "TEC capacitance fraction", "tec_capacitance_fraction", "dimensionless", 0.05, 0.95, 0.05),
        (r"G", "Thermal coupling", "coupling_w_per_c", "W/K", 0.1, 100.0, 1.0),
        (r"H", "Heat-loss conductance", "heat_loss_w_per_c", "W/K", 0.1, 10.0, 0.05),
        (r"P_{u,c}", "Cooling TEC coefficient", "tec_power_w_per_pwm", "W/PWM", 0.01, 0.5, 0.01),
        (r"r", "Heating/cooling ratio", "heating_to_cooling_ratio", "dimensionless", 0.25, 4.0, 0.05),
        (r"u_{\mathrm{user}}", "Open-loop command", "open_loop_pwm", "PWM", -255.0, 255.0, 1.0),
        (r"K_p", "Proportional gain", "kp_pwm_per_c", "PWM/°C", 0.0, 250.0, 1.0),
        (r"K_i", "Integral gain", "ki_pwm_per_c_s", "PWM/(°C s)", 0.0, 5.0, 0.02),
        (r"u_{\max}", "PWM limit", "pwm_limit", "PWM", 1.0, 255.0, 1.0),
        (r"\Delta t", "Euler time step", "dt_s", "s", 0.01, 2.0, 0.01),
        (r"t_{\mathrm{window}}", "Rolling window", "window_s", "s", 30.0, 600.0, 10.0),
        (r"s", "Simulation speed", "simulation_speed", "sim s/real s", 1.0, 50.0, 1.0),
    )

    def __init__(self, root: tk.Tk) -> None:
        os.environ.setdefault(
            "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "phys39_matplotlib_cache")
        )
        import matplotlib

        matplotlib.use("TkAgg")
        matplotlib.rcParams["mathtext.fontset"] = "stix"
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        from matplotlib.font_manager import FontProperties
        from matplotlib.mathtext import math_to_image

        self.plt = plt
        self.matplotlib = matplotlib
        self.FigureCanvasTkAgg = FigureCanvasTkAgg
        self.NavigationToolbar2Tk = NavigationToolbar2Tk
        self.FontProperties = FontProperties
        self.math_to_image = math_to_image
        self.math_symbol_images: list[tk.PhotoImage] = []
        self.live_symbol_widgets: dict[str, ttk.Label] = {}
        self.live_symbol_cache: dict[str, tk.PhotoImage] = {}
        self.root = root
        self.root.title("Module 6 Part II v3: Consistent TEC Models")
        self.root.geometry("1540x940")
        self.root.minsize(1260, 800)

        self.defaults = ModelConfig()
        self.config = self.defaults
        self.process_mode = tk.StringVar(value="one_lump")
        self.controller_mode = tk.StringVar(value="p")
        self.parameter_source = tk.StringVar(value="measured")
        self.anti_windup = tk.BooleanVar(value=self.defaults.anti_windup)
        self.mass_temperature_only = tk.BooleanVar(value=False)
        self.entries: dict[str, tk.DoubleVar] = {}
        self.field_widgets: dict[str, tuple[tk.Widget, ...]] = {}
        self.running = False
        self.syncing_derived_fields = False
        self.after_job: str | None = None

        self.live_temperature = tk.StringVar()
        self.live_p = tk.StringVar()
        self.live_i = tk.StringVar()
        self.live_error = tk.StringVar()
        self.live_command = tk.StringVar()
        self.live_susceptibility = tk.StringVar()
        self.live_time_scale = tk.StringVar()
        self.live_required_command = tk.StringVar()
        self.live_required_power = tk.StringVar()
        self.live_p_prediction = tk.StringVar()
        self.live_damping = tk.StringVar()
        self.live_status = tk.StringVar()
        self.run_button_text = tk.StringVar(value="Resume")

        self._build_layout()
        self._reset_experiment()
        for variable in self.entries.values():
            variable.trace_add("write", self._on_parameter_edit)
        self.anti_windup.trace_add("write", self._on_parameter_edit)
        self._schedule_next_tick()

    def _build_layout(self) -> None:
        outer = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        outer.pack(fill=tk.BOTH, expand=True)
        controls = ttk.Frame(outer, padding=10)
        plots = ttk.Frame(outer, padding=(4, 8, 8, 8))
        # Reserve enough horizontal space for both the sliders and their
        # exact-value entry boxes.  A zero-weight control pane collapses the
        # sliders to zero width on macOS when the plot requests extra space.
        outer.add(controls, weight=2)
        outer.add(plots, weight=3)

        ttk.Label(
            controls,
            text="Consistent one- and two-lump TEC models",
            font=("TkDefaultFont", 14, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))

        row = 1
        ttk.Label(controls, text="Physical model").grid(row=row, column=0, sticky="w")
        process_box = ttk.Combobox(
            controls,
            textvariable=self.process_mode,
            values=("one_lump", "two_lump"),
            state="readonly",
            width=15,
        )
        process_box.grid(row=row, column=1, columnspan=2, sticky="ew")
        process_box.bind("<<ComboboxSelected>>", self._change_process)
        row += 1

        self.mass_only_button = ttk.Checkbutton(
            controls,
            text="Plot measured mass T_m only",
            variable=self.mass_temperature_only,
            command=self._draw,
        )
        self.mass_only_button.grid(
            row=row, column=0, columnspan=3, sticky="w", pady=(2, 4)
        )
        row += 1

        ttk.Label(controls, text="Controller").grid(row=row, column=0, sticky="w")
        controller_box = ttk.Combobox(
            controls,
            textvariable=self.controller_mode,
            values=("open_loop", "p", "pi"),
            state="readonly",
            width=15,
        )
        controller_box.grid(row=row, column=1, columnspan=2, sticky="ew")
        controller_box.bind("<<ComboboxSelected>>", self._change_controller)
        row += 1

        ttk.Label(controls, text="Physical parameters").grid(row=row, column=0, sticky="w")
        parameter_box = ttk.Combobox(
            controls,
            textvariable=self.parameter_source,
            values=("measured", "direct constants"),
            state="readonly",
            width=15,
        )
        parameter_box.grid(row=row, column=1, columnspan=2, sticky="ew")
        parameter_box.bind("<<ComboboxSelected>>", self._change_parameter_source)
        row += 1

        for symbol, label, attribute, units, low, high, resolution in self.FIELD_SPECS:
            variable = tk.DoubleVar(value=getattr(self.defaults, attribute))
            self.entries[attribute] = variable
            label_widget = ttk.Frame(controls)
            label_widget.grid(row=row, column=0, sticky="w", pady=1)
            symbol_image = self._render_math_symbol(symbol)
            symbol_box = ttk.Frame(label_widget, width=94, height=26)
            symbol_box.grid(row=0, column=0, sticky="w")
            symbol_box.grid_propagate(False)
            symbol_widget = ttk.Label(symbol_box, image=symbol_image)
            symbol_widget.grid(row=0, column=0, sticky="w")
            description_widget = ttk.Label(label_widget, text=label)
            description_widget.grid(row=0, column=1, sticky="w")
            field = ttk.Frame(controls)
            field.grid(row=row, column=1, sticky="ew", padx=(7, 5))
            field.columnconfigure(0, weight=1)
            slider = tk.Scale(
                field,
                from_=low,
                to=high,
                resolution=resolution,
                orient=tk.HORIZONTAL,
                variable=variable,
                showvalue=False,
                highlightthickness=0,
                length=205,
            )
            slider.grid(row=0, column=0, sticky="ew")
            entry = ttk.Entry(field, textvariable=variable, width=9)
            entry.grid(row=0, column=1, padx=(5, 0))
            entry.bind("<Return>", self._apply_parameter_edit)
            entry.bind("<KP_Enter>", self._apply_parameter_edit)
            units_widget = ttk.Label(controls, text=units)
            units_widget.grid(row=row, column=2, sticky="w")
            self.field_widgets[attribute] = (
                symbol_widget,
                description_widget,
                slider,
                entry,
                units_widget,
            )
            row += 1

        ttk.Checkbutton(
            controls, text="Prevent integral windup", variable=self.anti_windup
        ).grid(row=row, column=0, columnspan=3, sticky="w", pady=(5, 5))
        row += 1

        buttons = ttk.Frame(controls)
        buttons.grid(row=row, column=0, columnspan=3, sticky="ew")
        ttk.Button(
            buttons, textvariable=self.run_button_text, command=self._toggle_running
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(buttons, text="Zero integral", command=self._zero_integral).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0)
        )
        ttk.Button(buttons, text="Reset experiment", command=self._reset_experiment).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0)
        )
        row += 1

        ttk.Separator(controls).grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=7
        )
        row += 1
        ttk.Label(
            controls,
            text="Live model and controller values",
            font=("TkDefaultFont", 14, "bold"),
        ).grid(row=row, column=0, columnspan=3, sticky="w", pady=(0, 5))
        row += 1

        live_values = ttk.Frame(controls)
        live_values.grid(row=row, column=0, columnspan=3, sticky="ew")
        left_values = (
            ("temperature", "Temperature", r"T", self.live_temperature),
            ("error", "Error", r"e", self.live_error),
            ("p", "P term", r"u_P", self.live_p),
            ("i", "I term", r"u_I", self.live_i),
            ("command", "Applied", r"u", self.live_command),
        )
        right_values = (
            (
                "susceptibility",
                "Susceptibility",
                r"\chi_c,\ \chi_h",
                self.live_susceptibility,
            ),
            (
                "time_scale",
                "Time scale",
                r"\tau_{\mathrm{OL}},\ \tau_P",
                self.live_time_scale,
            ),
            (
                "required_command",
                "Required command",
                r"u_{\mathrm{ss}}",
                self.live_required_command,
            ),
            (
                "required_power",
                "Required power",
                r"\dot Q_{\mathrm{ss}}",
                self.live_required_power,
            ),
            (
                "p_prediction",
                "Predicted P droop",
                r"\Delta T_{\mathrm{droop}}",
                self.live_p_prediction,
            ),
            ("damping", "Damping ratio", r"\zeta", self.live_damping),
        )
        for column, rows in enumerate((left_values, right_values)):
            for value_row, (key, description, symbol, variable) in enumerate(rows):
                value_frame = ttk.Frame(live_values)
                value_frame.grid(
                    row=value_row,
                    column=column,
                    sticky="w",
                    padx=(0, 12) if column == 0 else 0,
                    pady=1,
                )
                ttk.Label(
                    value_frame,
                    text=description,
                    font=("TkDefaultFont", 12, "bold"),
                    width=17,
                    anchor="w",
                ).pack(side=tk.LEFT)
                symbol_image = self._live_symbol_image(symbol)
                symbol_widget = ttk.Label(value_frame, image=symbol_image)
                symbol_widget.pack(side=tk.LEFT, padx=(5, 2))
                self.live_symbol_widgets[key] = symbol_widget
                ttk.Label(
                    value_frame,
                    textvariable=variable,
                    font=("TkFixedFont", 13, "bold"),
                    width=29,
                    anchor="w",
                ).pack(side=tk.LEFT)
            live_values.columnconfigure(column, weight=1)
        row += 1
        ttk.Label(
            controls,
            textvariable=self.live_status,
            font=("TkDefaultFont", 11, "bold"),
        ).grid(row=row, column=0, columnspan=3, sticky="w", pady=(5, 0))
        row += 1
        controls.columnconfigure(1, weight=1)

        self.figure, (
            self.ax_temperature,
            self.ax_command,
            self.ax_error,
        ) = self.plt.subplots(
            3, 1, figsize=(9, 8), sharex=True
        )
        self.figure.subplots_adjust(
            top=0.67, left=0.11, right=0.75, bottom=0.08, hspace=0.36
        )
        self.left_equations = self.figure.text(
            0.035, 0.98, "", ha="left", va="top", fontsize=16.0, linespacing=1.25
        )
        self.right_equations = self.figure.text(
            0.52, 0.98, "", ha="left", va="top", fontsize=16.0, linespacing=1.25
        )
        self.canvas = self.FigureCanvasTkAgg(self.figure, master=plots)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar = self.NavigationToolbar2Tk(self.canvas, plots, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(fill=tk.X)
        self.root.update_idletasks()
        outer.sashpos(0, 700)

    def _render_math_symbol(self, expression: str) -> tk.PhotoImage:
        """Render a control symbol with the same math engine as the plots."""

        buffer = io.BytesIO()
        with self.matplotlib.rc_context({"savefig.transparent": True}):
            self.math_to_image(
                f"${expression}$",
                buffer,
                prop=self.FontProperties(size=13.5),
                dpi=120,
                format="png",
                color="black",
            )
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        image = tk.PhotoImage(data=encoded)
        self.math_symbol_images.append(image)
        return image

    def _live_symbol_image(self, expression: str) -> tk.PhotoImage:
        """Return a cached MathText image for a live-value symbol."""

        if expression not in self.live_symbol_cache:
            self.live_symbol_cache[expression] = self._render_math_symbol(expression)
        return self.live_symbol_cache[expression]

    def _set_live_symbol(self, key: str, expression: str) -> None:
        """Change a live-row symbol when the selected process model changes."""

        self.live_symbol_widgets[key].configure(
            image=self._live_symbol_image(expression)
        )

    def _read_config(self) -> ModelConfig:
        values = {
            attribute: float(self.entries[attribute].get())
            for _symbol, _label, attribute, _units, _low, _high, _resolution
            in self.FIELD_SPECS
        }
        values["anti_windup"] = self.anti_windup.get()
        config = replace(self.defaults, **values)
        if self.parameter_source.get() == "measured":
            derived = constants_from_measurements(
                config.measured_cooling_chi_c_per_pwm,
                config.measured_heating_chi_c_per_pwm,
                config.measured_tau_s,
                config.tec_voltage_v,
                config.tec_resistance_ohm,
            )
            config = replace(
                config,
                total_capacitance_j_per_c=derived.total_capacitance_j_per_c,
                heat_loss_w_per_c=derived.heat_loss_w_per_c,
                tec_power_w_per_pwm=derived.cooling_power_w_per_pwm,
                heating_to_cooling_ratio=derived.heating_to_cooling_ratio,
            )
            self._show_derived_constants(config)
        validate_config(config)
        return config

    def _show_derived_constants(self, config: ModelConfig) -> None:
        """Keep the locked direct-constant fields synchronized with measurements."""

        if self.syncing_derived_fields:
            return
        self.syncing_derived_fields = True
        try:
            for attribute in (
                "total_capacitance_j_per_c",
                "heat_loss_w_per_c",
                "tec_power_w_per_pwm",
                "heating_to_cooling_ratio",
            ):
                self.entries[attribute].set(getattr(config, attribute))
        finally:
            self.syncing_derived_fields = False

    def _reset_experiment(self) -> None:
        try:
            self.config = self._read_config()
        except ValueError as error:
            messagebox.showerror("Check the model parameters", str(error))
            return
        self.state = ModelState(
            0.0, self.config.initial_c, self.config.initial_c, 0.0
        )
        self.times = [0.0]
        self.tec_temperatures = [self.config.initial_c]
        self.measured_temperatures = [self.config.initial_c]
        self.p_terms = [0.0]
        self.i_terms = [0.0]
        self.commands = [0.0]
        target_temperature = controller_target_temperature(
            self.config, self.controller_mode.get()
        )
        self.errors = [target_temperature - self.config.initial_c]
        self.latest = self._current_result()
        self.running = False
        self.run_button_text.set("Resume")
        self._draw()

    def _current_result(self) -> StepResult:
        error, p_term, i_term, command, saturated = controller_command(
            self.state,
            self.config,
            self.process_mode.get(),
            self.controller_mode.get(),
            advance_integral=False,
        )
        return StepResult(
            self.state.time_s,
            self.state.tec_temperature_c,
            self.state.measured_temperature_c,
            error,
            p_term,
            i_term,
            command,
            saturated,
        )

    def _change_process(self, _event=None) -> None:
        self._reset_experiment()

    def _change_controller(self, _event=None) -> None:
        self.state.integral_error_c_s = 0.0
        self.latest = self._current_result()
        self._draw()

    def _change_parameter_source(self, _event=None) -> None:
        """Switch between measured inputs and independently entered constants."""

        self._on_parameter_edit()

    def _zero_integral(self) -> None:
        """Clear controller memory without resetting time or temperature."""

        self.state.integral_error_c_s = 0.0
        self.latest = self._current_result()
        self._draw()

    def _on_parameter_edit(self, *_trace_arguments: str) -> None:
        """Apply valid slider and entry changes without restarting the model."""

        if self.syncing_derived_fields:
            return
        try:
            self.config = self._read_config()
        except (ValueError, tk.TclError):
            return
        if hasattr(self, "state"):
            self.latest = self._current_result()
            self._draw()

    def _apply_parameter_edit(self, _event=None) -> str:
        try:
            self.config = self._read_config()
        except ValueError as error:
            messagebox.showerror("Check the model parameters", str(error))
            return "break"
        self.latest = self._current_result()
        self._draw()
        return "break"

    def _toggle_running(self) -> None:
        if self.running:
            self.running = False
            self.run_button_text.set("Resume")
        else:
            try:
                self.config = self._read_config()
            except ValueError as error:
                messagebox.showerror("Check the model parameters", str(error))
                return
            self.running = True
            self.run_button_text.set("Pause")
        self._draw()

    def _schedule_next_tick(self) -> None:
        self.after_job = self.root.after(UPDATE_INTERVAL_MS, self._tick)

    def _tick(self) -> None:
        if self.running:
            simulated_interval = (
                self.config.simulation_speed * UPDATE_INTERVAL_MS / 1000.0
            )
            steps = max(1, round(simulated_interval / self.config.dt_s))
            for _ in range(steps):
                self.latest = advance_model(
                    self.state,
                    self.config,
                    self.process_mode.get(),
                    self.controller_mode.get(),
                )
                self._record(self.latest)
            self._trim_history()
            self._draw()
        self._schedule_next_tick()

    def _record(self, result: StepResult) -> None:
        self.times.append(result.time_s)
        self.tec_temperatures.append(result.tec_temperature_c)
        self.measured_temperatures.append(result.measured_temperature_c)
        self.p_terms.append(result.p_pwm)
        self.i_terms.append(result.i_pwm)
        self.commands.append(result.applied_pwm)
        self.errors.append(result.error_c)

    def _trim_history(self) -> None:
        earliest = self.state.time_s - 1.2 * self.config.window_s
        first = 0
        while first < len(self.times) - 1 and self.times[first] < earliest:
            first += 1
        if first:
            self.times = self.times[first:]
            self.tec_temperatures = self.tec_temperatures[first:]
            self.measured_temperatures = self.measured_temperatures[first:]
            self.p_terms = self.p_terms[first:]
            self.i_terms = self.i_terms[first:]
            self.commands = self.commands[first:]
            self.errors = self.errors[first:]

    def _draw(self) -> None:
        self._update_field_states()
        for axis in (self.ax_temperature, self.ax_command, self.ax_error):
            axis.clear()
            axis.grid(True, alpha=0.25)

        process = self.process_mode.get()
        controller = self.controller_mode.get()
        target_temperature = controller_target_temperature(self.config, controller)
        target_label = r"$T_{ss}$" if controller == "open_loop" else r"$T_{set}$"
        if process == "one_lump":
            self.ax_temperature.plot(
                self.times,
                self.tec_temperatures,
                color="tab:blue",
                linewidth=2,
                label=r"$T$",
            )
        else:
            if not self.mass_temperature_only.get():
                self.ax_temperature.plot(
                    self.times,
                    self.tec_temperatures,
                    color="tab:red",
                    linewidth=1.8,
                    label=r"TEC-side $T$",
                )
            self.ax_temperature.plot(
                self.times,
                self.measured_temperatures,
                color="tab:blue",
                linewidth=2,
                label=r"measured $T_m$",
            )
        self.ax_temperature.axhline(
            target_temperature,
            color="black",
            linestyle="--",
            linewidth=1,
            label=target_label,
        )
        self.ax_temperature.set_ylabel(r"Temperature ($^\circ$C)")
        self.ax_temperature.legend(
            loc="center left",
            bbox_to_anchor=(1.01, 0.5),
            fontsize=14.0,
            handlelength=2.2,
            borderaxespad=0.25,
        )

        self.ax_command.plot(
            self.times, self.p_terms, color="tab:blue", label=r"$u_P$"
        )
        self.ax_command.plot(
            self.times, self.i_terms, color="tab:orange", label=r"$u_I$"
        )
        self.ax_command.plot(
            self.times, self.commands, color="black", linewidth=2, label=r"applied $u$"
        )
        self.ax_command.axhline(0.0, color="gray", linewidth=0.8)
        self.ax_command.set_ylabel("Signed PWM")
        self.ax_command.legend(
            loc="center left",
            bbox_to_anchor=(1.01, 0.5),
            fontsize=14.0,
            handlelength=2.2,
            borderaxespad=0.25,
        )

        self.ax_error.plot(
            self.times,
            self.errors,
            color="tab:green",
            linewidth=2,
            label=(
                r"$e=T_{ss}-T_{measured}$"
                if controller == "open_loop"
                else r"$e=T_{set}-T_{measured}$"
            ),
        )
        self.ax_error.axhline(0.0, color="gray", linewidth=0.8)
        self.ax_error.set_ylabel(r"Error ($^\circ$C)")
        self.ax_error.set_xlabel("Model time (s)")
        self.ax_error.legend(
            loc="center left",
            bbox_to_anchor=(1.01, 0.5),
            fontsize=14.0,
            handlelength=2.2,
            borderaxespad=0.25,
        )

        left = max(0.0, self.state.time_s - self.config.window_s)
        right = max(self.config.window_s, self.state.time_s)
        self.ax_error.set_xlim(left, right)

        visible_temperatures = [
            value
            for time_s, value in zip(self.times, self.measured_temperatures)
            if time_s >= left
        ]
        if process == "one_lump" or not self.mass_temperature_only.get():
            visible_temperatures.extend(
                value
                for time_s, value in zip(self.times, self.tec_temperatures)
                if time_s >= left
            )
        visible_temperatures.extend((self.config.ambient_c, target_temperature))
        low_t = min(visible_temperatures)
        high_t = max(visible_temperatures)
        margin_t = max(1.0, 0.1 * (high_t - low_t))
        self.ax_temperature.set_ylim(low_t - margin_t, high_t + margin_t)

        visible_commands = [0.0]
        for time_s, p_term, i_term, command in zip(
            self.times, self.p_terms, self.i_terms, self.commands
        ):
            if time_s >= left:
                visible_commands.extend((p_term, i_term, command))
        low_u = min(visible_commands)
        high_u = max(visible_commands)
        margin_u = max(1.0, 0.08 * (high_u - low_u))
        self.ax_command.set_ylim(low_u - margin_u, high_u + margin_u)

        visible_errors = [
            value
            for time_s, value in zip(self.times, self.errors)
            if time_s >= left
        ] + [0.0]
        low_e = min(visible_errors)
        high_e = max(visible_errors)
        margin_e = max(0.25, 0.10 * (high_e - low_e))
        self.ax_error.set_ylim(low_e - margin_e, high_e + margin_e)

        cooling_chi = cooling_susceptibility(self.config)
        heating_chi = heating_susceptibility(self.config)
        susceptibility = (
            active_tec_coefficient(self.config, self.config.open_loop_pwm)
            / self.config.heat_loss_w_per_c
            if controller == "open_loop"
            else open_loop_susceptibility(self.config)
        )
        if process == "one_lump":
            self.left_equations.set_text(
                r"$\bf{Thermal\ model}$"
                "\n"
                r"$C=C_T+C_m$"
                "\n"
                r"$C\frac{dT}{dt}=P_u(u)u-H(T-T_{amb})$"
                "\n"
                rf"$\chi_c=\frac{{P_{{u,c}}}}{{H}}={cooling_chi:.3g},\quad"
                rf"\chi_h=\frac{{P_{{u,h}}}}{{H}}={heating_chi:.3g}\,^\circ\mathrm{{C/PWM}}$"
                "\n"
                rf"$r=\frac{{\chi_h}}{{\chi_c}}=\frac{{P_{{u,h}}}}{{P_{{u,c}}}}="
                rf"{self.config.heating_to_cooling_ratio:.3g}$"
                "\n"
                rf"$\tau=C/H={one_lump_time_constant(self.config):.3g}\,\mathrm{{s}}$"
            )
        else:
            tau_fast, tau_slow = two_lump_time_constants(self.config)
            self.left_equations.set_text(
                r"$\bf{Thermal\ model}$"
                "\n"
                r"$C_T\frac{dT}{dt}=P_u(u)u-G(T-T_m)$"
                "\n"
                r"$C_m\frac{dT_m}{dt}=G(T-T_m)-H(T_m-T_{amb})$"
                "\n"
                rf"$\chi_c={cooling_chi:.3g},\quad\chi_h={heating_chi:.3g}"
                r"\,^\circ\mathrm{C/PWM}$"
                "\n"
                rf"$r=\chi_h/\chi_c={self.config.heating_to_cooling_ratio:.3g}$"
                "\n"
                rf"$\tau_{{fast}}={tau_fast:.3g}\,\mathrm{{s}},\quad\tau_{{slow}}={tau_slow:.3g}\,\mathrm{{s}}$"
            )

        zeta = one_lump_pi_damping_ratio(self.config)
        zeta_text = r"\infty" if math.isinf(zeta) else f"{zeta:.3f}"
        self.right_equations.set_text(
            r"$\bf{Controller}$"
            "\n"
            rf"Open loop: $u=u_{{user}}={self.config.open_loop_pwm:.3g}\,\mathrm{{PWM}}$"
            "\n"
            r"P control: $e=T_{set}-T_{meas}$, $u_P=K_p e$"
            "\n"
            r"PI control: $u=u_P+u_I=K_p e+K_i\int e\,dt$"
            "\n"
            rf"One-lump PI: $\zeta={zeta_text}$ ({damping_description(zeta)})"
        )

        current_measured = measured_temperature(self.state, process)
        if process == "one_lump":
            self._set_live_symbol("temperature", r"T")
            self._set_live_symbol("time_scale", r"\tau_{\mathrm{OL}},\ \tau_P")
            self.live_temperature.set(f"= {self.state.tec_temperature_c:7.2f} °C")
            self.live_time_scale.set(
                f"= {one_lump_time_constant(self.config):.2f}; "
                f"{predicted_p_time_constant(self.config):.2f} s"
            )
        else:
            tau_fast, tau_slow = two_lump_time_constants(self.config)
            self._set_live_symbol("temperature", r"T,\ T_m")
            self._set_live_symbol(
                "time_scale", r"\tau_{\mathrm{fast}},\ \tau_{\mathrm{slow}}"
            )
            self.live_temperature.set(
                f"= {self.state.tec_temperature_c:7.2f}; "
                f"{current_measured:7.2f} °C"
            )
            self.live_time_scale.set(
                f"= {tau_fast:7.2f}; {tau_slow:7.2f} s"
            )
        self.live_error.set(f"= {self.latest.error_c:8.2f} °C")
        self.live_p.set(f"= {self.latest.p_pwm:8.2f} PWM")
        self.live_i.set(f"= {self.latest.i_pwm:8.2f} PWM")
        saturation = " (saturated)" if self.latest.saturated else ""
        self.live_command.set(
            f"= {self.latest.applied_pwm:8.2f} PWM{saturation}"
        )
        self.live_susceptibility.set(
            f"= {cooling_chi:.2f}; {heating_chi:.2f} °C/PWM"
        )
        delta_t = target_temperature - self.config.ambient_c
        if susceptibility > 0.0:
            required_command = delta_t / susceptibility
            self.live_required_command.set(
                f"= ΔT/χ = {required_command:7.2f} PWM"
            )
        else:
            self.live_required_command.set("= ΔT/χ = undefined")
        required_power = self.config.heat_loss_w_per_c * delta_t
        self.live_required_power.set(f"= HΔT = {required_power:7.2f} W")
        self.live_p_prediction.set(
            f"= {predicted_p_droop(self.config):7.2f} °C"
        )
        zeta_display = "∞" if math.isinf(zeta) else f"{zeta:.2f}"
        self.live_damping.set(
            f"= {zeta_display} ({damping_description(zeta)})"
        )
        run_state = "Running" if self.running else "Paused"
        self.live_status.set(
            f"{run_state} | {process.replace('_', ' ')} | "
            f"{controller.replace('_', ' ')} | {self.parameter_source.get()}"
        )
        self.canvas.draw_idle()

    def _update_field_states(self) -> None:
        """Disable sliders that do not affect the selected model or controller."""

        process = self.process_mode.get()
        controller = self.controller_mode.get()
        measured_parameters = self.parameter_source.get() == "measured"
        enabled = {
            attribute: True for attribute in self.field_widgets
        }
        enabled["coupling_w_per_c"] = process == "two_lump"
        for attribute in (
            "measured_cooling_chi_c_per_pwm",
            "measured_heating_chi_c_per_pwm",
            "measured_tau_s",
            "tec_voltage_v",
            "tec_resistance_ohm",
        ):
            enabled[attribute] = measured_parameters
        for attribute in (
            "total_capacitance_j_per_c",
            "heat_loss_w_per_c",
            "tec_power_w_per_pwm",
            "heating_to_cooling_ratio",
        ):
            enabled[attribute] = not measured_parameters
        enabled["open_loop_pwm"] = controller == "open_loop"
        enabled["setpoint_c"] = controller != "open_loop"
        enabled["kp_pwm_per_c"] = controller in {"p", "pi"}
        enabled["ki_pwm_per_c_s"] = controller == "pi"
        self.mass_only_button.configure(
            state="normal" if process == "two_lump" else "disabled"
        )
        for attribute, widgets in self.field_widgets.items():
            state = "normal" if enabled[attribute] else "disabled"
            for widget in widgets:
                try:
                    if str(widget.cget("state")) != state:
                        widget.configure(state=state)
                except tk.TclError:
                    pass


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Consistent one- and two-lump Module 6 TEC simulation"
    )
    parser.add_argument(
        "--demo", action="store_true", help="save a non-interactive two-lump PI plot"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("python/Lab_6_7_modeling_tec_v3_demo.png"),
        help="output path used with --demo",
    )
    args = parser.parse_args()
    if args.demo:
        run_demo(args.output)
        return

    root = tk.Tk()
    ModelingTECv3Gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
