# Module 5 Assignment: P-Only Temperature Control

## Module At A Glance

Module 4 measured the TEC response to manually chosen commands. Module 5 closes
the feedback loop: Python calculates the proportional control demand

\[
e=T_{\mathrm{set}}-T, \qquad u=K_p e.
\]

The sign of $u$ selects heat or cool; its magnitude becomes the nonnegative
8-bit PWM value sent to the Arduino. The Arduino applies the command and retains
independent shutdown authority. During S9-S10 you will verify the feedback sign,
measure droop versus gain, explore high-gain behavior, and compare the data with
a simple model. PI control follows in Module 6.

## Optional Background Sources

These are optional; Laplace transforms are not required in Module 5:

- [Module 6](../lab-06/index.md): [droop](../lab-06/index.md#part-1-algebraic-droop-model)
  and [first-order stability](../lab-06/index.md#part-6-why-the-first-order-model-may-not-oscillate)
- Bechhoefer, [*Feedback for Physicists*](../../references/bechhoefer-feedback-for-physicists-2005.pdf),
  pp. 788-790 and 804-805
- [Wikipedia: PID controller](https://en.wikipedia.org/wiki/PID_controller)
- [NI: PID theory explained](https://www.ni.com/en/shop/labview/pid-theory-explained.html)

## Safety Boundary

Before using feedback control:

1. The Module 4 software temperature limit is present.
2. PWM starts at zero.
3. The Python GUI shows plausible temperature.
4. Heat and cool directions have the correct sign.
5. The power supply current limit is set by the instructor.
6. The setpoint is between **20 °C and 35 °C** unless the instructor approves a
   different range.

Stop immediately if the temperature moves in the wrong direction, the GUI
freezes, the PWM saturates unexpectedly, or sustained oscillations grow in
amplitude.

## Vocabulary

| Quantity | Meaning | Units |
| --- | --- | --- |
| $T_{\mathrm{set}}$ | Desired temperature | °C |
| $e=T_{\mathrm{set}}-T$ | Temperature error; steady nonzero error is **droop** | °C |
| $u=K_p e$ | Signed control demand calculated by Python | PWM counts |
| $P=|u|$ | Nonnegative Arduino PWM magnitude, limited to 0-255 | PWM counts |
| $K_p$ | Proportional gain | PWM counts/°C |

**Saturation** occurs when the requested PWM exceeds its allowed range.
**Instability** means the response oscillates or diverges instead of settling.

## Before Class

1. From Module 4, identify the appropriate temperature susceptibility
   \(\chi_T=dT/d(\mathrm{PWM})\) near room temperature.
2. Confirm that your Arduino safety shutdown still works.
3. Choose a preliminary setpoint and calculate
   \(e_0=T_{\mathrm{set}}-T_{\mathrm{amb}}\).
4. Record the convention: positive $u$ selects heat, negative $u$ selects
   cool, and the Arduino receives $P=|u|$ as PWM magnitude.

## Outside-Class Workload Budget

| Session | Required outside work | Total |
| --- | --- | ---: |
| S9 | Read the assignment; answer the questions; review Module 4; prepare the controller and gain range | **2 hours 15 minutes** |
| S10 | Prepare the data plan; analyze and label evidence; update the note; commit and push | **2 hours 30 minutes** |

Optional background reading is not included in the required workload budget.

## Pre-Class Questions

1. If \(T_{\mathrm{set}}=30\ ^\circ\mathrm{C}\) and
   \(T=25\ ^\circ\mathrm{C}\), should the TEC heat or cool?
2. If $u$ is measured in PWM counts and $e$ is measured in °C, what are the
   units of $K_p$?
3. Why does proportional control require a nonzero error to produce a nonzero
   output?
4. What experimental symptoms might indicate that $K_p$ is too large?

## Part 1: Draw The Feedback Loop

Draw a block diagram with these pieces:

```text
Tset -> error e -> P controller -> signed demand u -> direction + PWM magnitude
  ^                                                                  |
  |                                                                  v
  +---------------- thermistor <- TEC/block <- H-bridge -------------+
```

Label $T_{\mathrm{set}}$, $T$, $e=T_{\mathrm{set}}-T$, $u=K_p e$,
$P=|u|$, the heat/cool direction, and the physical system.

## Part 2: Implement P-Only Control

Add a P-only mode to your Python GUI. Python calculates the control demand and
sends direction and PWM magnitude to the Arduino. The Arduino continues to
measure temperature, parse commands, drive the H-bridge, and enforce the
independent software temperature limit developed in Module 4.

The controller should:

1. read the measured temperature only after averaging between 100 and 1000 raw
   thermistor-voltage measurements and converting the average voltage to
   temperature,
2. calculate $e=T_{\mathrm{set}}-T$,
3. calculate $u=K_p e$,
4. convert the sign of $u$ into heat/cool direction,
5. convert $P=|u|$ into an integer PWM magnitude,
6. clamp $P$ to the range 0 to 255,
7. send direction and PWM magnitude to the Arduino,
8. keep plotting temperature, PWM, direction, setpoint, and error.

Start with a very small gain. Do not tune aggressively at first.

## Part 3: Sign Test At Low Gain

Before trying to regulate temperature:

1. Choose a setpoint slightly above room temperature.
2. Use a very small $K_p$.
3. Confirm that positive error produces heating.
4. Choose a setpoint slightly below room temperature.
5. Confirm that negative error produces cooling.

If the sign is wrong, stop and fix the sign convention before continuing.

## Part 4: Measure Droop Versus Gain

Choose one setpoint, for example **30 °C**, and use the corresponding Module 4
temperature susceptibility to select your own gain range. First estimate the
PWM magnitude required to produce the desired open-loop temperature change:

\[
P_{\mathrm{required}}\approx
\frac{|T_{\mathrm{set}}-T_{\mathrm{amb}}|}{|\chi_T|}.
\]

For every candidate gain, predict the initial control demand:

\[
P_0=K_p|e_0|,
\qquad e_0=T_{\mathrm{set}}-T_{\mathrm{amb}}.
\]

Select a sequence that starts with $P_0$ well below
$P_{\mathrm{required}}$ and progresses toward values comparable to or larger
than $P_{\mathrm{required}}$, without beginning outside the 0-to-255 PWM
range. Record your reasoning and have the instructor approve the range before
running it.

Use a table like this:

| $K_p$ (PWM/°C) | Predicted $P_0$ | Setpoint (°C) | Final Temperature (°C) | Droop (°C) | Final PWM | Notes |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
|  |  |  |  |  |  |  |

For each gain:

1. Start from PWM `0`.
2. Turn on P-only control.
3. Wait for the temperature to settle or clearly fail to settle.
4. Record final temperature, error, and PWM.
5. Save a strip chart trace.

Plot droop versus $K_p$.

## Part 5: Predict Droop From Module 4

For a heating setpoint above room temperature, use the heating susceptibility
$\chi_{T,h}>0$ measured in Module 4:

\[
T=T_{\mathrm{amb}}+\chi_{T,h}P,
\qquad
P=K_p(T_{\mathrm{set}}-T).
\]

Combining the equations predicts the steady-state droop:

\[
T_{\mathrm{set}}-T=
\frac{T_{\mathrm{set}}-T_{\mathrm{amb}}}
{1+\chi_{T,h}K_p}.
\]

The product in the denominator is dimensionless:

\[
[\chi_{T,h}K_p]
=\frac{^\circ\mathrm C}{\text{PWM count}}
\frac{\text{PWM count}}{^\circ\mathrm C}=1.
\]

If you instead select a cooling setpoint, use the magnitude of the cooling
susceptibility and the magnitude of the cooling error in the analogous model.
Calculate the predicted droop for each tested gain and overlay predicted and
measured droop on the same graph.

This model will not be perfect. Its job is to explain the main trend.

## Part 6: Explore The High-Gain Response

Continue through your instructor-approved gain range. Do not assume that the
apparatus must oscillate. For every retained gain, record the setpoint, mean or
steady temperature, response shape, PWM behavior, and whether PWM saturates.

If sustained oscillations appear, measure their amplitude, period, and
frequency. State how you define amplitude. If they do not appear within the
safe range, report the highest gain tested and describe how that response
differs from the low-gain response.

| $K_p$ (PWM/°C) | Settles? | Mean Temperature (°C) | Amplitude (°C) | Period (s) | Frequency (Hz) | Saturation? |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
|  |  |  |  |  |  |  |

Do not let oscillations grow without supervision. Stop control and set PWM to
zero if the run becomes unsafe.

## Part 7: Interpret And Preserve The Results

### Thermal Capacity And The One-Lump Model

To describe time dependence, first treat the TEC, block, and thermistor as one
object at one uniform temperature $T$. Its thermal capacity is

$$
C=\frac{dU}{dT}\approx mc_p,
$$

where $U$ is stored thermal energy. The units of $C$ are J/°C (equivalently
J/K): it is the energy needed to raise the lump's temperature by one degree.
The simplest energy balance is

$$
C\frac{dT}{dt}=P_u u-H(T-T_{\mathrm{amb}}).
$$

The left side is the rate of stored-energy change. The first term on the right
is TEC heating or cooling, where $P_u$ has units W/PWM count, and the second is
heat transfer to the room, where $H$ has units W/°C. Every term has units of
watts. The model assumes one uniform temperature, linear heat loss,
instantaneous measurement and actuation, and no saturation.

### First-Order Expectation

The algebraic model predicts droop but says nothing about time dependence. For
the one-lump model developed fully in [Module 6](../lab-06/index.md), define
$\theta=T-T_{\mathrm{eq}}$. Under P-only control its deviation from equilibrium
obeys

$$
\frac{d\theta}{dt}=-\frac{\theta}{\tau_{\mathrm{cl}}},
$$

with solution

$$
\theta(t)=\theta(0)e^{-t/\tau_{\mathrm{cl}}}.
$$

This response approaches equilibrium exponentially and cannot sustain an
oscillation. If the apparatus oscillates, the one-lump model is missing
important physics or implementation details. Discuss plausible causes such as
thermal delay between the TEC and thermistor, another thermal mass, discrete
sampling, sensor noise, or PWM saturation.

### Evidence For A3 And C4

Module 5 requires no separate paper. Its results support the later
[`A3` feedback-and-model memo](../lab-06/index.md#a3-feedback-data-and-lumped-model-memo)
and the C4 demonstration. During S9-S10, preserve:

- the feedback-loop diagram and low-gain sign test,
- the chosen gain range and the calculation used to justify it,
- dimensional droop and high-gain response tables,
- measured and predicted droop on one graph,
- representative low- and high-gain strip-chart traces,
- the exact Python controller, Arduino sketch, and raw-data filenames, and
- a brief explanation of droop and of why oscillations did or did not appear.

Keep the note in `docs/module_notes/module_05_p_control.md`, data in
`data/module_05/`, and figures in `docs/figures/module_05/`. Calculate droop and
any oscillation quantities in class. Reserve about **90 minutes** afterward for
analysis, captions, and the Git checkpoint.

### GitHub Checkpoint

```bash
git status
git add README.md arduino python docs data
git commit -m "Measure P-only temperature control"
git push
```

Before Module 6, confirm that all listed evidence is present in the pushed
repository and that it is clear which code and data produced each figure.
