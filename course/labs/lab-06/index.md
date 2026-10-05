# Module 6, Part I: P/PI Control And Lumped Modeling

Module 6 has two linked parts:

1. **Part I (this page):** develop one-lump P and PI models and connect them to
   the Module 5 measurements.
2. [**Part II: TEC Process Model And Python Simulation**](../lab-07/index.md):
   extend the model, compare one- and two-lump descriptions, and test the model
   in Python.

## Purpose

Module 6 slows down the theory. Module 5 showed that proportional feedback reduces
steady-state error but can become unstable. Module 6 builds simple models that
explain those observations.

The goal is not to become fluent in Laplace transforms. The goal is to connect
thermal physics, feedback equations, and the data you measured from the TEC.

You will begin with algebra, then simulate the one-lump model in time, then
extend the model just enough to understand why integral control is useful and
why real feedback loops can oscillate.

## Theme

**Time-Domain Models For P And PI Control**

Droop, time constants, numerical simulation, and the first model of integral
action.

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

- **Thermal capacitance:** energy required to raise the lump's temperature by
  one degree.
- **Thermal resistance:** opposition to passive heat flow between the lump and
  its surroundings.
- **Heat-loss conductance:** the inverse of thermal resistance; passive heat
  transfer per degree of temperature difference.
- **Time constant:** characteristic time over which a first-order system
  approaches a new temperature.
- **Open-loop temperature susceptibility:** steady-state temperature change per
  applied PWM command, with direction held fixed.
- **P control:** command proportional to the current temperature error.
- **I control:** command proportional to accumulated temperature error.
- **Windup:** continued growth of the integral term while the actuator is
  saturated.
- **Droop:** nonzero steady-state temperature error in P-only control.

### Symbols Used In Part 1

Symbols appear below in the order they are first used in Part 1. A temperature
difference has the same numerical value in K and °C.

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
| $\chi_{T,u}$ | Open-loop temperature susceptibility: steady-state temperature change per signed PWM count | °C/PWM count |
| $K_p$ | Proportional gain | PWM counts/°C |
| $T_{\mathrm{set}}$ | Requested temperature setpoint | °C |
| $\mathrm{droop}=T_{\mathrm{set}}-T$ | Steady-state temperature error | °C |

## Before Class

Review your Module 4 and Module 5 results. Before class, make sure you can
locate and open these existing files on your laptop:

- Module 4 steady-state temperature versus PWM data,
- Module 5 droop-versus-gain data,
- one Module 5 strip-chart trace at a stable gain,
- one Module 5 strip-chart trace near oscillation, if you observed one, and
- your current Python plotting or modeling environment.

Do not create new figures, tables, or written work for this section. The files
will be used during the in-class model comparison.

## Outside-Class Workload Budget

| Session | Work | Planned time |
| --- | --- | ---: |
| S12 | Read this assignment and the selected heat-transfer material | 90 minutes |
| S12 | Complete and check the guided one-lump derivation | 120 minutes |
| S12 | **Total associated with S12** | **3 hours 30 minutes** |
| S13 | Review PI control and windup; answer the preparation questions | 60 minutes |
| S13 | Prepare or revise the P/PI simulation for in-class comparison | 105 minutes |
| S13 | **Total associated with S13** | **2 hours 45 minutes** |
| S14 | Analyze matched P/PI results | 90 minutes |
| S14 | Write, check, commit, push, and prepare A3 | 120 minutes |
| S14 | **Total associated with S14** | **3 hours 30 minutes** |

Do not add optional reading until the required derivation and A3 evidence are
complete and understood.

## Pre-Class Questions

1. What physical part of the apparatus stores heat?
2. What physical paths let heat leave the measured block?
3. What evidence from your data suggests a thermal time constant?
4. Why does the algebraic droop model not predict oscillation?

## What You Will Do

- Derive the algebraic P-control droop model.
- Fit or estimate an open-loop thermal slope from Module 4.
- Fit or estimate a time constant from a temperature step.
- Simulate a first-order TEC/block model.
- Add P-only feedback to the simulation.
- Compare simulated droop with measured droop.
- Add a simple PI controller in simulation.
- Explain why integral action reduces droop and why windup is a problem.

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
T=T_{\mathrm{amb}}+\chi_{T,u}u,
\]

