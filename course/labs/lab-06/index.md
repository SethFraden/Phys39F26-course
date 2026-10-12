# Module 6, Part I: P/PI Control And Lumped Modeling

Module 6 has two linked parts:

1. **Part I (this page):** develop one-lump P and PI models and connect them to
   the Module 4 and Module 5 measurements.
2. [**Part II: TEC Process Model And Simulation**](../lab-07/index.md):
   extend the model, compare one- and two-lump descriptions, and test the model
   with the same prepared simulation.

## Purpose

Module 5 showed that proportional feedback reduces steady-state error but can
overshoot, ring, and oscillate. Module 6 develops the theory needed to
distinguish what a one-lump model explains from behavior that requires
additional thermal dynamics.

The goal is to connect thermal physics, feedback equations, and the data you measured from the TEC.

You will begin with algebra, then simulate the one-lump model in time, then
extend the model just enough to understand why integral control is useful and
why real feedback loops can oscillate.

## Learning Objectives

By the end of Module 6, Part I, you should be able to:

- derive and interpret the one-lump energy balance, open-loop susceptibility,
  thermal time constant, and P-control droop;
- use the prepared simulation to compare open-loop, P, and PI control;
- connect the model parameters and predictions to measured values of
  susceptibility, time constant, droop, and transient response;
- explain why the one-lump P-control model can predict steady-state droop yet
  cannot reproduce measured high-gain overshoot;
- explain qualitatively how internal thermal storage and transport create
  phase lag and motivate a two-lump model;
- implement PI control on the physical TEC, including integral reset and
  anti-windup;
- generate six experimental Goldilocks plots that show low-, medium-, and
  high-gain P and PI behavior, then use them to connect controller settings to
  droop, rise time, overshoot, and oscillation.

The Goldilocks plots are the principal way you achieve these objectives. They
are assessed through the physical six-run study, the six matched simulation
plots in Part II, and A3 Questions 1–5.

## Reading

Read selectively:

