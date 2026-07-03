"""Python conversion of the legacy MATLAB App Designer app ModelingTECv2.

The original MATLAB app is a teaching simulator, not a hardware controller. It
shows three progressively richer thermal models:

1. Manual TEC drive: choose PWM and heat/cool direction.
2. Proportional control: the model chooses PWM from the temperature error.
3. Proportional control with a thermal mass: the TEC temperature and the
   measured thermistor/block temperature are separate state variables.

Run the desktop GUI:

    python python/Lab_6_7_modeling_tec_v2.py

Run a non-interactive demo and save a plot:

    python python/Lab_6_7_modeling_tec_v2.py --demo
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import tempfile
import textwrap


MANUAL_TEC_GAIN = 20.0
MIN_TEMPERATURE_DISPLAY_SPAN_C = 0.1
EQUATION_TOP_PADDING_POINTS = 3.0
EQUATION_BLANK_LINE_SPACING_POINTS = 8.0
EQUATION_FRACTION_LINE_SPACING_POINTS = 27.0
EQUATION_MATH_LINE_SPACING_POINTS = 19.0
EQUATION_TEXT_LINE_SPACING_POINTS = 16.0


@dataclass
class ModelInputs:
    """All values that would have come from MATLAB app sliders and switches."""

    mode: str = "manual"
    dt_s: float = 0.01
    room_c: float = 20.0
    tec_power_on: bool = False
    manual_pwm: float = 0.0
    manual_heat_cool: int = 1
    setpoint_c: float = 25.0
    kp: float = 10.0
    heat_loss_h: float = 1.0
    mass_coupling: float = 10.0


@dataclass
class ModelSample:
    """One row of simulated data."""

    time_s: float
    tec_temp_c: float
    thermistor_temp_c: float
    signed_pwm: float
    heat_cool: int


class ModelingTECv2Model:
    """Forward-Euler thermal model translated from ModelingTECv2.mlapp."""

    def __init__(self, room_c: float = 20.0) -> None:
        self.room_c = room_c
        self.time_s = 0.0
        self.tec_temp_c = room_c
        self.thermistor_temp_c = room_c
        self.pwm_now = 0.0
        self.heat_cool = 1

    def reset(self, room_c: float | None = None) -> None:
        """Return both thermal state variables to room temperature."""

        if room_c is not None:
            self.room_c = room_c
        self.time_s = 0.0
        self.tec_temp_c = self.room_c
        self.thermistor_temp_c = self.room_c
        self.pwm_now = 0.0
        self.heat_cool = 1

    def step(self, inputs: ModelInputs) -> ModelSample:
        """Advance the selected thermal model by one Euler time step."""

        dt = inputs.dt_s
        self.room_c = inputs.room_c

        if inputs.mode == "manual":
            self.pwm_now = pwm_count(inputs.manual_pwm)
            self.heat_cool = 1 if inputs.manual_heat_cool >= 0 else -1
            actuator = float(inputs.tec_power_on) * MANUAL_TEC_GAIN * self.pwm_now / 255.0 * self.heat_cool
            dtec_dt = inputs.heat_loss_h * (self.room_c - self.tec_temp_c) + actuator
            self.tec_temp_c += dt * dtec_dt

        elif inputs.mode == "proportional":
            error = inputs.setpoint_c - self.tec_temp_c
            self.pwm_now = round(min(inputs.kp * abs(error), 255.0))
            self.heat_cool = sign_nonzero(error)
            heat_loss = inputs.heat_loss_h * (self.room_c - self.tec_temp_c)
            actuator = float(inputs.tec_power_on) * self.pwm_now / 10.0 * self.heat_cool
            self.tec_temp_c += dt * (heat_loss + actuator)

        elif inputs.mode == "mass":
            error = inputs.setpoint_c - self.thermistor_temp_c
            self.pwm_now = round(min(inputs.kp * abs(error), 255.0))
            self.heat_cool = sign_nonzero(error)
            tec_heat_loss = inputs.heat_loss_h * (self.room_c - self.tec_temp_c)
            actuator = float(inputs.tec_power_on) * self.pwm_now * self.heat_cool
            self.tec_temp_c += dt * (tec_heat_loss + actuator)

            mass_term = inputs.mass_coupling * (self.tec_temp_c - self.thermistor_temp_c)
            mass_heat_loss = inputs.heat_loss_h * (self.room_c - self.thermistor_temp_c)
            self.thermistor_temp_c += dt * (mass_term + mass_heat_loss)

        else:
            raise ValueError(f"unknown mode: {inputs.mode}")

        if inputs.mode != "mass":
            self.thermistor_temp_c = self.tec_temp_c

        self.time_s += dt
        return ModelSample(
            time_s=self.time_s,
            tec_temp_c=self.tec_temp_c,
            thermistor_temp_c=self.thermistor_temp_c,
            signed_pwm=self.pwm_now * self.heat_cool,
            heat_cool=self.heat_cool,
        )


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def sign_nonzero(value: float) -> int:
    """MATLAB sign(0) would be 0; an H-bridge direction needs a side."""

    return 1 if value >= 0 else -1


def pwm_count(value: float) -> int:
    """Convert a slider value to an Arduino PWM integer count."""

    return int(clamp(value, 0.0, 255.0) + 0.5)


def set_temperature_axis_span(axis, values: list[float]) -> None:
    """Set temperature axis limits with a minimum displayed span."""

    if not values:
        return

    low = min(values)
    high = max(values)
    span = high - low

    if span < MIN_TEMPERATURE_DISPLAY_SPAN_C:
        half_span = MIN_TEMPERATURE_DISPLAY_SPAN_C / 2.0
        center = (low + high) / 2.0
        axis.set_ylim(center - half_span, center + half_span)
        return

    margin = span * 0.05
    axis.set_ylim(low - margin, high + margin)


def proportional_droop_temperature(inputs: ModelInputs) -> float | None:
    """Return the proportional-mode steady temperature before saturation."""

    if not inputs.tec_power_on:
        return inputs.room_c

    heat_loss = inputs.heat_loss_h
    controller_gain = inputs.kp / 10.0
    denominator = heat_loss + controller_gain

    if denominator <= 0.0:
        return None

    return (heat_loss * inputs.room_c + controller_gain * inputs.setpoint_c) / denominator


def manual_steady_temperature(inputs: ModelInputs) -> float | None:
    """Return the manual-mode steady temperature for fixed PWM and direction."""

    if inputs.heat_loss_h <= 0.0:
        return None

    direction = 1 if inputs.manual_heat_cool >= 0 else -1
    actuator = (
        float(inputs.tec_power_on)
        * MANUAL_TEC_GAIN
        * pwm_count(inputs.manual_pwm)
        / 255.0
        * direction
    )
    return inputs.room_c + actuator / inputs.heat_loss_h


def mass_mode_stability(inputs: ModelInputs) -> tuple[str, float, float]:
    """Return damping class, discriminant, and effective proportional gain."""

    effective_kp = inputs.kp if inputs.tec_power_on else 0.0
    alpha = inputs.mass_coupling + 2.0 * inputs.heat_loss_h
    beta = (
        inputs.heat_loss_h * (inputs.mass_coupling + inputs.heat_loss_h)
        + inputs.mass_coupling * effective_kp
    )
    mass_rate = inputs.mass_coupling
    discriminant = alpha * alpha - 4.0 * beta

    if mass_rate <= 0.0:
        return "no mass dynamics", discriminant, effective_kp
    if beta <= 0.0:
        return "no restoring term", discriminant, effective_kp
    if discriminant < -1e-9:
        return "underdamped", discriminant, effective_kp
    if discriminant > 1e-9:
        return "overdamped", discriminant, effective_kp
    return "critically damped", discriminant, effective_kp


def run_demo(output: Path) -> None:
    """Execute a repeatable proportional-with-mass simulation and save a plot."""

    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "phys39_matplotlib_cache"))

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    model = ModelingTECv2Model(room_c=20.0)
    inputs = ModelInputs(
        mode="mass",
        dt_s=0.01,
        room_c=20.0,
        tec_power_on=True,
        setpoint_c=25.0,
        kp=10.0,
        heat_loss_h=1.0,
        mass_coupling=3.0,
    )

    samples = [model.step(inputs) for _ in range(2000)]
    time_s = [s.time_s for s in samples]
    tec_temp = [s.tec_temp_c for s in samples]
    thermistor_temp = [s.thermistor_temp_c for s in samples]
    signed_pwm = [s.signed_pwm for s in samples]
    error_c = [inputs.setpoint_c - t for t in thermistor_temp]
    duration_s = len(samples) * inputs.dt_s

    fig, axes = plt.subplots(3, 1, figsize=(5, 8), sharex=True)
    axes[0].plot(time_s, tec_temp, label="TEC temperature")
    axes[0].plot(time_s, thermistor_temp, label="Thermistor/block temperature")
    axes[0].axhline(inputs.setpoint_c, color="black", linestyle="--", linewidth=1, label="setpoint")
    axes[0].set_ylabel("temperature (C)")
    axes[0].legend(loc="best")

    axes[1].plot(time_s, signed_pwm, color="purple")
    axes[1].axhline(0, color="black", linestyle="--", linewidth=0.9, alpha=0.7)
    axes[1].set_ylabel("signed PWM")

    axes[2].plot(time_s, error_c, color="darkgreen")
    axes[2].axhline(0, color="black", linestyle="--", linewidth=0.9, alpha=0.7)
    axes[2].set_ylabel("error (C)")
    axes[2].set_xlabel("time (s)")

    fig.suptitle("Python conversion of ModelingTECv2: proportional control with mass")
    fig.text(
        0.01,
        0.01,
        "Demo parameters:\n" + "\n".join(demo_parameter_lines(inputs, duration_s)),
        ha="left",
        va="bottom",
        fontsize=8.5,
        family="monospace",
    )
    fig.tight_layout(rect=(0, 0.12, 1, 0.96))
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    print(f"Saved demo plot: {output}")
    print("Demo parameters: " + demo_parameter_summary(inputs, duration_s))
    print(
        "Final state: "
        f"TEC={tec_temp[-1]:.1f} C, "
        f"thermistor={thermistor_temp[-1]:.1f} C, "
        f"signed PWM={signed_pwm[-1]:.0f}"
    )


def demo_parameter_summary(inputs: ModelInputs, duration_s: float) -> str:
    """Return the parameter values needed to reproduce the demo figure."""

    return "; ".join(demo_parameter_lines(inputs, duration_s))


def demo_parameter_lines(inputs: ModelInputs, duration_s: float) -> list[str]:
    """Return short parameter lines that fit under the saved demo figure."""

    return (
        [
            f"mode={inputs.mode}; duration={duration_s:.1f} s; dt={inputs.dt_s:g} s; TEC power={'on' if inputs.tec_power_on else 'off'}",
            f"T_room={inputs.room_c:.1f} C; T_set={inputs.setpoint_c:.1f} C; Kp={inputs.kp:.1f} PWM/C",
            f"heat_loss_h={inputs.heat_loss_h:.1f} 1/s; mass_coupling={inputs.mass_coupling:.1f} 1/s",
        ]
    )


def equation_display_lines(mode: str, inputs: ModelInputs) -> list[tuple[str, bool]]:
    """Return model-equation lines for Matplotlib mathtext rendering."""

    common = "HC is +1 heat or -1 cool. PWM_count is 0 to 255."
    if mode == "manual":
        steady_temp = manual_steady_temperature(inputs)
        prediction_line = "predicted T: no finite value when h = 0"
        if steady_temp is not None:
            prediction_line = rf"$T_{{\mathrm{{pred}}}}={steady_temp:.1f}^\circ\mathrm{{C}}$"
        return [
            ("Manual drive", False),
            (r"$C\,\frac{dT}{dt}=G_{\mathrm{room}}(T_{\mathrm{room}}-T)+Q_{\max}\left(\frac{\mathrm{PWM}_{\mathrm{count}}}{255}\right)\mathrm{HC}$", True),
            (r"$h=G_{\mathrm{room}}/C$", True),
            (rf"$\frac{{dT}}{{dt}}=h(T_{{\mathrm{{room}}}}-T)+P_{{\mathrm{{on}}}}\,{MANUAL_TEC_GAIN:g}\left(\frac{{\mathrm{{PWM}}_{{\mathrm{{count}}}}}}{{255}}\right)\mathrm{{HC}}$", True),
            ("Steady prediction", False),
            (rf"$T_{{\mathrm{{pred}}}}=T_{{\mathrm{{room}}}}+\frac{{P_{{\mathrm{{on}}}}\,{MANUAL_TEC_GAIN:g}\left(\mathrm{{PWM}}_{{\mathrm{{count}}}}/255\right)\mathrm{{HC}}}}{{h}}$", True),
            (prediction_line, steady_temp is not None),
            (common + " Manual mode has one temperature T; mass is not used.", False),
        ]

    if mode == "proportional":
        t_droop = proportional_droop_temperature(inputs)
        droop_lines: list[tuple[str, bool]] = []
        if t_droop is not None:
            droop_error = inputs.setpoint_c - t_droop
            droop_lines = [
                (rf"$T_{{\mathrm{{droop}}}}={t_droop:.1f}^\circ\mathrm{{C}}$", True),
                (rf"$T_{{\mathrm{{set}}}}-T_{{\mathrm{{droop}}}}={droop_error:.1f}^\circ\mathrm{{C}}$", True),
            ]
        return [
            ("Proportional control", False),
            (r"$\mathrm{error}=T_{\mathrm{set}}-T$", True),
            (r"$\mathrm{PWM}=\min(K_p\left|\mathrm{error}\right|,255)$", True),
            (r"$\mathrm{HC}=\mathrm{sign}(\mathrm{error})$", True),
            (r"$C\,\frac{dT}{dt}=G_{\mathrm{room}}(T_{\mathrm{room}}-T)+Q_{\max}\left(\frac{\mathrm{PWM}}{255}\right)\mathrm{HC}$", True),
            (r"$h=G_{\mathrm{room}}/C,\quad K_c=K_p/10$", True),
            (r"$\frac{dT}{dt}=h(T_{\mathrm{room}}-T)+K_c(T_{\mathrm{set}}-T)$", True),
            ("Steady prediction before saturation", False),
            (r"$T_{\mathrm{droop}}=\frac{hT_{\mathrm{room}}+K_cT_{\mathrm{set}}}{h+K_c}$", True),
            *droop_lines,
            (common + " Kp has units of PWM/C.", False),
        ]

    if mode == "mass":
        stability, discriminant, effective_kp = mass_mode_stability(inputs)
        return [
            ("Proportional control with measured thermal mass", False),
            (r"$\mathrm{error}=T_{\mathrm{set}}-T_m$", True),
            (r"$\mathrm{PWM}=\min(K_p\left|\mathrm{error}\right|,255)$", True),
            (r"$\frac{dT}{dt}=h(T_{\mathrm{room}}-T)+K_{p,\mathrm{eff}}(T_{\mathrm{set}}-T_m)$", True),
            (r"$\frac{dT_m}{dt}=m(T-T_m)+h(T_{\mathrm{room}}-T_m)$", True),
            (r"$\alpha=m+2h,\quad \beta=h(m+h)+mK_{p,\mathrm{eff}}$", True),
            (r"$s^2+\alpha s+\beta=0,\quad D=\alpha^2-4\beta$", True),
            (
                f"{stability}: Kp_eff={effective_kp:.1f}, D={discriminant:.1f}",
                False,
            ),
        ]

    return [("Unknown model.", False)]


class ModelingTECv2Gui:
    """Tkinter/Matplotlib desktop GUI that mirrors the old MATLAB app."""

    def __init__(self) -> None:
        os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "phys39_matplotlib_cache"))

        import tkinter as tk
        from tkinter import ttk

        import matplotlib

        matplotlib.use("TkAgg")
        matplotlib.rcParams["mathtext.fontset"] = "stix"
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        self.tk = tk
        self.ttk = ttk
        self.Figure = Figure
        self.FigureCanvasTkAgg = FigureCanvasTkAgg
        self.root = tk.Tk()
        self.root.title("ModelingTECv2 Python")
        self.model = ModelingTECv2Model(room_c=20.0)
        self.samples: list[ModelSample] = []
        self.running = False
        self.rounding_trace_active = False
        self.max_samples = 200

        self.mode = tk.StringVar(value="manual")
        self.tec_power = tk.BooleanVar(value=False)
        self.heat_cool = tk.StringVar(value="Heat")
        self.manual_pwm = tk.IntVar(value=0)
        self.setpoint = tk.DoubleVar(value=25.0)
        self.kp = tk.DoubleVar(value=10.0)
        self.heat_loss = tk.DoubleVar(value=1.0)
        self.mass_coupling = tk.DoubleVar(value=10.0)
        self.room_temp = tk.DoubleVar(value=20.0)

        self.tec_label = tk.StringVar(value="TEC temp (T): 20.0 C")
        self.thermistor_label = tk.StringVar(value="Thermistor temp (Tm): 20.0 C")
        self.pwm_label = tk.StringVar(value="PWM: 0")
        self.direction_label = tk.StringVar(value="Heat/Cool: Heat")

        outer = ttk.Frame(self.root, padding=8)
        outer.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        outer.columnconfigure(1, weight=1)
        outer.rowconfigure(0, weight=1)

        controls = ttk.Frame(outer, padding=8)
        controls.grid(row=0, column=0, sticky="ns")

        plots = ttk.Frame(outer)
        plots.grid(row=0, column=1, sticky="nsew")
        plots.columnconfigure(0, weight=1)
        plots.rowconfigure(0, weight=1)

        self._build_controls(controls)

        self.figure = self.Figure(figsize=(6.2, 3.5), dpi=100)
        self.ax_temp = None
        self.ax_mass = None
        self.ax_pwm = None
        self.figure.tight_layout()
        self.canvas = self.FigureCanvasTkAgg(self.figure, master=plots)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self._attach_variable_traces()
        self._redraw()

    def _build_controls(self, parent) -> None:
        ttk = self.ttk

        ttk.Button(parent, text="Run / Pause", command=self.toggle_running).grid(row=0, column=0, sticky="ew")
        ttk.Button(parent, text="Reset", command=self.reset).grid(row=0, column=1, sticky="ew")

        ttk.Checkbutton(parent, text="TEC power", variable=self.tec_power).grid(row=1, column=0, columnspan=2, sticky="w")

        ttk.Label(parent, text="Mode").grid(row=2, column=0, sticky="w")
        mode_box = ttk.Combobox(parent, textvariable=self.mode, values=["manual", "proportional", "mass"], state="readonly")
        mode_box.grid(row=2, column=1, sticky="ew")
        mode_box.bind("<<ComboboxSelected>>", lambda _event: self._redraw())

        ttk.Label(parent, text="Heat/Cool").grid(row=3, column=0, sticky="w")
        ttk.Combobox(parent, textvariable=self.heat_cool, values=["Heat", "Cool"], state="readonly").grid(
            row=3, column=1, sticky="ew"
        )

        self.manual_pwm_widgets = self._integer_slider(parent, "Manual PWM", self.manual_pwm, 0, 255, 4)
        self.setpoint_widgets = self._decimal_slider(parent, "Set temp (C)", self.setpoint, -20, 100, 5)
        self.kp_widgets = self._decimal_slider(parent, "Kp", self.kp, 0, 200, 6)
        self.heat_loss_widgets = self._decimal_slider(parent, "Heat loss h", self.heat_loss, 0, 2, 7)
        self.mass_widgets = self._decimal_slider(parent, "mass^-1", self.mass_coupling, 0, 10, 8)
        self.room_temp_widgets = self._decimal_slider(parent, "Room temp (C)", self.room_temp, 0, 40, 9)

        ttk.Separator(parent).grid(row=10, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Label(parent, text="Model equations").grid(row=11, column=0, columnspan=2, sticky="w")
        self._build_equation_canvas(parent, row=12)

        ttk.Separator(parent).grid(row=13, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Label(parent, textvariable=self.tec_label).grid(row=14, column=0, columnspan=2, sticky="w")
        ttk.Label(parent, textvariable=self.thermistor_label).grid(row=15, column=0, columnspan=2, sticky="w")
        ttk.Label(parent, textvariable=self.pwm_label).grid(row=16, column=0, columnspan=2, sticky="w")
        ttk.Label(parent, textvariable=self.direction_label).grid(row=17, column=0, columnspan=2, sticky="w")

    def _build_equation_canvas(self, parent, row: int) -> None:
        self.equation_figure = self.Figure(figsize=(3.3, 4.0), dpi=110)
        self.equation_figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.equation_axis = self.equation_figure.add_axes((0, 0, 1, 1))
        self.equation_axis.axis("off")
        self.equation_canvas = self.FigureCanvasTkAgg(self.equation_figure, master=parent)
        self.equation_canvas.get_tk_widget().grid(row=row, column=0, columnspan=2, sticky="ew")

    def _slider(self, parent, label: str, variable, low: float, high: float, row: int) -> None:
        ttk = self.ttk
        label_widget = ttk.Label(parent, text=label)
        label_widget.grid(row=row, column=0, sticky="w")
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=1, sticky="ew")
        frame.columnconfigure(0, weight=1)
        scale = ttk.Scale(frame, from_=low, to=high, variable=variable, orient="horizontal")
        scale.grid(row=0, column=0, sticky="ew")
        entry = ttk.Entry(frame, textvariable=variable, width=7)
        entry.grid(row=0, column=1, padx=(6, 0))
        return (label_widget, scale, entry)

    def _decimal_slider(self, parent, label: str, variable, low: float, high: float, row: int) -> None:
        ttk = self.ttk
        tk = self.tk
        label_widget = ttk.Label(parent, text=label)
        label_widget.grid(row=row, column=0, sticky="w")
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=1, sticky="ew")
        frame.columnconfigure(0, weight=1)
        scale = tk.Scale(
            frame,
            from_=low,
            to=high,
            variable=variable,
            orient="horizontal",
            resolution=0.1,
            showvalue=False,
            highlightthickness=0,
            digits=4,
        )
        scale.grid(row=0, column=0, sticky="ew")
        entry = ttk.Entry(frame, textvariable=variable, width=7)
        entry.grid(row=0, column=1, padx=(6, 0))
        return (label_widget, scale, entry)

    def _integer_slider(self, parent, label: str, variable, low: int, high: int, row: int) -> None:
        ttk = self.ttk
        tk = self.tk
        label_widget = ttk.Label(parent, text=label)
        label_widget.grid(row=row, column=0, sticky="w")
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=1, sticky="ew")
        frame.columnconfigure(0, weight=1)
        scale = tk.Scale(
            frame,
            from_=low,
            to=high,
            variable=variable,
            orient="horizontal",
            resolution=1,
            showvalue=False,
            highlightthickness=0,
        )
        scale.grid(row=0, column=0, sticky="ew")
        entry = ttk.Entry(frame, textvariable=variable, width=7)
        entry.grid(row=0, column=1, padx=(6, 0))
        return (label_widget, scale, entry)

    def read_inputs(self) -> ModelInputs:
        return ModelInputs(
            mode=self.mode.get(),
            room_c=round(float(self.room_temp.get()), 1),
            tec_power_on=bool(self.tec_power.get()),
            manual_pwm=float(self.manual_pwm.get()),
            manual_heat_cool=1 if self.heat_cool.get() == "Heat" else -1,
            setpoint_c=round(float(self.setpoint.get()), 1),
            kp=round(float(self.kp.get()), 1),
            heat_loss_h=round(float(self.heat_loss.get()), 1),
            mass_coupling=round(float(self.mass_coupling.get()), 1),
        )

    def toggle_running(self) -> None:
        self.running = not self.running
        if self.running:
            if not self.samples:
                self.samples.append(self._initial_sample())
            self._tick()

    def reset(self) -> None:
        self.model.reset(room_c=round(float(self.room_temp.get()), 1))
        self.samples.clear()
        self._redraw()

    def _tick(self) -> None:
        if not self.running:
            return
        sample = self.model.step(self.read_inputs())
        self.samples.append(sample)
        self.samples = self.samples[-self.max_samples :]
        self._redraw()
        self.root.after(10, self._tick)

    def _redraw(self) -> None:
        mode = self.mode.get()
        self._update_control_states(mode)
        samples = self.samples or [self._initial_sample()]
        time_s = [s.time_s for s in samples]
        tec_temp = [s.tec_temp_c for s in samples]
        mass_temp = [s.thermistor_temp_c for s in samples]
        signed_pwm = [s.signed_pwm for s in samples]

        self.figure.clear()
        if mode == "mass":
            self.ax_temp, self.ax_mass, self.ax_pwm = self.figure.subplots(3, 1, sharex=True)
        else:
            self.ax_temp, self.ax_pwm = self.figure.subplots(2, 1, sharex=True)
            self.ax_mass = None

        self.ax_temp.clear()
        self.ax_temp.plot(time_s, tec_temp, color="tab:red")
        temp_axis_values = list(tec_temp)
        if mode == "proportional":
            t_droop = proportional_droop_temperature(self.read_inputs())
            if t_droop is not None:
                temp_axis_values.append(t_droop)
                self.ax_temp.axhline(
                    t_droop,
                    color="tab:green",
                    linestyle="--",
                    linewidth=1.2,
                    label=f"T_droop = {t_droop:.1f} C",
                )
                self.ax_temp.legend(loc="best")
        self.ax_temp.set_title("TEC temperature (C)" if mode == "mass" else "Temperature T (C)")
        self.ax_temp.set_ylabel("T")
        set_temperature_axis_span(self.ax_temp, temp_axis_values)
        self.ax_temp.grid(True, alpha=0.25)

        if self.ax_mass is not None:
            self.ax_mass.clear()
            self.ax_mass.plot(time_s, mass_temp, color="tab:blue", label="thermistor/block")
            if mode == "mass":
                self.ax_mass.plot(time_s, tec_temp, color="tab:red", alpha=0.55, label="TEC")
                self.ax_mass.legend(loc="best")
            self.ax_mass.set_title("Thermistor temperature (C)")
            self.ax_mass.set_ylabel("Tm")
            set_temperature_axis_span(self.ax_mass, mass_temp + tec_temp)
            self.ax_mass.grid(True, alpha=0.25)

        self.ax_pwm.clear()
        self.ax_pwm.plot(time_s, signed_pwm, color="purple")
        self.ax_pwm.axhline(0, color="black", linestyle="--", linewidth=0.9, alpha=0.7)
        self.ax_pwm.set_title("PWM")
        self.ax_pwm.set_ylabel("signed PWM")
        self.ax_pwm.set_xlabel("time (s)")
        self.ax_pwm.grid(True, alpha=0.25)

        latest = samples[-1]
        if mode == "mass":
            self.tec_label.set(f"TEC temp (T): {latest.tec_temp_c:.1f} C")
            self.thermistor_label.set(f"Thermistor temp (Tm): {latest.thermistor_temp_c:.1f} C")
        else:
            self.tec_label.set(f"Temperature (T): {latest.tec_temp_c:.1f} C")
            self.thermistor_label.set("")
        self.pwm_label.set(f"PWM: {abs(latest.signed_pwm):.0f}")
        self.direction_label.set("Heat/Cool: Heat" if latest.heat_cool >= 0 else "Heat/Cool: Cool")
        self._draw_equations(mode, self.read_inputs())

        self.figure.tight_layout()
        self.canvas.draw_idle()

    def _draw_equations(self, mode: str, inputs: ModelInputs) -> None:
        self.equation_axis.clear()
        self.equation_axis.axis("off")
        self.equation_axis.set_xlim(0, 1)
        self.equation_axis.set_ylim(0, 1)

        figure_height_inches = self.equation_figure.get_size_inches()[1]

        def points_to_axis_y(points: float) -> float:
            return points / (72.0 * figure_height_inches)

        y = 1.0 - points_to_axis_y(EQUATION_TOP_PADDING_POINTS)
        for text, is_math in equation_display_lines(mode, inputs):
            if text == "":
                y -= points_to_axis_y(EQUATION_BLANK_LINE_SPACING_POINTS)
                continue
            display_lines = [text] if is_math else textwrap.wrap(text, width=56)
            for display_text in display_lines:
                self.equation_axis.text(
                    0.0,
                    y,
                    display_text,
                    transform=self.equation_axis.transAxes,
                    va="top",
                    ha="left",
                    fontsize=12.0 if is_math else 8.2,
                    fontfamily="STIXGeneral" if is_math else "DejaVu Sans",
                )
                if is_math:
                    spacing_points = (
                        EQUATION_FRACTION_LINE_SPACING_POINTS
                        if r"\frac" in display_text
                        else EQUATION_MATH_LINE_SPACING_POINTS
                    )
                else:
                    spacing_points = EQUATION_TEXT_LINE_SPACING_POINTS
                y -= points_to_axis_y(spacing_points)

        self.equation_canvas.draw_idle()

    def _initial_sample(self) -> ModelSample:
        """Current initial condition, plotted at room temperature before stepping."""

        return ModelSample(
            time_s=0.0,
            tec_temp_c=self.model.tec_temp_c,
            thermistor_temp_c=self.model.thermistor_temp_c,
            signed_pwm=0.0,
            heat_cool=self.model.heat_cool,
        )

    def run(self) -> None:
        self.root.mainloop()

    def _attach_variable_traces(self) -> None:
        """Redraw derived guide lines when a slider or switch changes."""

        for variable in (
            self.mode,
            self.tec_power,
            self.heat_cool,
            self.manual_pwm,
        ):
            variable.trace_add("write", lambda *_args: self._redraw())
        for variable in (self.setpoint, self.kp, self.heat_loss, self.mass_coupling, self.room_temp):
            variable.trace_add("write", lambda *_args, var=variable: self._rounded_redraw(var, 1))

    def _rounded_redraw(self, variable, decimals: int) -> None:
        """Keep selected student-facing controls at a fixed displayed precision."""

        if self.rounding_trace_active:
            return

        try:
            raw_value = float(variable.get())
        except (ValueError, self.tk.TclError):
            return

        value = round(raw_value, decimals)
        if raw_value != value:
            self.rounding_trace_active = True
            try:
                variable.set(value)
            finally:
                self.rounding_trace_active = False
        self._redraw()

    def _update_control_states(self, mode: str) -> None:
        """Disable sliders that are not part of the selected model."""

        self._set_widgets_enabled(self.manual_pwm_widgets, mode == "manual")
        self._set_widgets_enabled(self.setpoint_widgets, mode in {"proportional", "mass"})
        self._set_widgets_enabled(self.kp_widgets, mode in {"proportional", "mass"})
        self._set_widgets_enabled(self.mass_widgets, mode == "mass")

    def _set_widgets_enabled(self, widgets, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for widget in widgets:
            widget.configure(state=state)


def equations_for_mode(mode: str, inputs: ModelInputs | None = None) -> str:
    """Return the compact equations shown in the GUI for each model."""

    common = "HC is +1 heat or -1 cool. PWM_count is an integer Arduino count from 0 to 255."
    if mode == "manual":
        steady_temp = manual_steady_temperature(inputs) if inputs is not None else None
        prediction_line = "current predicted T = no finite steady value when h = 0\n"
        if steady_temp is not None:
            prediction_line = f"current predicted T = {steady_temp:.1f} C\n"
        return (
            "Manual drive\n"
            "C dT/dt = G_room*(T_room - T) + Q_max*(PWM_count/255)*HC\n"
            "h = G_room/C\n"
            f"In this app: dT/dt = h*(T_room - T) + P_on*{MANUAL_TEC_GAIN:g}*(PWM_count/255)*HC\n\n"
            "Steady prediction:\n"
            f"T_pred = T_room + P_on*{MANUAL_TEC_GAIN:g}*(PWM_count/255)*HC/h\n"
            f"{prediction_line}\n"
            f"{common} Manual mode has one temperature T; mass is not used."
        )
    if mode == "proportional":
        t_droop = proportional_droop_temperature(inputs) if inputs is not None else None
        droop_line = ""
        if t_droop is not None:
            droop_error = inputs.setpoint_c - t_droop
            droop_line = (
                f"predicted T_droop = {t_droop:.1f} C\n"
                f"predicted droop error = T_set - T_droop = {droop_error:.1f} C\n"
            )
        return (
            "Proportional control\n"
            "error = T_set - T\n"
            "PWM = min(Kp*abs(error), 255)\n"
            "HC = sign(error)\n"
            "C dT/dt = G_room*(T_room - T) + Q_max*(PWM/255)*HC\n"
            "h = G_room/C\n"
            "Kc = Kp/10\n"
            "In this app: dT/dt = h*(T_room - T) + Kc*(T_set - T)\n"
            "Steady prediction before saturation:\n"
            "T_droop = (h*T_room + Kc*T_set)/(h + Kc)\n"
            f"{droop_line}\n"
            f"{common} Kp has units of PWM/C."
        )
    if mode == "mass":
        stability = ""
        if inputs is not None:
            damping, discriminant, effective_kp = mass_mode_stability(inputs)
            stability = f"D = {discriminant:.1f}; {damping}; Kp_eff = {effective_kp:.1f}\n"
        return (
            "Proportional control with measured thermal mass\n"
            "error = T_set - Tm\n"
            "PWM = min(Kp*abs(error), 255)\n"
            "HC = sign(error)\n"
            "dT/dt = h*(T_room - T) + Kp_eff*(T_set - Tm)\n"
            "dTm/dt = m*(T - Tm) + h*(T_room - Tm)\n"
            "alpha = m + 2*h; beta = h*(m + h) + m*Kp_eff\n"
            "s^2 + alpha*s + beta = 0\n"
            "D = alpha^2 - 4*beta\n"
            f"{stability}\n"
            f"{common} m is the mass^-1 slider."
        )
    return "Unknown model."


def main() -> None:
    parser = argparse.ArgumentParser(description="Python conversion of ModelingTECv2.mlapp")
    parser.add_argument("--demo", action="store_true", help="run a non-interactive simulation and save a PNG")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("python/Lab_6_7_modeling_tec_v2_demo.png"),
        help="demo plot output path",
    )
    args = parser.parse_args()

    if args.demo:
        run_demo(args.output)
    else:
        ModelingTECv2Gui().run()


if __name__ == "__main__":
    main()