where $\chi_{T,u}=dT/du$ is the open-loop susceptibility with respect to signed
PWM. With the signed convention, $\chi_{T,u}$ is positive: positive $u$ heats
and raises $T$, while negative $u$ cools and lowers $T$. P-only feedback supplies

\[
u=K_p(T_{\mathrm{set}}-T).
\]

Substitute the controller law into the measured open-loop relationship:

\[
T=T_{\mathrm{amb}}+\chi_{T,u}K_p(T_{\mathrm{set}}-T).
\]

At steady state, collect the terms containing $T$:

\[
(1+\chi_{T,u}K_p)T
=T_{\mathrm{amb}}+\chi_{T,u}K_pT_{\mathrm{set}}.
\]

Subtract this result from $T_{\mathrm{set}}$ to obtain the droop:

\[
\boxed{
T_{\mathrm{set}}-T=
\frac{T_{\mathrm{set}}-T_{\mathrm{amb}}}{1+\chi_{T,u}K_p}.
}
\]

The product $L=\chi_{T,u}K_p$ is dimensionless. It is the loop gain for this
steady-state model. Part 2 derives $\chi_{T,u}=P_u/H$ from the dimensional
model.

Using one of your Module 5 runs, use $\chi_{T,u}$, $T_{\mathrm{amb}}$,
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
$T=T_{\mathrm{amb}}+\chi_{T,u}u$ identifies

\[
\boxed{\chi_{T,u}=\frac{P_u}{H}}.
\]

For constant $u$, define the steady-state temperature