1. Lienhard and Lienhard, [*A Heat Transfer Textbook*](https://ahtt.mit.edu/).

    - Section 1.3: read for energy-balance language and units.
    - Chapter 4, especially Section 4.5: read for transient response and thermal
      time constants.

2. Review your Module 4 and Module 5 data.
3. Optional after class: [Bechhoefer, *Feedback for Physicists*,
   pp. 795-797](../../references/bechhoefer-feedback-for-physicists-2005.pdf),
   on feedback and stability.

Do not try to learn all of transient heat transfer at once. For this module, you
need the idea that a physical object has heat capacity, exchanges heat with its
environment, and responds over a time scale.

## Vocabulary

### Terms

- **Thermal capacitance (thermal mass):** energy required to raise the lump's
  temperature by one degree. In this module, *thermal mass* is an informal
  synonym for thermal capacitance.
- **Thermal resistance:** opposition to passive heat flow between the lump and
  its surroundings.
- **Heat-loss conductance:** the inverse of thermal resistance; passive heat
  transfer per degree of temperature difference.
- **Time constant:** characteristic decay time. A first-order system has one
  time constant; a higher-order system can have more than one decay time.
- **Open-loop temperature susceptibility:** steady-state temperature change per
  applied PWM command, with direction held fixed.
- **P control:** command proportional to the current temperature error.
- **PI control:** command equal to the sum of a proportional term and a term
  proportional to accumulated temperature error.
- **Windup:** continued growth of the integral term while the actuator is
  saturated.
- **Anti-windup:** a software rule that prevents or reverses inappropriate
  growth of the integral term while the actuator is saturated.
- **Droop:** nonzero steady-state temperature error in P-only control.

### Symbols Used In Module 6, Part I

A temperature difference has the same numerical value in K and °C. Earlier
modules wrote the generic open-loop susceptibility as $\chi_{T,u}$. For
concision, this module writes it as $\chi$ and uses $\chi_h$ and $\chi_c$ when
the heating and cooling values must be distinguished. Similarly, $P_u$ means
the coefficient for the active direction; $P_{u,h}$ and $P_{u,c}$ distinguish
heating from cooling.

| Symbol | Meaning | Units |
| --- | --- | --- |
| $C$ | Thermal capacitance of one lump | J/K or J/°C |
| $T$ | Lump temperature | °C |
| $t$ | Time | s |
| $dT/dt$ | Rate of temperature change | K/s or °C/s |
| $P_u$ | Effective TEC thermal-power coefficient per signed PWM count | W/PWM count |
| $u$ | Signed PWM command: positive heats and negative cools | PWM counts |
| $H$ | Passive heat-loss conductance to the surroundings | W/K or W/°C |
| $T_{\mathrm{amb}}$ | Ambient (room) temperature | °C |
| $U$ | Thermal energy stored in the lump | J |
| $\dot Q_{\mathrm{in}}$ | Rate at which heat enters the lump | W |
| $\dot Q_{\mathrm{out}}$ | Rate at which heat leaves the lump | W |
| $m$ | Mass of the lump | kg |
| $c_p$ | Specific heat capacity of the lump material | J/(kg K) |
| $\chi$ | Open-loop temperature susceptibility for the active direction | °C/PWM count |
| $\chi_h$, $\chi_c$ | Heating and cooling susceptibilities | °C/PWM count |
| $r=\chi_h/\chi_c$ | Ratio of heating to cooling susceptibility | dimensionless |
| $\tau=C/H$ | Open-loop thermal time constant | s |
| $K_p$ | Proportional gain | PWM counts/°C |
| $K_i$ | Integral gain | PWM counts/(°C s) |
| $T_{\mathrm{set}}$ | Requested temperature setpoint | °C |
| $e=T_{\mathrm{set}}-T$ | Temperature error | °C |
| $q=\int e\,dt$ | Accumulated temperature error | °C s |
| $u_P=K_pe$, $u_I=K_iq$ | Proportional and integral contributions to the PWM command | PWM counts |
| $\mathrm{droop}=T_{\mathrm{set}}-T_{\mathrm{ss}}$ | Steady-state temperature error | °C |
| $\theta$, $z$ | Temperature and integral-state displacements from steady state | °C, °C s |
| $\lambda$ | Eigenvalue governing exponential growth or decay | 1/s |
| $\zeta$ | PI damping ratio | dimensionless |
| $T_m$ | Temperature of the measured block in the two-lump model | °C |

In this module, a **command** means setting the controller output $u$, which is
the signed PWM value, to a particular value. For example, a command of
$+25$ PWM means set $u=+25$ PWM.

## Before Class

Review your Module 4 and Module 5 results. Before class, make sure you can
locate and open these existing files on your laptop:

- Module 4 steady-state temperature versus PWM data,
- Module 5 droop-versus-gain data,
- one Module 5 strip-chart trace at a stable gain,
- one Module 5 high-gain strip-chart trace showing overshoot or ringing; if no
  overshoot was safely observed, bring the highest-gain trace, and
- your current Python plotting or modeling environment.

Do not create new figures, tables, or written work for this section. The files
will be used during the in-class model comparison.

## Outside-Class Workload Budget

| Session | Work | Planned time |
| --- | --- | ---: |
| S12 | Read the selected material and complete the one-lump derivation | 150 minutes |
| S12 | **Total associated with S12** | **2 hours 30 minutes** |
| S13 | Explore open-loop, P, and PI behavior in the simulation and prepare the physical controller | 120 minutes |
| S13 | **Total associated with S13** | **2 hours** |
| S14 | Complete the six-run experimental Goldilocks study | 150 minutes |
| S14 | Organize plots and begin A3 | 90 minutes |
| S14 | **Total associated with S14** | **4 hours** |

Do not add optional reading until the required derivation and A3 evidence are
complete and understood.

## Pre-Class Questions

1. What physical part of the apparatus stores heat?
2. What physical paths let heat leave the measured block?
3. What evidence from your data suggests a thermal time constant?
4. Why does the algebraic droop model not predict oscillation?

## Part I Roadmap

1. Derive the one-lump steady-state droop and transient response using the
   susceptibility and time constant measured earlier.
2. Compare open-loop and P-control predictions with experiment.
3. Use the model's failure at high gain to motivate thermal phase lag and a
   qualitative two-lump description.
4. Explore PI control in simulation, then implement integral action and
   anti-windup on the physical TEC.
5. Generate the six experimental Goldilocks plots that anchor the comparison
   with simulation and the A3 analysis.

## Part 1: Algebraic Droop Model

The dimensional one-lump model is

\[
C\frac{dT}{dt}=P_u u-H(T-T_{\mathrm{amb}}).
\]

This is the one-lump heat balance written in terms of the lump's temperature.
It follows from the more general First Law in rate form. The change of energy in time is equal to the rate of heat into the lump minus the rate of heat out:

\[
\frac{dU}{dt}=\dot Q_{\mathrm{in}}-\dot Q_{\mathrm{out}}.
\]

If the lump has constant thermal capacitance \(C\), then \(dU=C\,dT\), so

\[
\frac{dU}{dt}=C\frac{dT}{dt}.
\]

Each of the three terms in the one-lump model therefore has units of power:

**1. Energy storage**

\[
C\frac{dT}{dt}.
\]

The thermal capacitance \(C=mc_p\) has units J/K, and \(dT/dt\) has units
K/s or °C/s. Their product has units J/s = W. A positive value means the
lump is warming; a negative value means it is cooling.

**2. TEC heating or cooling**

\[
P_u u.
\]

The signed PWM command \(u\) is positive for heating and negative for
cooling. The effective TEC coefficient \(P_u\) has units W/PWM, so
\(P_u u\) has units W. This term treats the rapidly switched PWM drive as
an average thermal power.

**3. Heat transfer to the surroundings**

\[
-H(T-T_{\mathrm{amb}}).
\]

The total heat-loss conductance \(H\) has units W/K, while
\(T-T_{\mathrm{amb}}\) is a temperature difference in K or °C. Their
product has units W. If \(T>T_{\mathrm{amb}}\), this term is negative and
the lump loses heat. If \(T<T_{\mathrm{amb}}\), the term is positive: the
room transfers heat into the colder lump.

The algebraic droop model below is the steady-state limit of this energy
balance, where \(dT/dt=0\).

### Guided Derivation And Numerical Check

The measured Module 4 open-loop relationship is

\[
T=T_{\mathrm{amb}}+\chi u,
\]

where $\chi=dT/du$ is the open-loop susceptibility with respect to signed
PWM. With the signed convention, $\chi$ is positive: positive $u$ heats
and raises $T$, while negative $u$ cools and lowers $T$. P-only feedback supplies

\[
u=K_p(T_{\mathrm{set}}-T).
\]

Substitute the controller law into the measured open-loop relationship:

\[
T=T_{\mathrm{amb}}+\chi K_p(T_{\mathrm{set}}-T).
\]

At steady state, collect the terms containing $T$:

\[
(1+\chi K_p)T
=T_{\mathrm{amb}}+\chi K_pT_{\mathrm{set}}.
\]

Subtract this result from $T_{\mathrm{set}}$ to obtain the droop:

\[
\boxed{
T_{\mathrm{set}}-T=
\frac{T_{\mathrm{set}}-T_{\mathrm{amb}}}{1+\chi K_p}.
}
\]

The product $L=\chi K_p$ is dimensionless. It is the loop gain for this
steady-state model. Part 2 derives $\chi=P_u/H$ from the dimensional
model.

Using one of your Module 5 runs, use $\chi$, $T_{\mathrm{amb}}$,
$T_{\mathrm{set}}$, and $K_p$ in the boxed equation to calculate the predicted
settled temperature and droop. Compare the prediction with the measured Module
5 droop, then state one physical reason they may differ.

## Part 2: Express The One-Lump Model Using Measured Parameters

Continue with the dimensional one-lump energy balance from Part 1:

\[
C\frac{dT}{dt}=P_u u-H(T-T_{\mathrm{amb}}).
\]

This remains the physical foundation for the rest of Module 6. Divide by $C$:

\[
\frac{dT}{dt}
=\frac{P_u}{C}u-\frac{H}{C}(T-T_{\mathrm{amb}}).
\]

At steady state, $dT/dt=0$, so

\[
T=T_{\mathrm{amb}}+\frac{P_u}{H}u.
\]

Comparison with the Module 4 measurement
$T=T_{\mathrm{amb}}+\chi u$ identifies

\[
\boxed{\chi=\frac{P_u}{H}}.
\]

For constant $u$, define the steady-state temperature

\[
T_{\mathrm{ss}}
=T_{\mathrm{amb}}+\frac{P_u}{H}u
=T_{\mathrm{amb}}+\chi u.
\]

Now define the displacement from that steady state:

\[
\theta(t)=T(t)-T_{\mathrm{ss}}.
\]

Because $u$ and $T_{\mathrm{ss}}$ are constant, substitution into the
one-lump energy balance gives

\[
C\frac{d\theta}{dt}=-H\theta,
\]

or

\[
\frac{d\theta}{dt}=-\frac{H}{C}\theta.
\]

Its solution is

\[
\theta(t)=\theta(0)e^{-(H/C)t}
=\theta(0)e^{-t/\tau}.
\]

Comparison of the exponents identifies the open-loop thermal time constant:

\[
\boxed{\tau=\frac{C}{H}}.
\]

The units confirm that this ratio is a time:

\[
[\tau]=\frac{\mathrm{J/K}}{\mathrm{W/K}}
=\frac{\mathrm{J}}{\mathrm{J/s}}=\mathrm{s}.
\]

<details class="note" markdown="1">
<summary>Sidebar: Dimensionless form</summary>

The ratios $\tau=C/H$ and $\chi=P_u/H$ are the measured combinations that
govern the one-lump model. Define

\[
\hat t=\frac{t}{\tau},
\qquad
\hat T=\frac{T-T_{\mathrm{amb}}}{\chi u_0},
\qquad
\hat u=\frac{u}{u_0}.
\]

The open-loop model becomes

\[
\frac{d\hat T}{d\hat t}=\hat u-\hat T.
\]

This shows that $\tau$ supplies the time scale and $\chi u_0$ supplies the
temperature scale. For P control, the dimensionless loop gain is
$L=\chi K_p$. See [Stone, Sections 1.5.1-1.5.2](../../references/stone-dimensional-analysis-size-and-scale.pdf#page=21)
and [Lienhard, Section 5.2](../../references/lienhard-heat-transfer-textbook-v6.pdf#page=208)
for fuller treatments.

</details>

The two measured quantities are the thermal time constant and the open-loop
susceptibility:

\[
\boxed{\tau=\frac{C}{H}},
\qquad
\boxed{\chi=\frac{P_u}{H}}.
\]

These two measured quantities determine the two parameter ratios that govern
the dynamics:

\[
\boxed{\frac{H}{C}=\frac{1}{\tau}},
\qquad
\boxed{\frac{P_u}{C}
=\frac{P_u/H}{C/H}
=\frac{\chi}{\tau}}.
\]

Module 4 provides the heating and cooling susceptibilities, and a temperature
step from Module 4 or Module 5 provides $\tau$. Use the susceptibility for the
corresponding direction. Therefore, once
$T_{\mathrm{amb}}$ and the command $u$ are specified, the model has **no free
parameters**. Its transient temperature prediction can be compared directly
with the measurement rather than fitted to it.

The same dimensional energy balance can therefore be written entirely in
terms of $\chi$ and $\tau$:

\[
\boxed{
\frac{dT}{dt}
=\frac{T_{\mathrm{amb}}+\chi u-T}{\tau}.
}
\]

This is not a different model. It is the one-lump energy balance expressed in
a form that can be simulated using your measured susceptibility and time
constant. The quantity $T_{\mathrm{amb}}+\chi u$ is the steady temperature toward
which the model moves for a constant command $u$; $\tau$ determines how
quickly it moves there.

## Part 3: Estimate $\tau$

Use a temperature step from Module 4 or Module 5.

Use a trace in which every temperature value was calculated by averaging
exactly 1,000 raw thermistor-voltage measurements, as required in Modules 2
through 5.

One practical method:

1. Identify the initial temperature, $T_{\mathrm{initial}}$.
2. Identify the approximate final temperature, $T_{\mathrm{final}}$.
3. Calculate 63 percent of the total change using
   $T_{63}=T_{\mathrm{initial}}
   +0.63\left(T_{\mathrm{final}}-T_{\mathrm{initial}}\right)$.

4. Estimate $\tau$ as the elapsed time when the temperature first reaches
   $T_{63}$.

Record how uncertain your estimate is. The trace may not be a perfect
exponential. In the dimensional model, this measurement determines the ratio
$C/H$; it does not separately determine $C$ and $H$.

### Using The Prepared Simulation

The simulation is the modeling tool for Parts 4 through 7. It runs
continuously in a rolling time window, and its sliders change physical and
controller parameters while the simulation runs. The display separates the
proportional and integral PWM contributions and shows the dimensional energy
balance, controller equations, heating and cooling susceptibilities, time
constants, P droop prediction, required steady-state command and power, and PI
damping ratio.

Your work is to predict behavior from the equations, choose controlled
parameter comparisons, record quantitative results, and explain the physics
and control. The prepared program supplies the numerical integration; it does
not replace comparison with your experimental data. Its **two-lump** option is
motivated qualitatively in Part 5 and developed quantitatively in [Module 6,
Part II](../lab-07/index.md).

## Part 4: Simulate Open-Loop And P Control

Download [the prepared Module 6/7 TEC
simulation](../../downloads/Lab_6_7_modeling_tec.py). Save it in your
project repository as `python/Lab_6_7_modeling_tec.py`, then run it from the
repository root:

```bash
python python/Lab_6_7_modeling_tec.py
```

For Module 6, select `one_lump` as the physical model. The program performs an
Euler integration of the dimensional energy balance:

\[
T_{n+1}=T_n+\frac{\Delta t}{C}
\left[P_u u_n-H(T_n-T_{\mathrm{amb}})\right].
\]

Because your experiment measures $\chi=P_u/H$ and $\tau=C/H$, the
equivalent measured-parameter update is

\[
\boxed{
T_{n+1}=T_n+\frac{\Delta t}{\tau}
\left(T_{\mathrm{amb}}+\chi u_n-T_n\right).
}
\]

Select `measured` under **Physical parameters**. Enter your measured
$\chi_c$, $\chi_h$, and $\tau$, the on-state voltage measured across the TEC,
and the TEC module resistance from the datasheet. The voltage control is
limited to the apparatus maximum of $12\ \mathrm{V}$. The program uses these
measurements to calculate $r$, $P_{u,c}$, $H$, and the total one-lump
capacitance $C$. Select `direct constants`  when you want to enter $H$,
$C$, $P_{u,c}$, and $r$ independently for a modeling study. Before running,
use the steady-state equation to predict the final temperature for one heating
command and one cooling command.



### Guided Simulation Exercise: Open Loop And Thermal Mass

Select `one_lump`, `measured`, and `open_loop`. Use the
current simulation defaults

\[
T_{\mathrm{amb}}=22\ ^\circ\mathrm{C},
\qquad
\chi_c=0.23\ ^\circ\mathrm{C/PWM},
\qquad
\chi_h=0.46\ ^\circ\mathrm{C/PWM},
\qquad
r=2.
\]

Before each run, predict the steady-state temperature from
$T_{\mathrm{ss}}=T_{\mathrm{amb}}+\chi u$:

| Command | Predicted $T_{\mathrm{ss}}$ |
| ---: | ---: |
| $u=+25$ PWM | $33.5\ ^\circ\mathrm{C}$ |
| $u=-25$ PWM | $16.25\ ^\circ\mathrm{C}$ |
| $u=-50$ PWM | $10.5\ ^\circ\mathrm{C}$ |

Run each case and answer:

1. Why do $+25$ PWM and $-25$ PWM produce unequal temperature changes?
2. Use the displayed PWM value $u$, ambient temperature $T_{\mathrm{amb}}$,
   and steady-state temperature $T_{\mathrm{ss}}$ to calculate $\chi_h$,
   $\chi_c$, and their ratio. Confirm that your calculated values agree with
   the susceptibilities displayed by the simulation.

Next, keep one open-loop command fixed and note the displayed value of $C$.
Select `direct constants`, double $C$, and leave $H$, $P_{u,c}$, and $r$
unchanged. Predict both the steady temperature and the response time before
resuming. Confirm that the steady temperature is unchanged while
$\tau=C/H$ doubles. Explain why thermal mass changes the transient but not the
steady-state energy balance. Return to `measured` before continuing.

After the guided exercise, choose one heating command and one cooling command
that match your experimental runs. Compare the simulated curves with measured
open-loop traces. Record the values and units of $\chi_c$, $\chi_h$, $\tau$,
$T_{\mathrm{amb}}$, $u$, and $\Delta t$. Choose $\Delta t$ much smaller than
$\tau$ and verify that making it smaller does not appreciably change the
result. Explain any important difference between the model and the apparatus.

### Continue With P Control

Keep the same measured one-lump parameters and select `p`. The command is

\[
u_n=K_p(T_{\mathrm{set}}-T_n).
\]

Use one gain from your Module 5 experiment and one larger gain. Before each
run, predict the steady-state droop and closed-loop time constant from

\[
T_{\mathrm{set}}-T_{\mathrm{ss}}
=\frac{T_{\mathrm{set}}-T_{\mathrm{amb}}}{1+\chi K_p},
\qquad
\tau_{\mathrm{cl}}=\frac{\tau}{1+\chi K_p}.
\]

Confirm that increasing $K_p$ decreases both droop and response time. Record
only the settings and whether the predictions agree; do not make a second
P-control data table. The six experimental Goldilocks plots later in this
lesson provide the assessed gain comparison.

## Part 5: Explain The One-Lump P Transient And Its Limit

Now analyze the same dimensional one-lump model used throughout this module.
The solution explains why its P-controlled response cannot oscillate. If the
real apparatus oscillates, the difference identifies physics missing from the
model.

Substituting the P-control law into the energy balance gives

\[
C\frac{dT}{dt}
=P_uK_pT_{\mathrm{set}}+HT_{\mathrm{amb}}
-(H+P_uK_p)T.
\]

Now define the displacement from steady state,

\[
\theta(t)=T(t)-T_{\mathrm{ss}}.
\]

Substitution reduces the entire closed-loop P model to

\[
C\frac{d\theta}{dt}=-(H+P_uK_p)\theta.
\]

Separate variables and integrate:

\[
\frac{d\theta}{\theta}
=-\frac{H+P_uK_p}{C}\,dt,
\]

\[
\ln\!\left(\frac{\theta(t)}{\theta(0)}\right)
=-\frac{H+P_uK_p}{C}t.
\]

Therefore the temperature is explicitly

\[
\boxed{
T(t)=T_{\mathrm{ss}}
+\left[T(0)-T_{\mathrm{ss}}\right]
\exp\!\left(-\frac{H+P_uK_p}{C}t\right)
}.
\]

Equivalently,

\[
T(t)=T_{\mathrm{ss}}
+\left[T(0)-T_{\mathrm{ss}}\right]e^{-t/\tau_{\mathrm{cl}}},
\qquad
\tau_{\mathrm{cl}}=\frac{C}{H+P_uK_p}.
\]

Using $\tau=C/H$ and the dimensionless loop gain $L=\chi K_p$,

\[
\boxed{
\tau_{\mathrm{cl}}=\frac{\tau}{1+\chi K_p}=\frac{\tau}{1+L}.
}
\]

!!! important "Increasing gain has two effects"

    Increasing $K_p$ does two things at the same time:

    1. **It decreases droop.**

        \[
        T_{\mathrm{set}}-T_{\mathrm{ss}}
        =\frac{T_{\mathrm{set}}-T_{\mathrm{amb}}}{1+\chi K_p}.
        \]

    2. **It speeds up the response** by decreasing the closed-loop time
       constant.

        \[
        \tau_{\mathrm{cl}}=\frac{\tau}{1+\chi K_p}.
        \]

    Thus, in this unsaturated one-lump model, both droop and response time are
    reduced by the same factor, $1+\chi K_p$. Larger gain moves the
    temperature closer to the setpoint and makes it approach its steady value
    more quickly.

To find the eigenvalue directly, try an exponential mode,

\[
\theta(t)=\theta_0e^{\lambda t},
\qquad
\frac{d\theta}{dt}=\lambda\theta.
\]

Substitute this trial solution into the homogeneous P equation:

\[
C\lambda\theta=-(H+P_uK_p)\theta.
\]

Cancel the nonzero factor \(\theta\). There is only one eigenvalue,

\[
\lambda=-\frac{H+P_uK_p}{C},
\]

and it is real and negative for positive physical parameters and negative
feedback. The exponential is always positive, so
\(T(t)-T_{\mathrm{ss}}\) retains its
initial sign while shrinking toward zero. The response therefore cannot cross
the steady state, overshoot, or oscillate. Increasing \(K_p\) decreases both
droop and \(\tau_{\mathrm{cl}}\); it does not create the additional dynamical
state or time delay needed for oscillation.

Return to the high-gain trace saved in Module 5. Mark the late-time value
$T_{\mathrm{ss}}$ and the first overshoot. If the measured temperature crosses
$T_{\mathrm{ss}}$, its behavior is incompatible with this one-lump solution.
State the contradiction directly: the model predicts a monotonic exponential,
whereas the apparatus shows an underdamped transient. This is evidence that the
model is inadequate, not that the exponential solution is wrong.

The one-lump model is missing thermal lag between where the TEC applies heat
and where the thermistor measures temperature. The simplest extension is to
represent these locations as two coupled thermal masses. This **two-lump
model** is introduced below and developed systematically in Part II.

<details class="note" markdown="1">
<summary>Why a Thermal Control System Can Oscillate Without Mechanical Inertia</summary>

**Begin with the familiar mass and spring.** A damped mechanical oscillator
obeys

\[
m\ddot x+b\dot x+kx=0.
\]

Its two state variables are position $x$ and velocity $\dot x$. Ignoring
damping for the moment, the spring force is zero when the mass passes through
$x=0$, but the velocity is largest there. Kinetic energy carries the mass past
equilibrium. This is mechanical inertia: zero restoring force does not imply
zero velocity.

**A one-lump thermal model cannot coast.** Its P-controlled displacement obeys

\[
C\frac{d\theta}{dt}=-(H+P_uK_p)\theta.
\]

Temperature is its only state variable. If the net heat flow becomes zero,
then $dT/dt=0$ immediately. The temperature cannot coast through equilibrium,
so the model produces one monotonic exponential and cannot overshoot.

**The apparatus contains a hidden thermal state.** The simplest improvement is
a **two-lump thermal model**. One lump represents the region near the TEC,
where heat is applied. The other represents the block and thermistor, where
temperature is measured. Each lump stores thermal energy, and heat takes time
to move between them.

With P control, $u=K_p(T_{\mathrm{set}}-T_m)$, where $T_m$ is the measured
temperature. Suppose $T_m$ reaches the setpoint and the controller reduces its
command. The TEC-side region can still be hotter than the measured block, so
stored energy continues flowing toward the thermistor and $T_m$ continues
rising. The temperature overshoots not because it has mechanical momentum,
but because the measured temperature does not reveal all the thermal energy
already stored elsewhere in the apparatus.

The qualitative correspondence is

| Mass-spring oscillator | Thermal control system |
| --- | --- |
| measured position $x$ | measured temperature $T_m$ |
| hidden velocity $\dot x$ | hidden TEC-side temperature $T$ |
| kinetic energy carries the mass past equilibrium | stored heat continues flowing after $T_m$ reaches the setpoint |
| mechanical inertia supplies the second state | thermal storage and transport supply the second state |

**The phase-lag interpretation.** The thermistor reports the effect of a TEC
command only after heat has propagated to the measured block. The controller
therefore acts partly on old information. As gain increases, this lag can make
the correction arrive too late, after which the controller overcorrects in the
opposite direction.

This qualitative model explains why the real apparatus can overshoot even
though the one-lump model cannot. [Module 6, Part II introduces the coupled
two-lump equations, shows why they form a second-order system, and explores
their behavior
quantitatively.](../lab-07/index.md#from-two-first-order-equations-to-one-second-order-equation)

</details>

The one-lump model predicts the final temperature well because steady state is
governed by the nearly model-independent requirement that energy entering per
unit time equals energy leaving per unit time. It fails at high gain because
transient behavior also depends on where energy is stored and how long it takes
to reach the thermistor. The qualitative two-lump explanation is developed in
the sidebar above; its equations and parameter study are the focus of Part II.

## Part 6: Add Integral Action In Simulation

Keep the same dimensional one-lump energy balance. PI control changes only the
command supplied to the TEC. Define the temperature error and its accumulated
value as

\[
e=T_{\mathrm{set}}-T,
\qquad
q(t)=q(0)+\int_0^t e(t')\,dt'.
\]

The PI command is

\[
u=K_p e+K_iq,
\]

so the physical model remains

\[
\boxed{
C\frac{dT}{dt}
=P_u\left[K_p(T_{\mathrm{set}}-T)+K_iq\right]
-H(T-T_{\mathrm{amb}}),
\qquad
\frac{dq}{dt}=T_{\mathrm{set}}-T.
}
\]

The simulation first updates the integral state,

\[
q_{n+1}=q_n+(T_{\mathrm{set}}-T_n)\Delta t,
\]

then calculates and clamps the command using the accepted value of
$q_{n+1}$,

\[
u_n=K_p(T_{\mathrm{set}}-T_n)+K_iq_{n+1},
\]

and finally advances the temperature:

\[
T_{n+1}=T_n+\frac{\Delta t}{\tau}
\left(T_{\mathrm{amb}}+\chi u_n-T_n\right).
\]

Select `pi` in the simulation and begin with a stable $K_p$. Use **Zero integral** to
clear the controller memory before a comparison. Watch the displayed values of
$e$, $u_P$, $u_I$, and the applied command while the temperature approaches
the setpoint.

Compare P-only and PI simulations:

- final droop,
- time to approach setpoint,
- overshoot,
- sensitivity to saturation.

The main point is that integral action can reduce steady-state error, but it can
also create overshoot and windup.

### Guided Simulation Exercise: Watch The Integral Contribution

Begin from the P-control case after it has developed visible droop. Select
`pi`, press **Zero integral**, and resume. Watch $e$, $u_P$, $u_I$, and the
applied command $u$ while the temperature approaches the setpoint. Answer:

1. While $e>0$, why does $u_I$ continue to grow?
2. As $T$ reaches the setpoint, why does $u_P$ approach zero?
3. Why can $u_I$ remain nonzero when $e=0$?
4. After steady state, press **Zero integral** again. Why does the temperature
   initially move away from the setpoint?

The steady integral contribution replaces the nonzero proportional error that
was required to provide the steady command under P-only control.

<a id="why-integral-windup-occurs"></a>

<details class="note" markdown="1">
<summary>Why Integral Windup Occurs</summary>

The PI controller first calculates a **requested command**,

\[
u_{\mathrm{req}}=K_pe+K_iq,
\qquad
q_{n+1}=q_n+e_n\Delta t.
\]

The actuator can apply only a limited command, so the program clamps that
request:

\[
u_{\mathrm{applied}}
=\operatorname{clamp}(u_{\mathrm{req}},-u_{\max},u_{\max}).
\]

Suppose a large positive error requests more than $u_{\max}$. The applied PWM
cannot increase further, but ordinary integration keeps adding the positive
error to $q$. The extra integral contribution has no immediate effect on the
TEC because the actuator is already saturated. It is stored in the controller
instead.

When the temperature later approaches the setpoint, the error and proportional
contribution become small, but the accumulated integral contribution can
remain large. The controller therefore continues driving the TEC through the
setpoint. It may take a long time for error of the opposite sign to unwind the
stored integral, producing excessive overshoot and slow recovery.

The anti-windup rule used here is **conditional integration**:

- if the command is saturated and the current error would push it farther into
  saturation, hold $q$ fixed;
- otherwise, update $q$, including when the error helps bring the command out
  of saturation.

The PWM clamp, anti-windup rule, and **Zero integral** control have different
jobs. The clamp protects the actuator, anti-windup controls the growth of the
controller's memory during normal operation, and **Zero integral** deliberately
clears that memory before a new comparison.

</details>

### Why PI Can Be Underdamped

PI control adds the accumulated error as a second state variable. The
one-lump P model has only one state and therefore produces one monotonic
exponential; the one-lump PI model has two coupled states and can overshoot or
oscillate. For the unsaturated linear model, the temperature and integral-state
displacements obey a second-order characteristic equation,

\[
\lambda^2+\frac{H+P_uK_p}{C}\lambda+\frac{P_uK_i}{C}=0.
\]

Real negative roots give a nonoscillatory response, while a complex-conjugate
pair gives a decaying oscillation. This result is included for interpretation,
not as a required A3 derivation. Use the simulation to observe how $K_p$ and
$K_i$ change the response.

## Part 7: Implement PI Control And Collect The Experimental Goldilocks Plots

Use your working Module 5 P controller as the starting point. Do not replace
the Arduino's independent temperature shutdown or the existing signed-PWM
clamp. Implement the integral state and the [conditional-integration rule
introduced above](#why-integral-windup-occurs):

\[
q_{n+1}=q_n+e_n\Delta t,
\qquad
u_n=K_pe_n+K_iq_{n+1}.
\]

Calculate $\Delta t$ from the actual elapsed time between accepted temperature
measurements. Display and save $e$, $u_P=K_pe$, $u_I=K_iq$, the requested
command, and the applied command. Provide a control that sets $q=0$ before a
new comparison.

Use **conditional integration** for anti-windup: if the requested command is
already beyond the PWM limit and the current error would drive it farther into
saturation, do not update $q$ on that step. The output clamp and independent
Arduino safety shutdown remain active even when anti-windup is working.

Before applying actuator power, show the instructor the lines that calculate
$e$, $q$, $u_P$, $u_I$, and the clamped command. Then:

1. Use the same safe setpoint and a stable $K_p$ from Module 5.
2. Set $K_i=0$, zero the integral state, and record a P-only baseline.
3. Set PWM to zero before changing controller mode or resetting the integral.
4. Choose a small positive $K_i$ after exploring it in the simulation. Zero the integral
   state, enable PI, and record the response from comparable initial conditions.
5. Confirm that $u_I$ grows while a persistent error remains and that the
   steady error becomes smaller than in the P-only run.
6. Stop and set PWM to zero if the temperature moves in the wrong direction,
   the display freezes, saturation persists unexpectedly, or oscillations grow.

Preserve both traces and the exact $K_p$, $K_i$, setpoint, starting
temperature, PWM limit, sample interval, and anti-windup setting. These two
preliminary traces establish that the controller works. Now complete the
Goldilocks study below before beginning Part II.

### Experimental Goldilocks Study

Use one apparatus, one PWM limit, and the same two temperature setpoints for
all six retained runs. Each run must contain an upward setpoint step and a
downward setpoint step so that heating and cooling are compared under matched
conditions. Begin each step from a settled or clearly documented initial
temperature.

| Run | Controller | Gain choice | Purpose |
| ---: | --- | --- | --- |
| 1 | P | Low $K_p$ | No overshoot; relatively slow response or large droop |
| 2 | P | Intermediate $K_p$ | Best P-only compromise |
| 3 | P | High $K_p$ | Clear overshoot or ringing |
| 4 | PI | Slightly below Run 2 $K_p$; low $K_i$ | Slow integral correction |
| 5 | PI | Run 4 $K_p$; intermediate $K_i$ | Best PI compromise |
| 6 | PI | Run 4 $K_p$; high $K_i$ | Excess overshoot, ringing, or saturation |

For P runs, set $K_i=0$. **Hint for PI control:** the integral term contributes
part of the output $u$, so begin by exploring $K_p$ values near but slightly
below the Run 2 value. Choose one PI value of $K_p$, hold it fixed for Runs
4-6, and change only $K_i$. Reset the integral state before every run.
Preserve time series for measured temperature, setpoint, signed applied PWM,
$u_P$, $u_I$, and error. Record the actual gains, initial temperatures, PWM
limit, sample interval, and anti-windup setting. The Arduino temperature
shutdown and PWM clamp remain active for every run.

Make and label the **six experimental Goldilocks plots** during this lesson.
Part II asks you to make the six corresponding simulation plots and compare
them under matched conditions.

### Preserve Your Evidence

Before closing the simulation or dismantling the apparatus, save the settings,
data, plots, and calculations needed for A3. Commit the simulation and your
Markdown record so the analysis is reproducible.

```bash
git status
git add README.md docs data python/Lab_6_7_modeling_tec.py
git commit -m "Analyze open-loop P and PI temperature control"
git push
```

## A3: Feedback Data And Lumped-Model Memo

- **Due:** Wednesday, October 21, at **6:00 PM**
- **Type:** team, 10 points
- **Moodle file:** `A3_Lastname_Lastname.pdf`
- **Moodle submission:** Each student uploads the team PDF separately;
  teammates may upload the same PDF
- **Repository file:** `docs/assessments/a3_feedback_model.md`
- **Analysis and submission target:** about **2 hours** after the in-class analysis is
  complete

**A3 spans both parts of Module 6.** After Part I, you can complete Questions
1, 2, and 4. Complete Questions 3 and 5 only after Part II: Question 3 uses
the two-lump model to simulate P and PI responses with overshoot, and Question
5 uses that model to explain why the one-lump model succeeds at steady state
but fails to reproduce the measured high-gain transient behavior.

The final A3 assembly consists of selecting the already completed comparison
plots and table, writing the short interpretation, checking paths, committing,
pushing, and submitting the PDF. The one-lump derivation is part of this paper,
not a separate graded document.

Use the six experimental Goldilocks plots produced in Part 7 and the six
corresponding simulation plots produced in Part II. No additional runs are
required for A3.

### A3 Questions

Answer the following questions concisely. Support each answer with equations,
measured values, or plots where requested.

#### 1. One-Lump Model And P-Control Predictions

Starting from the dimensional one-lump energy balance, show that $\tau=C/H$
and $\chi=P_u/H$, then write the model using your measured $\tau$ and $\chi$.
Derive the P-control droop,

\[
T_{\mathrm{set}}-T_{\mathrm{ss}}
=\frac{T_{\mathrm{set}}-T_{\mathrm{amb}}}{1+\chi K_p},
\]

and the closed-loop time constant,

\[
\tau_{\mathrm{cl}}=\frac{\tau}{1+\chi K_p}.
\]

Explain why increasing $K_p$ both decreases droop and speeds up the response.
Identify the dimensionless loop gain. Compare one representative open-loop or
P-control prediction with measurement and state what agrees.

<span id="a3-question-2"></span>

#### 2. Experimental Goldilocks Plots And Step-Response Metrics

**Part 1: Experimental Goldilocks plots.**

Present six experimental plots: low-, medium-, and high-gain P responses
followed by low-, medium-, and high-gain PI responses. For each plot, show the
process output (measured temperature) and process input (signed applied PWM).
The four curves in the reference figure below correspond to this part: the
input $u$ and output $y$ for P control, and the input $u$ and output $y$ for PI
control.

![Responses to step changes for proportional and PI control](../../assets/controller_gain_response_reference.png)

*Reference responses for (a) proportional control and (b) PI control. In this
course, the input $u$ is the signed PWM command applied to the TEC, and the
output $y$ is the measured temperature.*

**Part 2: Step-response metrics.**

Analyze the largest-gain P and PI cases quantitatively. For both upward and
downward steps, report rise time, percent overshoot, settling time,
steady-state error, and oscillation period when applicable. Define the
thresholds used for rise and settling times.

![Rise time, percent overshoot, settling time, and steady-state error](../../assets/step_response_metrics.gif)

*Step-response attributes: rise time, percent overshoot, settling time, and
steady-state error.*

<span id="a3-question-3"></span>

#### 3. Simulation Goldilocks Plots And Experiment-Theory Comparison

**To be answered after completing Part II.**

Present six simulation plots corresponding to the six experimental plots in
Question 2. Every simulation must use the **same physical parameters**
$\chi_c$, $\chi_h$, $\tau$, $G$, $C_T/C$, TEC voltage, TEC resistance,
setpoints, starting conditions, and PWM limit because all six experiments use
the same apparatus. Change only controller mode, $K_p$, and $K_i$ as required
by the six-run protocol. Use the two-lump equations to explain which parameters
primarily control rise time, P-control droop, overshoot, and the number and
decay of oscillations. Identify one important agreement and one important
disagreement between simulation and experiment.

#### 4. Integral Action And Windup

Use $u=u_P+u_I=K_pe+K_iq$ and $dq/dt=e$ to explain how integral action removes
droop. Explain integral windup, describe your anti-windup rule, and state what
happens when the integral state is reset after PI control has reached steady
state.

#### 5. Model Limits And Gain Selection

**To be answered after completing Part II.**

Explain mathematically why the one-lump P-control model cannot overshoot. Use
the two-lump equations and your twelve Goldilocks plots to explain how internal
thermal lag produces behavior absent from the one-lump model. Justify your
final $K_p$ and $K_i$ and name one physical effect that a better model should
include.

### What To Submit

Submit one PDF containing concise responses to all five questions, the six
experimental and six simulated Goldilocks plots, the comparison tables, and
links to the underlying data, analysis
code, and GitHub modeling checkpoint. Integrate the [Module 5 interpretation
questions](../lab-05/index.md#student-derivation-recover-the-droop-equation)
into A3 Questions 1 and 5, and integrate the windup thought experiment into
Question 4 rather than repeating either set separately.

### A3 Rubric

| Criterion | Points |
| --- | ---: |
| One-lump energy balance, measured parameters, P-control droop, response speed, and dimensionless gain are correct | 2 |
| Six experimental Goldilocks plots use matched conditions, and the largest-gain P and PI runs are quantified in both directions | 2 |
| Six simulation Goldilocks plots use one common set of physical parameters and are compared with experiment | 2 |
| Integral action, reset, windup, and anti-windup are explained using the controller equations | 2 |
| The two-lump explanation, parameter-behavior connections, model comparison, and final gain choice are justified | 2 |

### Oral Review Questions: PI Control

Use this PI-control question to check your understanding and prepare A3:

1. Why can integral action remove droop, and what is integral windup?
2. How did changing $K_p$ and $K_i$ affect rise time, overshoot, settling time,
   steady-state error, and saturation in the physical apparatus?

Also prepare the [Module 5 P-control questions](../lab-05/index.md#oral-review-questions-p-control)
and [Module 7 modeling questions](../lab-07/index.md#oral-review-questions-process-modeling).
The [A3 deadline and rubric](#a3-feedback-data-and-lumped-model-memo) are above.
