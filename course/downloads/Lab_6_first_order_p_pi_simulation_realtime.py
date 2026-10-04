"""Real-time-display Module 6 model of P and PI temperature control.

The program deliberately keeps the physical model small enough to inspect. It
starts from a dimensional energy balance:

    C*dT/dt = P_u*u - H*(T - T_ambient)

The equivalent measured-parameter form is:

    dT/dt = (T_ambient + chi_Tu*u - T)/tau
    tau = C/H                 chi_Tu = P_u/H

Here ``u`` is signed PWM. Positive PWM heats and negative PWM cools. The GUI
lets the user run either controller under the same physical conditions:

    P:   u = Kp*error
    PI:  u = Kp*error + Ki*integral(error dt)

Run from the Phys39F26 repository root:

    .venv/bin/python python/Lab_6_first_order_p_pi_simulation_realtime.py

No Arduino is needed. This is a mathematical model, not a hardware controller.
Each complete simulated run is drawn progressively over 10 seconds so the
display develops like a live experiment.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import math
import tkinter as tk
import time
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


@dataclass(frozen=True)
class ModelConfig:
    """Physical, controller, and numerical parameters with explicit units."""

    ambient_c: float = 22.0
    initial_c: float = 22.0
    setpoint_c: float = 30.0
    thermal_capacitance_j_per_c: float = 100.0
    heat_loss_w_per_c: float = 1.25
    tec_power_w_per_pwm: float = 0.15
    dt_s: float = 0.25
    duration_s: float = 600.0
    kp_pwm_per_c: float = 18.0
    ki_pwm_per_c_s: float = 0.08
    pwm_limit: float = 255.0
    anti_windup: bool = True


@dataclass
class SimulationResult:
    """Complete time history for one controller."""

    time_s: list[float]
    temperature_c: list[float]
    error_c: list[float]
    signed_pwm: list[float]
    saturated: list[bool]

    @property
    def final_droop_c(self) -> float:
        return self.error_c[-1]

    @property
    def saturation_fraction(self) -> float:
        return sum(self.saturated) / len(self.saturated)


def clamp(value: float, low: float, high: float) -> float:
    """Restrict an actuator command to the available PWM interval."""

    return max(low, min(high, value))


def simulate(mode: str, config: ModelConfig) -> SimulationResult:
    """Integrate the one-lump model using the forward-Euler method.

    ``mode`` must be ``"p"`` or ``"pi"``. Conditional integration is used as
    a simple anti-windup rule: when saturation would drive the actuator farther
    into saturation, the integral is temporarily not increased.
    """

    if mode not in {"p", "pi"}:
        raise ValueError("mode must be 'p' or 'pi'")

    time_s: list[float] = []
    temperature_c: list[float] = []
    error_c: list[float] = []
    signed_pwm: list[float] = []
    saturated: list[bool] = []

    time = 0.0
    temperature = config.initial_c
    error_integral = 0.0

    while time <= config.duration_s + 0.5 * config.dt_s:
        error = config.setpoint_c - temperature
        proportional_term = config.kp_pwm_per_c * error

        if mode == "pi":
            proposed_integral = error_integral + error * config.dt_s
            proposed_command = (
                proportional_term
                + config.ki_pwm_per_c_s * proposed_integral
            )

            driving_farther_into_saturation = (
                proposed_command > config.pwm_limit and error > 0.0
            ) or (
                proposed_command < -config.pwm_limit and error < 0.0
            )
            if not (config.anti_windup and driving_farther_into_saturation):
                error_integral = proposed_integral

            unclamped_command = (
                proportional_term
                + config.ki_pwm_per_c_s * error_integral
            )
        else:
            unclamped_command = proportional_term

        command = clamp(
            unclamped_command,
            -config.pwm_limit,
            config.pwm_limit,
        )

        # Dimensional energy balance:
        # C*dT/dt = TEC power - heat lost to the surroundings.
        tec_power_w = config.tec_power_w_per_pwm * command
        heat_loss_w = config.heat_loss_w_per_c * (
            temperature - config.ambient_c
        )
        dtemperature_dt = (
            tec_power_w - heat_loss_w
        ) / config.thermal_capacitance_j_per_c
        temperature += config.dt_s * dtemperature_dt

        time_s.append(time)
        temperature_c.append(temperature)
        error_c.append(config.setpoint_c - temperature)
        signed_pwm.append(command)
        saturated.append(abs(unclamped_command) > config.pwm_limit)
        time += config.dt_s

    return SimulationResult(
        time_s=time_s,
        temperature_c=temperature_c,
        error_c=error_c,
        signed_pwm=signed_pwm,
        saturated=saturated,
    )


def open_loop_susceptibility(config: ModelConfig) -> float:
    """Return chi_Tu = P_u/H, the temperature change per signed PWM count."""

    return config.tec_power_w_per_pwm / config.heat_loss_w_per_c


def thermal_time_constant(config: ModelConfig) -> float:
    """Return tau = C/H in seconds."""

    return config.thermal_capacitance_j_per_c / config.heat_loss_w_per_c


def predicted_p_droop(config: ModelConfig) -> float:
    """Analytic unsaturated steady-state droop for proportional control."""

    loop_gain = open_loop_susceptibility(config) * config.kp_pwm_per_c
    return (config.setpoint_c - config.ambient_c) / (1.0 + loop_gain)


def pi_damping_ratio(config: ModelConfig) -> float:
    """Return the linear, unsaturated PI damping ratio.

    The PI characteristic equation is

        lambda^2 + ((H + P_u*Kp)/C)*lambda + P_u*Ki/C = 0.

    Ki = 0 removes the integral state from the controller, so the response
    reduces to first order. ``math.inf`` represents that nonoscillatory limit.
    """

    if config.ki_pwm_per_c_s == 0.0 or config.tec_power_w_per_pwm == 0.0:
        return math.inf
    numerator = config.heat_loss_w_per_c + (
        config.tec_power_w_per_pwm * config.kp_pwm_per_c
    )
    denominator = 2.0 * math.sqrt(
        config.thermal_capacitance_j_per_c
        * config.tec_power_w_per_pwm
        * config.ki_pwm_per_c_s
    )
    return numerator / denominator


def damping_description(damping_ratio: float) -> str:
    """Translate the damping ratio into the usual linear-system category."""

    if math.isinf(damping_ratio):
        return "first order because Ki = 0"
    if damping_ratio < 1.0 - 1e-9:
        return "underdamped"
    if damping_ratio > 1.0 + 1e-9:
        return "overdamped"
    return "critically damped"


DISPLAY_DURATION_S = 10.0
ANIMATION_FRAME_MS = 100


class Module6RealtimeApp:
    """A Module 6 interface that reveals each simulation over 10 seconds."""

    FIELD_SPECS = (
        ("Ambient temperature", "ambient_c", "°C"),
        ("Initial temperature", "initial_c", "°C"),
        ("Setpoint", "setpoint_c", "°C"),
        ("Thermal capacitance C", "thermal_capacitance_j_per_c", "J/K"),
        ("Heat-loss conductance H", "heat_loss_w_per_c", "W/K"),
        ("TEC power coefficient P_u", "tec_power_w_per_pwm", "W/PWM"),
        ("Proportional gain Kp", "kp_pwm_per_c", "PWM/°C"),
        ("Integral gain Ki", "ki_pwm_per_c_s", "PWM/(°C s)"),
        ("PWM limit", "pwm_limit", "PWM"),
        ("Simulation duration", "duration_s", "s"),
        ("Euler time step", "dt_s", "s"),
    )

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Module 6: Real-Time-Display P and PI Simulation")
        self.root.geometry("1280x820")
        self.root.minsize(1050, 700)

        self.defaults = ModelConfig()
        self.entries: dict[str, tk.StringVar] = {}
        self.anti_windup = tk.BooleanVar(value=self.defaults.anti_windup)
        self.controller_mode = tk.StringVar(value="p")
        self.animation_job: str | None = None
        self.animation_started_at = 0.0

        self._build_layout()
        self.run_model()

    def _build_layout(self) -> None:
        outer = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        outer.pack(fill=tk.BOTH, expand=True)

        controls = ttk.Frame(outer, padding=12)
        plots = ttk.Frame(outer, padding=(4, 8, 8, 8))
        outer.add(controls, weight=0)
        outer.add(plots, weight=1)

        ttk.Label(
            controls,
            text="Physical model and controller",
            font=("TkDefaultFont", 14, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        row = 1
        for label, attribute, units in self.FIELD_SPECS:
            value = getattr(self.defaults, attribute)
            variable = tk.StringVar(value=f"{value:g}")
            self.entries[attribute] = variable
            ttk.Label(controls, text=label).grid(row=row, column=0, sticky="w", pady=3)
            ttk.Entry(controls, textvariable=variable, width=11).grid(
                row=row, column=1, sticky="ew", padx=(8, 5)
            )
            ttk.Label(controls, text=units).grid(row=row, column=2, sticky="w")
            row += 1

        ttk.Label(
            controls,
            text="Controller",
            font=("TkDefaultFont", 11, "bold"),
        ).grid(row=row, column=0, sticky="w", pady=(8, 4))
        controller_selector = ttk.Frame(controls)
        controller_selector.grid(
            row=row, column=1, columnspan=2, sticky="ew", pady=(8, 4)
        )
        ttk.Radiobutton(
            controller_selector,
            text="P only",
            variable=self.controller_mode,
            value="p",
        ).pack(side=tk.LEFT, padx=(0, 12))
        ttk.Radiobutton(
            controller_selector,
            text="PI",
            variable=self.controller_mode,
            value="pi",
        ).pack(side=tk.LEFT)
        row += 1

        ttk.Checkbutton(
            controls,
            text="Prevent integral windup",
            variable=self.anti_windup,
        ).grid(row=row, column=0, columnspan=3, sticky="w", pady=(8, 4))
        row += 1

        button_bar = ttk.Frame(controls)
        button_bar.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(8, 10))
        self.run_button = ttk.Button(
            button_bar,
            text="Run 10 s experiment",
            command=self.run_model,
        )
        self.run_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(button_bar, text="Reset", command=self.reset_defaults).pack(
            side=tk.LEFT, padx=(6, 0)
        )
        row += 1

        ttk.Separator(controls).grid(row=row, column=0, columnspan=3, sticky="ew", pady=8)
        row += 1
        ttk.Label(
            controls,
            text="What to notice",
            font=("TkDefaultFont", 12, "bold"),
        ).grid(row=row, column=0, columnspan=3, sticky="w")
        row += 1
        ttk.Label(
            controls,
            text=(
                "1. Increase Kp: P droop decreases.\n"
                "2. Set Ki = 0: P and PI coincide.\n"
                "3. Restore Ki: PI removes droop slowly.\n"
                "4. Increase H: heat loss and P droop increase.\n"
                "5. Raise the setpoint: PWM may saturate.\n"
                "6. Disable anti-windup and compare overshoot."
            ),
            justify=tk.LEFT,
        ).grid(row=row, column=0, columnspan=3, sticky="w", pady=(5, 10))
        row += 1

        ttk.Label(
            controls,
            text="Model Results",
            font=("TkDefaultFont", 12, "bold"),
        ).grid(row=row, column=0, columnspan=3, sticky="w", pady=(0, 4))
        row += 1
        self.result_figure = Figure(figsize=(3.2, 3.15), dpi=100)
        self.result_figure.patch.set_alpha(0.0)
        self.result_axis = self.result_figure.add_subplot(111)
        self.result_axis.set_axis_off()
        self.result_axis.patch.set_alpha(0.0)
        self.result_canvas = FigureCanvasTkAgg(self.result_figure, master=controls)
        self.result_canvas.get_tk_widget().grid(
            row=row, column=0, columnspan=3, sticky="nsew"
        )
        controls.columnconfigure(1, weight=1)

        self.figure, (self.ax_temperature, self.ax_error, self.ax_pwm) = plt.subplots(
            3, 1, figsize=(9, 7), sharex=True
        )
        self.figure.subplots_adjust(
            top=0.70, left=0.15, right=0.94, bottom=0.09, hspace=0.40
        )
        self.canvas = FigureCanvasTkAgg(self.figure, master=plots)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, plots, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(fill=tk.X)

    def read_config(self) -> ModelConfig:
        """Convert text boxes into a validated ModelConfig."""

        values: dict[str, float | bool] = {}
        for _label, attribute, _units in self.FIELD_SPECS:
            values[attribute] = float(self.entries[attribute].get())
        values["anti_windup"] = self.anti_windup.get()

        config = replace(self.defaults, **values)
        if config.thermal_capacitance_j_per_c <= 0.0:
            raise ValueError("Thermal capacitance C must be positive.")
        if config.heat_loss_w_per_c <= 0.0:
            raise ValueError("Heat-loss conductance H must be positive.")
        if config.dt_s <= 0.0 or config.duration_s <= 0.0:
            raise ValueError("Time step and duration must be positive.")
        if config.dt_s > thermal_time_constant(config) / 5.0:
            raise ValueError("Use dt no larger than tau/5 for a meaningful Euler simulation.")
        if config.pwm_limit <= 0.0:
            raise ValueError("PWM limit must be positive.")
        if config.tec_power_w_per_pwm < 0.0:
            raise ValueError(
                "TEC power coefficient P_u cannot be negative in this sign convention."
            )
        if config.kp_pwm_per_c < 0.0 or config.ki_pwm_per_c_s < 0.0:
            raise ValueError("Kp and Ki must be zero or positive in this activity.")
        return config

    def reset_defaults(self) -> None:
        self._cancel_animation()
        for _label, attribute, _units in self.FIELD_SPECS:
            self.entries[attribute].set(f"{getattr(self.defaults, attribute):g}")
        self.anti_windup.set(self.defaults.anti_windup)
        self.controller_mode.set("p")
        self.run_model()

    def run_model(self) -> None:
        self._cancel_animation()
        try:
            config = self.read_config()
            mode = self.controller_mode.get()
            result = simulate(mode, config)
        except ValueError as error:
            messagebox.showerror("Check the model parameters", str(error))
            return

        self._show_result_lines(
            self._time_independent_result_lines(config, mode)
            + [
                "Experiment running: the simulated time axis",
                "is compressed into 10 seconds.",
            ]
        )
        self.run_button.state(["disabled"])
        self.animation_started_at = time.monotonic()
        self._animate(config, result, mode)

    def _cancel_animation(self) -> None:
        if self.animation_job is not None:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
        if hasattr(self, "run_button"):
            self.run_button.state(["!disabled"])

    def _animate(
        self,
        config: ModelConfig,
        result: SimulationResult,
        mode: str,
    ) -> None:
        elapsed = time.monotonic() - self.animation_started_at
        fraction = min(elapsed / DISPLAY_DURATION_S, 1.0)
        end_index = max(1, math.ceil(fraction * len(result.time_s)))
        self._draw(config, result, mode, end_index)

        if fraction < 1.0:
            self.animation_job = self.root.after(
                ANIMATION_FRAME_MS,
                self._animate,
                config,
                result,
                mode,
            )
            return

        self.animation_job = None
        self.run_button.state(["!disabled"])
        self._summarize(config, result, mode)

    def _draw(
        self,
        config: ModelConfig,
        result: SimulationResult,
        mode: str,
        end_index: int,
    ) -> None:
        for axis in (self.ax_temperature, self.ax_error, self.ax_pwm):
            axis.clear()
            axis.grid(True, alpha=0.25)

        label = "P only" if mode == "p" else "PI"
        color = "tab:blue" if mode == "p" else "tab:red"
        self.ax_temperature.plot(
            result.time_s[:end_index],
            result.temperature_c[:end_index],
            label=label,
            color=color,
        )
        self.ax_temperature.axhline(
            config.setpoint_c, color="black", linestyle="--", linewidth=1, label="setpoint"
        )
        self.ax_temperature.set_ylabel("Temp (°C)")
        self.ax_temperature.legend(
            loc="center right",
        )

        self.ax_error.plot(
            result.time_s[:end_index],
            result.error_c[:end_index],
            color=color,
            label=label,
        )
        self.ax_error.axhline(0.0, color="black", linestyle="--", linewidth=1)
        self.ax_error.set_ylabel("Error (°C)")

        self.ax_pwm.plot(
            result.time_s[:end_index],
            result.signed_pwm[:end_index],
            color=color,
            label=label,
        )
        self.ax_pwm.axhline(0.0, color="black", linestyle="--", linewidth=1)
        self.ax_pwm.axhline(config.pwm_limit, color="gray", linestyle=":", linewidth=1)
        self.ax_pwm.axhline(-config.pwm_limit, color="gray", linestyle=":", linewidth=1)
        self.ax_pwm.set_ylabel("Signed PWM")
        self.ax_pwm.set_xlabel("Time (s)")

        # Keep the ranges fixed while the curves grow, like a strip chart
        # whose axes were selected before an experimental run began.
        self.ax_pwm.set_xlim(0.0, config.duration_s)
        self._set_fixed_limits(
            self.ax_temperature,
            result.temperature_c + [config.setpoint_c],
        )
        self._set_fixed_limits(
            self.ax_error,
            result.error_c + [0.0],
        )
        self.ax_pwm.set_ylim(-1.05 * config.pwm_limit, 1.05 * config.pwm_limit)

        # Stagger adjacent vertical labels so the long rotated text does not
        # crowd at the boundary between plots. The first and third labels share
        # one line; the middle label sits on a second line closer to its axis.
        self.ax_temperature.yaxis.set_label_coords(-0.14, 0.5)
        self.ax_error.yaxis.set_label_coords(-0.07, 0.5)
        self.ax_pwm.yaxis.set_label_coords(-0.14, 0.5)

        title_lines = [
            r"Energy balance: $C\frac{dT}{dt}=P_u u-H(T-T_{amb})$",
            (
                r"Measured form: $\frac{dT}{dt}=\frac{T_{amb}+\chi_{T,u}u-T}{\tau}$, "
                r"$\tau=\frac{C}{H}$, $\chi_{T,u}=\frac{P_u}{H}$"
            ),
            r"P control: $e=T_{set}-T$, $u_P=K_p e$",
            r"PI control: $u_{PI}=K_p e+K_i\int e\,dt$",
        ]
        if mode == "pi":
            title_lines.append(
                r"PI damping: $\zeta=\frac{H+P_uK_p}{2\sqrt{CP_uK_i}}$; "
                r"underdamped when $\zeta<1$"
            )
        self.figure.suptitle("\n".join(title_lines), fontsize=11)
        self.canvas.draw_idle()

    def _show_result_lines(self, lines: list[str]) -> None:
        """Render result notation with Matplotlib's math typography."""

        self.result_axis.clear()
        self.result_axis.set_axis_off()
        self.result_axis.patch.set_alpha(0.0)
        y_position = 0.99
        for line in lines:
            self.result_axis.text(
                0.0,
                y_position,
                line,
                transform=self.result_axis.transAxes,
                ha="left",
                va="top",
                fontsize=9.5,
            )
            y_position -= 0.068
        self.result_canvas.draw_idle()

    @staticmethod
    def _time_independent_result_lines(config: ModelConfig, mode: str) -> list[str]:
        """Return results fixed by the model parameters before integration."""

        susceptibility = open_loop_susceptibility(config)
        controller_label = r"\mathrm{P\ only}" if mode == "p" else r"\mathrm{PI}"
        lines = [
            rf"Controller $={controller_label}$",
            r"Heat-loss term $-H(T-T_{\mathrm{amb}})$",
            rf"Time constant $\tau=C/H={thermal_time_constant(config):.3g}\,\mathrm{{s}}$",
            rf"Susceptibility $\chi_{{T,u}}=P_u/H={susceptibility:.4g}\,{{}}^\circ\mathrm{{C}}/\mathrm{{PWM}}$",
            rf"Loop gain $\chi_{{T,u}}K_p={susceptibility * config.kp_pwm_per_c:.3g}$",
        ]
        if mode == "p":
            lines.append(
                rf"Predicted $\mathrm{{P}}$ droop $={predicted_p_droop(config):.3f}\,{{}}^\circ\mathrm{{C}}$"
            )
        else:
            damping_ratio = pi_damping_ratio(config)
            damping_value = (
                r"\infty" if math.isinf(damping_ratio) else f"{damping_ratio:.3f}"
            )
            lines[1:1] = [
                rf"$\mathrm{{PI}}$ damping ratio $\zeta={damping_value}$",
                f"Linear prediction: {damping_description(damping_ratio)}",
            ]
        return lines

    @staticmethod
    def _set_fixed_limits(axis, values: list[float]) -> None:
        low = min(values)
        high = max(values)
        span = high - low
        margin = 0.05 * span if span > 0.0 else 0.5
        axis.set_ylim(low - margin, high + margin)

    def _summarize(
        self,
        config: ModelConfig,
        result: SimulationResult,
        mode: str,
    ) -> None:
        controller_name = r"\mathrm{P}" if mode == "p" else r"\mathrm{PI}"
        self._show_result_lines(
            self._time_independent_result_lines(config, mode)
            + [
                rf"Simulated ${controller_name}$ droop $={result.final_droop_c:.3f}\,{{}}^\circ\mathrm{{C}}$",
                rf"${controller_name}$ saturation $={100 * result.saturation_fraction:.1f}\%$",
            ]
        )


def main() -> None:
    root = tk.Tk()
    Module6RealtimeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