\[
T_{\mathrm{ss}}
=T_{\mathrm{amb}}+\frac{P_u}{H}u
=T_{\mathrm{amb}}+\chi_{T,u}u.
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

!!! note "Sidebar: From dimensional analysis to a dimensionless model"

    This follows the progression in [Howard Stone, Sections 1.5.1-1.5.2:
    characteristic time and rescaling a differential
    equation](../../references/stone-dimensional-analysis-size-and-scale.pdf#page=21).
    Stone examines a model four related ways: inspect the dimensions, balance
    the sizes of terms, solve the equation when possible, and then rescale it
    so that only dimensionless variables and parameters remain.

    **1. Inspect the dimensions.** For the unforced departure from steady state,

    \[
    C\frac{d\vartheta}{dt}=-H\vartheta,
    \qquad \vartheta=T-T_{\mathrm{ss}},
    \]

    the parameters that contain time are $C$ and $H$. Their ratio has units of
    time:

    \[
    \frac{C}{H}
    =\frac{\mathrm{J/K}}{\mathrm{W/K}}
    =\mathrm{s}.
    \]

    Dimensional analysis therefore identifies $C/H$ as the characteristic
    time, but cannot by itself determine the complete function of time.

    **2. Balance the sizes of the terms.** If a typical temperature departure
    $\Delta T$ changes over a typical time $t_c$, then

    \[
    C\frac{\Delta T}{t_c}\sim H\Delta T.
    \]

    The temperature scale cancels because this equation is linear, leaving

    \[
    t_c\sim\frac{C}{H}.
    \]

    **3. Solve the equation.** Separation of variables gives

    \[
    \vartheta(t)=\vartheta(0)e^{-tH/C}.
    \]

    The solution supplies what dimensional reasoning alone cannot: the decay
    is exponential, and its exact time constant is $\tau=C/H$.

    **4. Nondimensionalize time and temperature.** Following Stone, choose the
    initial departure as the temperature scale and define

    \[
    \Theta=\frac{\vartheta}{\vartheta(0)}
    =\frac{T-T_{\mathrm{ss}}}{T(0)-T_{\mathrm{ss}}},
    \qquad
    \hat t=\frac{t}{\tau}.
    \]

    Substitution removes every dimensional parameter:

    \[
    \frac{d\Theta}{d\hat t}=-\Theta,
    \qquad \Theta(0)=1,
    \qquad \Theta=e^{-\hat t}.
    \]

    This is also the form used in [Lienhard and Lienhard, Section 5.2:
    dimensional analysis of a lumped-capacity
    system](../../references/lienhard-heat-transfer-textbook-v6.pdf#page=208).
    They use

    \[
    \Theta=\frac{T-T_\infty}{T_i-T_\infty},
    \qquad
    \frac{t}{\mathcal{T}},
    \qquad
    \mathcal{T}=\frac{\rho cV}{hA}.
    \]

    In our notation, $C=\rho cV$, $H=hA$, and $T_\infty=T_{\mathrm{amb}}$,
    so Lienhard's $\mathcal{T}$ is our $\tau=C/H$. See also [Lienhard and
    Lienhard, Section 4.3](../../references/lienhard-heat-transfer-textbook-v6.pdf#page=164)
    for why temperature is nondimensionalized using a temperature
    *difference*: the absolute temperature level is not significant in a
    linear conduction problem.

    **What changes when the TEC drives the system?** Choose a characteristic
    command $u_0$ and a characteristic temperature change $\Delta T$, then
    define

    \[
    \hat t=\frac{t}{\tau},\qquad
    \hat T=\frac{T-T_{\mathrm{amb}}}{\Delta T},\qquad
    \hat u=\frac{u}{u_0}.
    \]

    Substitution into the one-lump model gives

    \[
    \frac{d\hat T}{d\hat t}
    =\Gamma\hat u-\hat T,
    \qquad
    \Gamma=\frac{\chi_{T,u}u_0}{\Delta T}.
    \]

    Thus the dimensional parameters enter through the single dimensionless
    group $\Gamma$. Choosing $\Delta T=\chi_{T,u}u_0$, the steady temperature
    change produced by $u_0$, makes $\Gamma=1$ and leaves

    \[
    \frac{d\hat T}{d\hat t}=\hat u-\hat T.
    \]

    Thus, for an open-loop step, the natural temperature scale is either the
    measured step size or $\chi_{T,u}u_0$, its predicted steady-state value.
    For setpoint control, use
    $\Delta T=|T_{\mathrm{set}}-T_{\mathrm{amb}}|$. Absolute temperature is not
    useful here because the model depends only on temperature differences.
    Absolute kelvin temperature would become relevant for thermal radiation or
    strongly temperature-dependent material properties.

    Nondimensionalization is useful because it reveals which experiments are
    dynamically equivalent. For P control, scaling by the setpoint offset gives

    \[
    \frac{d\hat T}{d\hat t}
    =L(\hat T_{\mathrm{set}}-\hat T)-\hat T,
    \qquad
    L=\chi_{T,u}K_p,
    \]

    where $L$ is the dimensionless loop gain and
    $\hat T_{\mathrm{set}}=+1$ for heating or $-1$ for cooling. The response
    shape is therefore controlled by $L$, while $\tau$ restores the physical
    time scale.

Therefore $P_u/C=\chi_{T,u}/\tau$ and $H/C=1/\tau$. The same dimensional
energy balance can be written entirely in terms of the two measured parameters
$\chi_{T,u}$ and $\tau$:

\[
\boxed{
\frac{dT}{dt}
=\frac{T_{\mathrm{amb}}+\chi_{T,u}u-T}{\tau}.
}
\]

This is not a different model. It is the one-lump energy balance expressed in
a form that can be simulated using your measured susceptibility and time
constant. The quantity $T_{\mathrm{amb}}+\chi_{T,u}u$ is the steady temperature toward
which the model moves for a constant command $u$; $\tau$ determines how
quickly it moves there.

## Part 3: Estimate $\tau$

Use a temperature step from Module 4 or Module 5.

Use a trace in which every temperature value was calculated after averaging
between 100 and 1000 raw thermistor-voltage measurements, as required in Modules
2 through 5.

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

## Part 4: Simulate Open-Loop Response

Write a short Python simulation of the dimensional one-lump balance using
Euler integration:

\[
T_{n+1}=T_n+\frac{\Delta t}{C}
\left[P_u u_n-H(T_n-T_{\mathrm{amb}})\right].
\]

Because your experiment measures $\chi_{T,u}=P_u/H$ and $\tau=C/H$, implement the
equivalent measured-parameter update:

\[
\boxed{
T_{n+1}=T_n+\frac{\Delta t}{\tau}
\left(T_{\mathrm{amb}}+\chi_{T,u}u_n-T_n\right).
}
\]

Simulate a constant signed PWM command and compare the simulated curve with one
of your measured open-loop traces. State the values and units of $\chi_{T,u}$, $\tau$,
$T_{\mathrm{amb}}$, $u$, and $\Delta t$. Choose $\Delta t$ much smaller than
$\tau$ and verify that making it smaller does not appreciably change the
result.

## Part 5: Simulate P-Only Feedback

Continue using the same one-lump energy balance. Replace the constant command
with

\[
u_n=K_p(T_{\mathrm{set}}-T_n),
\]

then clamp $u_n$ to the allowed signed PWM range before applying the Euler
update from Part 4.

Simulate several values of $K_p$. Plot:

- temperature versus time,
- PWM command versus time,
- final droop versus $K_p$.

Compare with Module 5. The one-lump model should capture some trends, but it
may not reproduce oscillations.

## Part 6: Solve The P-Controlled One-Lump Model

Now analyze the same dimensional one-lump model used throughout this module.
The solution explains why its P-controlled response cannot oscillate. If the
real apparatus oscillates, the difference identifies physics missing from the
model.

With P control, the energy balance is

\[
C\frac{dT}{dt}
=P_uK_pT_{\mathrm{set}}+HT_{\mathrm{amb}}
-(H+P_uK_p)T.
\]

First find the steady-state temperature by setting \(dT/dt=0\):

\[
T_{\mathrm{ss}}
=\frac{P_uK_pT_{\mathrm{set}}+HT_{\mathrm{amb}}}
{H+P_uK_p}.
\]

The remaining error from the setpoint is the P-control droop:

\[
T_{\mathrm{set}}-T_{\mathrm{ss}}
=\frac{H(T_{\mathrm{set}}-T_{\mathrm{amb}})}
{H+P_uK_p}.
\]

Divide numerator and denominator by $H$ and use $\chi_{T,u}=P_u/H$:

\[
T_{\mathrm{set}}-T_{\mathrm{ss}}
=\frac{T_{\mathrm{set}}-T_{\mathrm{amb}}}{1+\chi_{T,u}K_p}.
\]

This is the same droop equation derived from the measured open-loop relation
in Part 1.

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

Using $\tau=C/H$ and the dimensionless loop gain $L=\chi_{T,u}K_p$,

\[
\boxed{
\tau_{\mathrm{cl}}=\frac{\tau}{1+\chi_{T,u}K_p}=\frac{\tau}{1+L}.
}
\]

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

Discuss what you would need to add:

- a time delay,
- two thermal masses,
- sensor lag,
- actuator lag,
- discrete controller update time,
- PWM saturation,
- measurement noise.

Choose one extension that you think is physically most important for the class
apparatus.

## Part 7: Add Integral Action In Simulation

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

At each time step, calculate and clamp the command from the current state, then
update both state variables:

\[
u_n=K_p(T_{\mathrm{set}}-T_n)+K_iq_n,
\]

\[
T_{n+1}=T_n+\frac{\Delta t}{\tau}
\left(T_{\mathrm{amb}}+\chi_{T,u}u_n-T_n\right).
\]

\[
q_{n+1}=q_n+(T_{\mathrm{set}}-T_n)\Delta t.
\]

Simulate PI control for a stable $K_p$.

Compare P-only and PI simulations:

- final droop,
- time to approach setpoint,
- overshoot,
- sensitivity to saturation.

The main point is that integral action can reduce steady-state error, but it can
also create overshoot and windup.

### Why PI Can Be Underdamped

From the definitions above,

\[
\frac{dq}{dt}=e,
\qquad
u=K_p e+K_i q,
\qquad
e=T_{\mathrm{set}}-T.
\]

For an unsaturated PI controller at steady state, the temperature reaches the
setpoint and the integral term supplies the PWM needed to balance heat loss:

\[
T_{\mathrm{ss}}=T_{\mathrm{set}},
\qquad
q_{\mathrm{ss}}
=\frac{H(T_{\mathrm{set}}-T_{\mathrm{amb}})}{P_uK_i}.
\]

Now define the **two state variables as displacements from steady state**:

\[
\boxed{
\theta(t)=T(t)-T_{\mathrm{set}}
},
\qquad
\boxed{
z(t)=q(t)-q_{\mathrm{ss}}
}.
\]

Thus \(\theta\) is the temperature displacement and \(z\) is the integral-state
displacement. Because \(e=-\theta\), their time derivatives obey

\[
\frac{d\theta}{dt}
=-\frac{H+P_uK_p}{C}\theta
+\frac{P_uK_i}{C}z,
\qquad
\frac{dz}{dt}=-\theta.
\]

In matrix form,

\[
\frac{d}{dt}
\begin{pmatrix}
\theta\\ z
\end{pmatrix}
=
\underbrace{
\begin{pmatrix}
-\dfrac{H+P_uK_p}{C} & \dfrac{P_uK_i}{C}\\
-1 & 0
\end{pmatrix}
}_{A}
\begin{pmatrix}
\theta\\ z
\end{pmatrix}.
\]

<details class="note" markdown="1">
<summary>Sidebar: Solving a matrix ODE by diagonalization</summary>

Write the two state variables as one vector,

\[
\mathbf{x}(t)=
\begin{pmatrix}
\theta(t)\\ z(t)
\end{pmatrix},
\qquad
\frac{d\mathbf{x}}{dt}=A\mathbf{x}.
\]

First look for one exponential mode,

\[
\mathbf{x}(t)=\mathbf{v}e^{\lambda t},
\]

where the constant vector \(\mathbf{v}\) gives the relative amounts of
temperature displacement and integral-state displacement in that mode.
Substitution gives

\[
\lambda\mathbf{v}e^{\lambda t}
=A\mathbf{v}e^{\lambda t},
\]

and cancellation of the nonzero exponential leaves

\[
(A-\lambda I)\mathbf{v}=0.
\]

We want a nonzero eigenvector \(\mathbf{v}\). A homogeneous matrix equation
has a nonzero solution only when its matrix is singular, so

\[
\boxed{\det(A-\lambda I)=0}.
\]

This determinant equation therefore finds the values of \(\lambda\) for which
exponential solutions are possible. For each eigenvalue, solving
\((A-\lambda I)\mathbf{v}=0\) gives its eigenvector.

If the two eigenvectors are independent, place them in the columns of

\[
V=\begin{pmatrix}\mathbf{v}_+&\mathbf{v}_-\end{pmatrix},
\qquad
\Lambda=
\begin{pmatrix}
\lambda_+&0\\0&\lambda_-
\end{pmatrix}.
\]

The eigenvalue equations together say \(AV=V\Lambda\), or

\[
A=V\Lambda V^{-1}.
\]

Now change coordinates by writing \(\mathbf{x}=V\mathbf{y}\). The coupled
matrix equation becomes

\[
\frac{d\mathbf{y}}{dt}=\Lambda\mathbf{y}.
\]

Because \(\Lambda\) is diagonal, this is just two independent scalar
equations:

\[
\frac{dy_+}{dt}=\lambda_+y_+,
\qquad
\frac{dy_-}{dt}=\lambda_-y_-.
\]

Their solutions are \(y_\pm(t)=y_\pm(0)e^{\lambda_\pm t}\). Transforming back
gives

\[
\boxed{
\mathbf{x}(t)
=V
\begin{pmatrix}
e^{\lambda_+t}&0\\0&e^{\lambda_-t}
\end{pmatrix}
V^{-1}\mathbf{x}(0)
=e^{At}\mathbf{x}(0)
}.
\]

Thus diagonalization reveals the matrix exponential as a combination of two
ordinary exponential modes. If the eigenvalues are complex conjugates, those
two modes combine to produce a real decaying oscillation. At critical damping,
the repeated eigenvalue may provide only one eigenvector; the matrix
exponential still exists, but its solution can also contain a term
proportional to \(t e^{\lambda t}\).

</details>

The eigenvalues satisfy

\[
\det(A-\lambda I)=0.
\]

Evaluating this determinant gives the characteristic equation

\[
\lambda^2
+\frac{H+P_uK_p}{C}\lambda
+\frac{P_uK_i}{C}=0.
\]

The quadratic formula gives both eigenvalues:

\[
\boxed{
\lambda_{\pm}
=-\frac{H+P_uK_p}{2C}
\pm
\sqrt{
\left(\frac{H+P_uK_p}{2C}\right)^2
-\frac{P_uK_i}{C}
}
}.
\]

- Two negative real eigenvalues give an overdamped response.
- One repeated negative eigenvalue gives critical damping.
- A complex-conjugate pair with negative real parts gives an underdamped
  oscillation.
- An eigenvalue with a positive real part gives an unstable response.

The damping ratio is a dimensionless number the transition from under- to over-damped:

\[
\boxed{
\zeta=\frac{H+P_uK_p}{2\sqrt{CP_uK_i}}
}.
\]

The linear PI response is underdamped when

\[
\zeta<1
\qquad\Longleftrightarrow\qquad
(H+P_uK_p)^2<4CP_uK_i.
\]

Increasing $C$ or $K_i$ increases the tendency to oscillate while increasing $H$ or $K_p$ dampens the system.

<details class="note" markdown="1">
<summary>Time constants for open-loop, P, and PI control</summary>

The open-loop one-lump model has one time constant,

\[
\tau=\frac{C}{H}.
\]

P control changes the coefficient multiplying the temperature displacement
but does not add a state variable. Its response is still a single
exponential, with

\[
\boxed{
\tau_P=\frac{C}{H+P_uK_p}
=\frac{\tau}{1+\chi_{T,u}K_p}
}.
\]

Thus P control makes the one-lump response faster as $K_p$ increases,
although it retains steady-state droop.

PI control adds the integral state, so it is a second-order system and
generally does **not** have one time constant. Its two eigenvalues are
$\lambda_+$ and $\lambda_-$, as derived above.

**Overdamped PI control.** If both eigenvalues are real and negative, the
response contains two exponentials. Their time constants are

\[
\tau_+=-\frac{1}{\lambda_+},
\qquad
\tau_-=-\frac{1}{\lambda_-}.
\]

The eigenvalue closer to zero gives the slow time constant and usually
controls the final approach to the setpoint. The other gives the fast
transient.

**Underdamped PI control.** If the eigenvalues are complex, write

\[
\lambda_{\pm}=-\zeta\omega_n\pm i\omega_d,
\qquad
\omega_n=\sqrt{\frac{P_uK_i}{C}},
\qquad
\omega_d
=\sqrt{
\frac{P_uK_i}{C}
-\left(\frac{H+P_uK_p}{2C}\right)^2
}
=\omega_n\sqrt{1-\zeta^2}.
\]

The oscillation envelope decays with time constant

\[
\boxed{
\tau_{\mathrm{env}}
=\frac{1}{\zeta\omega_n}
=\frac{2C}{H+P_uK_p}
=2\tau_P
}.
\]

The oscillation frequency in hertz and the corresponding period are

\[
\boxed{
f_{\mathrm{osc}}
=\frac{\omega_d}{2\pi}
=\frac{1}{2\pi}
\sqrt{
\frac{P_uK_i}{C}
-\left(\frac{H+P_uK_p}{2C}\right)^2
}
},
\qquad
T_{\mathrm{osc}}=\frac{1}{f_{\mathrm{osc}}}
=\frac{2\pi}{\omega_d}.
\]

The period and decay time are different quantities: $T_{\mathrm{osc}}$
describes how rapidly the response oscillates, while
$\tau_{\mathrm{env}}$ describes how rapidly those oscillations decay.

**Critically damped PI control.** The two eigenvalues coincide. The
characteristic decay time is

\[
\tau_{\mathrm{crit}}
=\frac{1}{\omega_n}
=\frac{2C}{H+P_uK_p}.
\]

Therefore, report one time constant for open-loop or P control. For PI
control, report the two real time constants when overdamped, or report the
decay-envelope time and oscillation period when underdamped.

</details>

Use the simulation to find one overdamped and one underdamped parameter set.
For each case, record \(C\), \(H\), \(P_u\), \(K_p\), \(K_i\), the displayed
value of \(\zeta\), and whether the temperature trace agrees with the
prediction. The formula applies only while the model is linear and the PWM is
not saturated.

### Instructor Verification And Exploration Tool

**First implement your own one-lump model for open-loop, P, and PI control.**
Your program must perform the Euler update itself and produce the comparisons
requested in Parts 4, 5, and 7. Do not begin with the supplied program, and do
not submit the supplied program unchanged as your own work.

After your own open-loop, P, and PI simulations run, download
[the rolling-window Module 6 open-loop/P/PI simulation](../../downloads/Lab_6_pi_contribution_rolling_demo.py).
Save it in your project repository as
`python/Lab_6_pi_contribution_rolling_demo.py`, then run it from the repository
root:

```bash
python python/Lab_6_pi_contribution_rolling_demo.py
```

The supplied simulation runs continuously in a rolling time window. Select
open-loop, P, or PI control; pause and resume the run; and change model or
controller parameters while watching the temperature and PWM histories. The
display separates the proportional and integral contributions to PWM and shows
the dimensional energy balance, controller equations, open-loop time constant,
P droop prediction, required steady-state PWM, and PI damping ratio. Use it to
check your reasoning, compare its predictions with your independently written
model, and investigate parameter changes. Do not substitute its plots for
comparisons with your own experimental data.

## Part 8: Windup Thought Experiment

Suppose the setpoint is far away and the controller demands more PWM than the
hardware can supply. The PWM saturates, but the integral error may keep growing.

Answer:

1. What happens to the integral term while PWM is saturated?
2. What happens after the temperature finally approaches the setpoint?
3. Why might this cause overshoot?
4. How could software prevent or reduce windup?

## Part 9: Modeling Checkpoint

Commit your modeling notebook or Python script.

```bash
git status
git add README.md python docs data
git commit -m "Model P and PI temperature control"
git push
```

## Complete And Preserve The A3 Work

Module 6 combines the most important Module 4-6 evidence into one purposeful
team paper. The one-lump derivation is guided work used in the paper and in the
later oral-review questions; it is not a separate document to grade.

For the in-class modeling work, save the parameter set, units, initial
conditions, controller settings, saturation limits, exact command used to run
the model, open-loop comparison, matched P/PI plots, and residuals. Complete
the comparison table while the simulations and experimental traces are open.

### A3: Feedback Data And Lumped-Model Memo

- **Due:** Wednesday, October 21, at **6:00 PM**
- **Type:** team, 10 points
- **Moodle file:** `A3_Lastname_Lastname.pdf`
- **Moodle submission:** Each student uploads the team PDF separately;
  teammates may upload the same PDF
- **Repository file:** `docs/assessments/a3_feedback_model.md`
- **Analysis and submission target:** about **2 hours** after the in-class analysis is
  complete

The final A3 assembly consists of selecting the already completed comparison
plots and table, writing the short interpretation, checking paths, committing,
pushing, and submitting the PDF.

## What To Submit

Submit:

- derivation of the P-control droop equation,
- concise responses to the [three Module 5 interpretation questions](../lab-05/index.md#student-derivation-recover-the-droop-equation), integrated with that derivation and the droop data rather than repeated separately,
- estimate of open-loop temperature susceptibility $\chi_{T,u}$,
- estimate of thermal time constant `tau`,
- open-loop simulation compared with one measured trace,
- P-only simulation compared with Module 5 droop data,
- PI simulation compared with P-only simulation,
- short explanation of why the one-lump model does or does not oscillate,
- windup thought-experiment answers,
- link to your GitHub modeling checkpoint.

### A3 Rubric

| Criterion | Points |
| --- | ---: |
| P-control droop and instability evidence is quantitative and reproducible | 2 |
| One-lump energy balance, steady state, time constant, parameters, and units are correct; interpretation explains why droop is needed, susceptibility as $P_u/H$, and dimensionless gain | 2 |
| P and PI cases use comparable conditions and quantitative transient metrics | 2 |
| Integral action, anti-windup, thermal lag, and a model limitation are explained | 2 |
| PDF, code, data links, and cited Git checkpoint are clear and on time | 2 |

### Oral Review Questions: PI Control

Use this PI-control question to check your understanding and prepare A3:

1. Why can integral action remove droop, and what is integral windup?

Also prepare the [Module 5 P-control questions](../lab-05/index.md#oral-review-questions-p-control)
and [Module 7 modeling questions](../lab-07/index.md#oral-review-questions-process-modeling).
The [A3 deadline and rubric](#a3-feedback-data-and-lumped-model-memo) are above.
