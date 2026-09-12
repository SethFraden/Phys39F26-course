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

1. Lienhard and Lienhard, *A Heat Transfer Textbook*.
   - Section 1.3: read for energy-balance language and units.
   - Chapter 4, especially Section 4.5: read for transient response and thermal
     time constants.
   - Official free textbook site: [A Heat Transfer Textbook](https://ahtt.mit.edu)
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
| S11 | Read this assignment and the selected heat-transfer material | 90 minutes |
| S11 | Complete and check the guided one-lump derivation | 120 minutes |
| S11 | **Total associated with S11** | **3 hours 30 minutes** |
| S12 | Review PI control and windup; answer the preparation questions | 60 minutes |
| S12 | Prepare or revise the P/PI simulation for in-class comparison | 105 minutes |
| S12 | **Total associated with S12** | **2 hours 45 minutes** |
| S13 | Analyze matched P/PI results | 90 minutes |
| S13 | Write, check, commit, push, and submit A3 | 120 minutes |
| S13 | **Total associated with S13** | **3 hours 30 minutes** |

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

This equation does not directly describe the time dependence of heat. It is an
energy-conservation equation that predicts the time dependence of the lump's
temperature, \(T(t)\). Heat is energy being transferred; temperature describes
the thermal state of the lump.

Begin with the First Law in rate form; the change in the lump's energy with
time is the difference between the rate of putting heat in and taking heat out
of the lump:

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

Dimensional analysis identifies $C/H$ as the natural timescale; solving the
energy balance shows that it is specifically the exponential time constant.

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

Its damping ratio is

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

After your own P and PI simulations run, download
[the Module 6 P/PI lumped-model simulation](../../downloads/Lab_6_first_order_p_pi_simulation.py).
Save it in your project repository as
`python/Lab_6_first_order_p_pi_simulation.py`, then run it from the repository
root:

```bash
python python/Lab_6_first_order_p_pi_simulation.py
```

The supplied simulation displays the dimensional energy balance, the
equivalent measured-parameter form, the P and PI controller equations, the
predicted P droop, and the PI damping ratio. Use it to check your reasoning,
compare its predictions with your independently written model, and investigate
parameter changes. Do not substitute its plots for comparisons with your own
experimental data.

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
C4 oral questions; it is not a separate document to grade.

For the in-class modeling work, save the parameter set, units, initial
conditions, controller settings, saturation limits, exact command used to run
the model, open-loop comparison, matched P/PI plots, and residuals. Complete
the comparison table while the simulations and experimental traces are open.

### A3: Feedback Data And Lumped-Model Memo

- **Due:** Wednesday, October 14, at **6:00 PM**
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

### C4 Oral Questions: PI Control

This is the authoritative PI-control question for C4:

1. Why can integral action remove droop, and what is integral windup?

Also prepare the [Module 5 P-control questions](../lab-05/index.md#c4-oral-questions-p-control)
and [Module 7 modeling questions](../lab-07/index.md#c4-oral-questions-process-modeling).
The [C4 deadline and rubric](../../assessment.md#c4-feedback-controller-and-tec-process-model)
remain on the Assessment page.
