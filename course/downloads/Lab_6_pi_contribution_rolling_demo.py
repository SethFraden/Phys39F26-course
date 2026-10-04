"""Rolling-window demonstration of P and I contributions to temperature control.

The program starts with integral action disabled. The proportional contribution
to the signed PWM command is

    u_P = Kp * error

and the integral contribution is

    u_I = Ki * integral(error dt).

Press "Enable I from zero" to begin accumulating error. Press "Zero and
disable I" to set the integral contribution back to zero and hold it there.
The counters and rolling plots make the two contributions visible separately.

Run from the Phys39F26 repository root:

    .venv/bin/python python/Lab_6_pi_contribution_rolling_demo.py

No Arduino is needed. This is a mathematical model, not a hardware controller.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import math
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


UPDATE_INTERVAL_MS = 50


@dataclass(frozen=True)
class ModelConfig:
    """Physical, controller, display, and numerical parameters."""

    ambient_c: float = 22.0
    initial_c: float = 22.0
    setpoint_c: float = 30.0
    thermal_capacitance_j_per_c: float = 100.0
    heat_loss_w_per_c: float = 1.25
    tec_power_w_per_pwm: float = 0.15
    kp_pwm_per_c: float = 18.0
    ki_pwm_per_c_s: float = 0.08
    pwm_limit: float = 255.0
    dt_s: float = 0.25
    window_s: float = 180.0
    simulation_speed: float = 10.0
    anti_windup: bool = True


@dataclass
class ModelState:
    """Current state of the one-lump model and PI controller."""

    time_s: float
    temperature_c: float
    integral_error_c_s: float = 0.0


@dataclass(frozen=True)
class StepResult:
    """Quantities produced by one numerical time step."""

    time_s: float
    temperature_c: float
    error_c: float
    p_pwm: float
    i_pwm: float
    applied_pwm: float
    saturated: bool


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def pi_damping_ratio(config: ModelConfig) -> float:
    """Return the linear, unsaturated PI damping ratio."""

    denominator = 2.0 * math.sqrt(
        config.thermal_capacitance_j_per_c
        * config.tec_power_w_per_pwm
        * config.ki_pwm_per_c_s
    )
    if denominator == 0.0:
        return math.inf
    return (
        config.heat_loss_w_per_c
        + config.tec_power_w_per_pwm * config.kp_pwm_per_c
    ) / denominator


def damping_description(damping_ratio: float) -> str:
    """Classify the linear PI response using its damping ratio."""

    if math.isinf(damping_ratio):
        return "no integral action"
    if damping_ratio < 1.0 - 1e-9:
        return "underdamped"
    if damping_ratio > 1.0 + 1e-9:
        return "overdamped"
    return "critically damped"


def advance_model(
    state: ModelState,
    config: ModelConfig,
    integral_enabled: bool,
) -> StepResult:
    """Advance the controller and one-lump energy balance by one Euler step."""

    error_c = config.setpoint_c - state.temperature_c
    p_pwm = config.kp_pwm_per_c * error_c

    if integral_enabled:
        candidate_integral = state.integral_error_c_s + error_c * config.dt_s
        i_pwm = config.ki_pwm_per_c_s * candidate_integral
    else:
        candidate_integral = 0.0
        i_pwm = 0.0

    raw_pwm = p_pwm + i_pwm
    applied_pwm = clamp(raw_pwm, -config.pwm_limit, config.pwm_limit)
    saturated = not math.isclose(raw_pwm, applied_pwm)

    # Conditional integration prevents the I term from growing farther into
    # saturation while still allowing it to unwind toward the usable range.
    pushing_farther_into_saturation = (
        raw_pwm > config.pwm_limit and error_c > 0.0
    ) or (raw_pwm < -config.pwm_limit and error_c < 0.0)
    if (
        integral_enabled
        and config.anti_windup
        and saturated
        and pushing_farther_into_saturation
    ):
        candidate_integral = state.integral_error_c_s
        i_pwm = config.ki_pwm_per_c_s * candidate_integral
        raw_pwm = p_pwm + i_pwm
        applied_pwm = clamp(raw_pwm, -config.pwm_limit, config.pwm_limit)
        saturated = not math.isclose(raw_pwm, applied_pwm)

    state.integral_error_c_s = candidate_integral
    heating_w = config.tec_power_w_per_pwm * applied_pwm
    heat_loss_w = config.heat_loss_w_per_c * (
        state.temperature_c - config.ambient_c
    )
    state.temperature_c += (
        (heating_w - heat_loss_w)
        / config.thermal_capacitance_j_per_c
        * config.dt_s
    )
    state.time_s += config.dt_s

    return StepResult(
        time_s=state.time_s,
        temperature_c=state.temperature_c,
        error_c=error_c,
        p_pwm=p_pwm,
        i_pwm=i_pwm,
        applied_pwm=applied_pwm,
        saturated=saturated,
    )


class PIContributionDemo:
    """Tk interface for switching integral action into a running P controller."""

    FIELD_SPECS = (
        ("Ambient temperature", "ambient_c", "°C"),
        ("Initial temperature", "initial_c", "°C"),
        ("Setpoint", "setpoint_c", "°C"),
        ("Thermal capacitance C", "thermal_capacitance_j_per_c", "J/K"),
        ("Heat-loss conductance H", "heat_loss_w_per_c", "W/K"),
        ("TEC coefficient P_u", "tec_power_w_per_pwm", "W/PWM"),
        ("Proportional gain Kp", "kp_pwm_per_c", "PWM/°C"),
        ("Integral gain Ki", "ki_pwm_per_c_s", "PWM/(°C s)"),
        ("PWM limit", "pwm_limit", "PWM"),
        ("Euler time step", "dt_s", "s"),
        ("Rolling window", "window_s", "s"),
        ("Simulation speed", "simulation_speed", "sim s/real s"),
    )

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Module 6: P and I Contribution Demonstration")
        self.root.geometry("1320x850")
        self.root.minsize(1100, 720)

        self.defaults = ModelConfig()
        self.config = self.defaults
        self.state = ModelState(0.0, self.defaults.initial_c)
        self.entries: dict[str, tk.StringVar] = {}
        self.anti_windup = tk.BooleanVar(value=self.defaults.anti_windup)
        self.integral_enabled = False
        self.running = True
        self.after_job: str | None = None
        self.latest_result: StepResult | None = None
        self.i_enabled_times: list[float] = []
        self.temperature_limits = (0.0, 1.0)

        self.times: list[float] = []
        self.temperatures: list[float] = []
        self.p_terms: list[float] = []
        self.i_terms: list[float] = []
        self.total_commands: list[float] = []

        self.p_counter = tk.StringVar()
        self.i_counter = tk.StringVar()
        self.error_counter = tk.StringVar()
        self.total_counter = tk.StringVar()
        self.temperature_counter = tk.StringVar()
        self.required_command_counter = tk.StringVar()
        self.required_power_counter = tk.StringVar()
        self.status_text = tk.StringVar()
        self.run_button_text = tk.StringVar(value="Pause")

        self._build_layout()
        self._reset_experiment()
        for variable in self.entries.values():
            variable.trace_add("write", self._on_parameter_edit)
        self.anti_windup.trace_add("write", self._on_parameter_edit)
        self._schedule_next_tick()

    def _build_layout(self) -> None:
        outer = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        outer.pack(fill=tk.BOTH, expand=True)

        controls = ttk.Frame(outer, padding=12)
        plots = ttk.Frame(outer, padding=(4, 8, 8, 8))
        outer.add(controls, weight=0)
        outer.add(plots, weight=1)

        ttk.Label(
            controls,
            text="P and I contributions",
            font=("TkDefaultFont", 14, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        row = 1
        for label, attribute, units in self.FIELD_SPECS:
            variable = tk.StringVar(value=f"{getattr(self.defaults, attribute):g}")
            self.entries[attribute] = variable
            ttk.Label(controls, text=label).grid(row=row, column=0, sticky="w", pady=2)
            ttk.Entry(controls, textvariable=variable, width=10).grid(
                row=row, column=1, sticky="ew", padx=(8, 5)
            )
            ttk.Label(controls, text=units).grid(row=row, column=2, sticky="w")
            row += 1

        ttk.Checkbutton(
            controls,
            text="Prevent integral windup",
            variable=self.anti_windup,
        ).grid(row=row, column=0, columnspan=3, sticky="w", pady=(6, 8))
        row += 1

        mode_buttons = ttk.Frame(controls)
        mode_buttons.grid(row=row, column=0, columnspan=3, sticky="ew")
        ttk.Button(
            mode_buttons,
            text="Enable I from zero",
            command=self._enable_integral_from_zero,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(
            mode_buttons,
            text="Zero and disable I",
            command=self._zero_and_disable_integral,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))
        row += 1

        run_buttons = ttk.Frame(controls)
        run_buttons.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(6, 10))
        ttk.Button(
            run_buttons,
            textvariable=self.run_button_text,
            command=self._toggle_running,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(
            run_buttons,
            text="Reset experiment",
            command=self._reset_experiment,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))
        row += 1

        ttk.Separator(controls).grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=(0, 8)
        )
        row += 1
        ttk.Label(
            controls,
            text="Live controller contributions",
            font=("TkDefaultFont", 12, "bold"),
        ).grid(row=row, column=0, columnspan=3, sticky="w", pady=(0, 5))
        row += 1

        for variable in (
            self.p_counter,
            self.i_counter,
            self.error_counter,
            self.total_counter,
            self.temperature_counter,
            self.required_command_counter,
            self.required_power_counter,
        ):
            ttk.Label(
                controls,
                textvariable=variable,
                font=("TkFixedFont", 12, "bold"),
            ).grid(row=row, column=0, columnspan=3, sticky="w", pady=2)
            row += 1

        ttk.Label(
            controls,
            textvariable=self.status_text,
            font=("TkDefaultFont", 11, "bold"),
        ).grid(row=row, column=0, columnspan=3, sticky="w", pady=(6, 0))
        controls.columnconfigure(1, weight=1)

        self.figure, (self.ax_temperature, self.ax_command) = plt.subplots(
            2, 1, figsize=(9, 7), sharex=True
        )
        self.figure.subplots_adjust(
            top=0.78, left=0.12, right=0.80, bottom=0.10, hspace=0.28
        )
        self.left_equations = self.figure.text(
            0.07,
            0.965,
            "",
            ha="left",
            va="top",
            fontsize=10.5,
            linespacing=1.35,
        )
        self.right_equations = self.figure.text(
            0.56,
            0.965,
            "",
            ha="left",
            va="top",
            fontsize=10.5,
            linespacing=1.35,
        )
        self.canvas = FigureCanvasTkAgg(self.figure, master=plots)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, plots, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(fill=tk.X)

    def _read_config(self) -> ModelConfig:
        values: dict[str, float | bool] = {}
        for _label, attribute, _units in self.FIELD_SPECS:
            values[attribute] = float(self.entries[attribute].get())
        values["anti_windup"] = self.anti_windup.get()
        config = replace(self.defaults, **values)

        if config.thermal_capacitance_j_per_c <= 0.0:
            raise ValueError("Thermal capacitance C must be positive.")
        if config.heat_loss_w_per_c <= 0.0:
            raise ValueError("Heat-loss conductance H must be positive.")
        if config.tec_power_w_per_pwm < 0.0:
            raise ValueError("TEC coefficient P_u cannot be negative.")
        if config.kp_pwm_per_c < 0.0 or config.ki_pwm_per_c_s < 0.0:
            raise ValueError("Kp and Ki must be zero or positive.")
        if config.pwm_limit <= 0.0 or config.dt_s <= 0.0:
            raise ValueError("PWM limit and time step must be positive.")
        if config.window_s <= 0.0 or config.simulation_speed <= 0.0:
            raise ValueError("Rolling window and simulation speed must be positive.")
        if config.dt_s > (config.thermal_capacitance_j_per_c / config.heat_loss_w_per_c) / 5:
            raise ValueError("Use a time step no larger than tau/5.")
        return config

    def _reset_experiment(self) -> None:
        try:
            self.config = self._read_config()
        except ValueError as error:
            messagebox.showerror("Check the model parameters", str(error))
            return

        self.state = ModelState(0.0, self.config.initial_c)
        self._set_temperature_limits()
        self.integral_enabled = False
        self.i_enabled_times.clear()
        self.times = [0.0]
        self.temperatures = [self.config.initial_c]
        initial_error = self.config.setpoint_c - self.config.initial_c
        initial_p = self.config.kp_pwm_per_c * initial_error
        self.p_terms = [initial_p]
        self.i_terms = [0.0]
        self.total_commands = [
            clamp(initial_p, -self.config.pwm_limit, self.config.pwm_limit)
        ]
        self.latest_result = StepResult(
            time_s=0.0,
            temperature_c=self.config.initial_c,
            error_c=initial_error,
            p_pwm=initial_p,
            i_pwm=0.0,
            applied_pwm=self.total_commands[0],
            saturated=not math.isclose(initial_p, self.total_commands[0]),
        )
        self.running = False
        self.run_button_text.set("Resume")
        self._update_counters()
        self._draw()

    def _set_temperature_limits(self) -> None:
        """Choose fixed temperature limits for the current parameter set."""

        temperature_anchors = (
            self.config.ambient_c,
            self.state.temperature_c,
            self.config.setpoint_c,
        )
        temperature_span = max(temperature_anchors) - min(temperature_anchors)
        temperature_margin = max(2.0, 0.10 * temperature_span)
        self.temperature_limits = (
            min(temperature_anchors) - temperature_margin,
            max(temperature_anchors) + temperature_margin,
        )

    def _on_parameter_edit(self, *_trace_arguments: str) -> None:
        """Apply valid parameter edits immediately while the model is paused."""

        if self.running:
            return
        try:
            self.config = self._read_config()
        except ValueError:
            # A text field is temporarily incomplete while the user is typing.
            return
        self._set_temperature_limits()
        self._refresh_current_controller_values()
        self._update_counters()
        self._draw()

    def _refresh_current_controller_values(self) -> None:
        """Recalculate controller values without advancing model time."""

        error_c = self.config.setpoint_c - self.state.temperature_c
        p_pwm = self.config.kp_pwm_per_c * error_c
        i_pwm = (
            self.config.ki_pwm_per_c_s * self.state.integral_error_c_s
            if self.integral_enabled
            else 0.0
        )
        applied_pwm = clamp(
            p_pwm + i_pwm,
            -self.config.pwm_limit,
            self.config.pwm_limit,
        )
        self.latest_result = StepResult(
            time_s=self.state.time_s,
            temperature_c=self.state.temperature_c,
            error_c=error_c,
            p_pwm=p_pwm,
            i_pwm=i_pwm,
            applied_pwm=applied_pwm,
            saturated=not math.isclose(p_pwm + i_pwm, applied_pwm),
        )
        if self.times:
            self.temperatures[-1] = self.state.temperature_c
            self.p_terms[-1] = p_pwm
            self.i_terms[-1] = i_pwm
            self.total_commands[-1] = applied_pwm

    def _enable_integral_from_zero(self) -> None:
        self.state.integral_error_c_s = 0.0
        self.integral_enabled = True
        self.i_enabled_times.append(self.state.time_s)
        self._refresh_current_controller_values()
        self._update_counters()
        self._draw()

    def _zero_and_disable_integral(self) -> None:
        self.state.integral_error_c_s = 0.0
        self.integral_enabled = False
        self._refresh_current_controller_values()
        self._update_counters()
        self._draw()

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
            self._set_temperature_limits()
            self._refresh_current_controller_values()
            self.running = True
            self.run_button_text.set("Pause")
        self._update_counters()
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
                self.latest_result = advance_model(
                    self.state,
                    self.config,
                    self.integral_enabled,
                )
                self._record(self.latest_result)
            self._trim_history()
            self._update_counters()
            self._draw()
        self._schedule_next_tick()

    def _record(self, result: StepResult) -> None:
        self.times.append(result.time_s)
        self.temperatures.append(result.temperature_c)
        self.p_terms.append(result.p_pwm)
        self.i_terms.append(result.i_pwm)
        self.total_commands.append(result.applied_pwm)

    def _trim_history(self) -> None:
        earliest = self.state.time_s - 1.2 * self.config.window_s
        first = 0
        while first < len(self.times) - 1 and self.times[first] < earliest:
            first += 1
        if first:
            self.times = self.times[first:]
            self.temperatures = self.temperatures[first:]
            self.p_terms = self.p_terms[first:]
            self.i_terms = self.i_terms[first:]
            self.total_commands = self.total_commands[first:]
        self.i_enabled_times = [
            event_time for event_time in self.i_enabled_times if event_time >= earliest
        ]

    def _update_counters(self) -> None:
        if self.latest_result is None:
            return
        result = self.latest_result
        displayed_i = result.i_pwm if self.integral_enabled else 0.0
        displayed_total = clamp(
            result.p_pwm + displayed_i,
            -self.config.pwm_limit,
            self.config.pwm_limit,
        )
        self.p_counter.set(f"P contribution  u_P = {result.p_pwm:8.2f} PWM")
        self.i_counter.set(f"I contribution  u_I = {displayed_i:8.2f} PWM")
        self.error_counter.set(f"Error             e = {result.error_c:8.3f} °C")
        self.total_counter.set(f"Applied command u = {displayed_total:8.2f} PWM")
        self.temperature_counter.set(
            f"Temperature       T = {result.temperature_c:8.3f} °C"
        )
        delta_t_c = self.config.setpoint_c - self.config.ambient_c
        susceptibility_c_per_pwm = (
            self.config.tec_power_w_per_pwm / self.config.heat_loss_w_per_c
        )
        if susceptibility_c_per_pwm > 0.0:
            required_pwm = delta_t_c / susceptibility_c_per_pwm
            self.required_command_counter.set(
                f"Steady command u_ss = ΔT/χ = {required_pwm:8.2f} PWM"
            )
        else:
            self.required_command_counter.set(
                "Steady command u_ss = ΔT/χ = undefined"
            )
        required_power_w = self.config.heat_loss_w_per_c * delta_t_c
        self.required_power_counter.set(
            f"Steady power   Q̇_ss = HΔT = {required_power_w:8.2f} W"
        )
        run_state = "Running" if self.running else "Paused"
        mode = "PI active" if self.integral_enabled else "P only: I held at zero"
        saturation = " | PWM saturated" if abs(displayed_total) >= self.config.pwm_limit else ""
        self.status_text.set(run_state + " | " + mode + saturation)

    def _draw(self) -> None:
        for axis in (self.ax_temperature, self.ax_command):
            axis.clear()
            axis.grid(True, alpha=0.25)

        self.ax_temperature.plot(
            self.times,
            self.temperatures,
            color="tab:blue",
            linewidth=2,
            label=r"$T$",
        )
        self.ax_temperature.axhline(
            self.config.setpoint_c,
            color="black",
            linestyle="--",
            linewidth=1,
            label=r"$T_{\mathrm{set}}$",
        )
        self.ax_temperature.set_ylabel(r"Temperature ($^\circ$C)")
        self.ax_temperature.set_ylim(*self.temperature_limits)
        self.ax_temperature.legend(
            loc="center left",
            bbox_to_anchor=(1.01, 0.5),
            ncol=1,
            fontsize=9,
            handlelength=2.0,
            borderaxespad=0.2,
        )

        self.ax_command.plot(
            self.times,
            self.p_terms,
            color="tab:blue",
            linewidth=1.8,
            label=r"$u_P=K_p e$",
        )
        self.ax_command.plot(
            self.times,
            self.i_terms,
            color="tab:orange",
            linewidth=1.8,
            label=r"$u_I=K_i\int e\,dt$",
        )
        self.ax_command.plot(
            self.times,
            self.total_commands,
            color="black",
            linewidth=2,
            label=r"applied $u$",
        )
        self.ax_command.axhline(0.0, color="gray", linewidth=0.8)
        self.ax_command.set_ylabel("Signed PWM")
        self.ax_command.set_xlabel("Model time (s)")
        self.ax_command.legend(
            loc="center left",
            bbox_to_anchor=(1.01, 0.5),
            ncol=1,
            fontsize=9,
            handlelength=2.0,
            borderaxespad=0.2,
        )

        left = max(0.0, self.state.time_s - self.config.window_s)
        right = max(self.config.window_s, self.state.time_s)
        for event_time in self.i_enabled_times:
            if left <= event_time <= right:
                for axis in (self.ax_temperature, self.ax_command):
                    axis.axvline(
                        event_time,
                        color="tab:green",
                        linestyle="--",
                        linewidth=1.2,
                    )
        self.ax_command.set_xlim(left, right)

        visible_commands = [0.0]
        for time_s, p_pwm, i_pwm, total_pwm in zip(
            self.times,
            self.p_terms,
            self.i_terms,
            self.total_commands,
        ):
            if time_s >= left:
                visible_commands.extend((p_pwm, i_pwm, total_pwm))
        command_low = min(visible_commands)
        command_high = max(visible_commands)
        command_span = command_high - command_low
        command_margin = 0.08 * command_span if command_span > 0.0 else 1.0
        self.ax_command.set_ylim(
            command_low - command_margin,
            command_high + command_margin,
        )

        damping_ratio = pi_damping_ratio(self.config)
        damping_value = (
            r"\infty" if math.isinf(damping_ratio) else f"{damping_ratio:.3f}"
        )
        damping_class = damping_description(damping_ratio)
        time_constant_s = (
            self.config.thermal_capacitance_j_per_c
            / self.config.heat_loss_w_per_c
        )
        self.left_equations.set_text(
            r"$C\frac{dT}{dt}=P_u u-H(T-T_{amb})$"
            "\n"
            rf"$\tau=\frac{{C}}{{H}}={time_constant_s:.3g}\,\mathrm{{s}}$"
            "\n"
            rf"$\zeta=\frac{{H+P_uK_p}}{{2\sqrt{{CP_uK_i}}}}={damping_value}$"
        )
        self.right_equations.set_text(
            r"P control: $e=T_{set}-T$, $u_P=K_p e$"
            "\n"
            r"PI control: $u_{PI}=u_P+u_I=K_p e+K_i\int e\,dt$"
            "\n"
            f"PI model: {damping_class}"
        )
        self.canvas.draw_idle()


def main() -> None:
    root = tk.Tk()
    PIContributionDemo(root)
    root.mainloop()


if __name__ == "__main__":
    main()
