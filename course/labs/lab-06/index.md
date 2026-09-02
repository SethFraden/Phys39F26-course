# Module 6 Assignment: Modeling P And PI Temperature Control

## Purpose

Module 6 slows down the theory. Module 5 showed that proportional feedback reduces
steady-state error but can become unstable. Module 6 builds simple models that
explain those observations.

The goal is not to become fluent in Laplace transforms. The goal is to connect
thermal physics, feedback equations, and the data you measured from the TEC.

You will begin with algebra, then write a first-order time-domain model, then
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

- **Thermal capacitance**, `C`: how much heat is needed to change temperature.
- **Thermal resistance**, `R`: how strongly the object is thermally connected
  to its surroundings.
- **Heat-loss conductance**, `H = 1/R`: heat-loss rate per kelvin above ambient,
  in W/K.
- **TEC power coefficient**, `P_u`: thermal power per signed PWM count, in
  W/PWM.
- **Time constant**, `tau = R*C`: the approximate response time of a first-order
  thermal system.
- **Open-loop slope**, `S`: steady-state temperature change per PWM command.
- **P control**: command proportional to current error.
- **I control**: command proportional to accumulated error.
- **Windup**: integral term grows while the actuator is saturated.

## Before Class

Bring:

- your Module 4 steady-state `T` versus PWM data,
- your Module 5 droop versus `Kp` data,
- one Module 5 strip chart trace at a stable gain,
- one Module 5 strip chart trace near oscillation,
- your current Python plotting/modeling environment.

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

Begin with the First Law in rate form:

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

### Student Instructions: Code The Steady-State Model

Start by coding the steady-state open-loop relationship measured in Module 4:

```text
T = Tamb + S*u
```

where:

- `T` is steady-state temperature,
- `Tamb` is ambient temperature,
- `S` is the open-loop slope in °C/PWM,
- `u` is the signed PWM command.

For P-only feedback:

```text
u = Kp*(Tset - T)
```

Combine the two equations:

```text
T = Tamb + S*Kp*(Tset - T)
```

Solve for the steady-state error:

```text
droop = Tset - T = (Tset - Tamb)/(1 + S*Kp)
```

Use your own values of `S`, `Tamb`, `Tset`, and `Kp` to calculate predicted
droop. Compare the prediction with Module 5.

## Part 2: First-Order Thermal Model

Use a one-body thermal model:

```text
dT/dt = -(T - Tamb)/tau + B*u
```

Interpretation:

- `-(T - Tamb)/tau` pulls the block back toward room temperature,
- `B*u` is the heating or cooling rate caused by the TEC command,
- `tau` is the thermal time constant.

This model is deliberately simple. It treats the TEC/block/thermistor as one
effective thermal object.

## Part 3: Estimate `tau`

Use a temperature step from Module 4 or Module 5.

Use a trace in which every temperature value was calculated after averaging
between 100 and 1000 raw thermistor-voltage measurements, as required in Modules
2 through 5.

One practical method:

1. Identify the initial temperature, `T_initial`.
2. Identify the approximate final temperature, `T_final`.
3. Calculate 63 percent of the total change:

```text
T_63 = T_initial + 0.63*(T_final - T_initial)
```

4. Estimate `tau` as the time when the temperature first reaches `T_63`.

Record how uncertain your estimate is. The trace may not be a perfect
exponential.

## Part 4: Simulate Open-Loop Response

Write a short Python simulation of:

```text
dT/dt = -(T - Tamb)/tau + B*u
```

Use Euler integration:

```text
T_next = T + dt * (-(T - Tamb)/tau + B*u)
```

Simulate a constant PWM command and compare the simulated curve with one of
your measured open-loop traces.

## Part 5: Simulate P-Only Feedback

Replace the constant command with:

```text
u = Kp*(Tset - T)
```

Clamp `u` to the allowed PWM range.

Simulate several values of `Kp`. Plot:

- temperature versus time,
- PWM command versus time,
- final droop versus `Kp`.

Compare with Module 5. The first-order model should capture some trends, but it
may not reproduce oscillations.

## Part 6: Why The First-Order Model May Not Oscillate

If your first-order model does not oscillate, that is useful. It means one
thermal mass with instantaneous measurement and actuation is too simple.

The dimensional one-lump model is

\[
C\frac{dT}{dt}=P_u u-H(T-T_{\mathrm{amb}}).
\]

With P control,

\[
u=K_p(T_{\mathrm{set}}-T),
\]

so

\[
C\frac{dT}{dt}
=P_uK_pT_{\mathrm{set}}+HT_{\mathrm{amb}}
-(H+P_uK_p)T.
\]

First find the equilibrium temperature by setting \(dT/dt=0\):

\[
T_{\mathrm{eq}}
=\frac{P_uK_pT_{\mathrm{set}}+HT_{\mathrm{amb}}}
{H+P_uK_p}.
\]

The remaining error from the setpoint is the P-control droop:

\[
T_{\mathrm{set}}-T_{\mathrm{eq}}
=\frac{H(T_{\mathrm{set}}-T_{\mathrm{amb}})}
{H+P_uK_p}.
\]

Now define the displacement from equilibrium,

\[
\theta(t)=T(t)-T_{\mathrm{eq}}.
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
T(t)=T_{\mathrm{eq}}
+\left[T(0)-T_{\mathrm{eq}}\right]
\exp\!\left(-\frac{H+P_uK_p}{C}t\right)
}.
\]

Equivalently,

\[
T(t)=T_{\mathrm{eq}}
+\left[T(0)-T_{\mathrm{eq}}\right]e^{-t/\tau_{\mathrm{cl}}},
\qquad
\tau_{\mathrm{cl}}=\frac{C}{H+P_uK_p}.
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
\(T(t)-T_{\mathrm{eq}}\) retains its
initial sign while shrinking toward zero. The response therefore cannot cross
the equilibrium, overshoot, or oscillate. Increasing \(K_p\) decreases both
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

Integral control accumulates error:

```text
error_integral = error_integral + error*dt
u = Kp*error + Ki*error_integral
```

Simulate PI control for a stable `Kp`.

Compare P-only and PI simulations:

- final droop,
- time to approach setpoint,
- overshoot,
- sensitivity to saturation.

The main point is that integral action can reduce steady-state error, but it can
also create overshoot and windup.

### Why PI Can Be Underdamped

First call the controller's accumulated error \(q\). It is the time integral of
the error:

\[
q(t)=q(0)+\int_0^t e(t')\,dt'.
\]

Therefore

\[
\frac{dq}{dt}=e,
\qquad
u=K_p e+K_i q,
\qquad
e=T_{\mathrm{set}}-T.
\]

For an unsaturated PI controller at equilibrium, the temperature reaches the
setpoint and the integral term supplies the PWM needed to balance heat loss:

\[
T_{\mathrm{eq}}=T_{\mathrm{set}},
\qquad
q_{\mathrm{eq}}
=\frac{H(T_{\mathrm{set}}-T_{\mathrm{amb}})}{P_uK_i}.
\]

Now define the **two state variables as displacements from equilibrium**:

\[
\boxed{
\theta(t)=T(t)-T_{\mathrm{set}}
},
\qquad
\boxed{
z(t)=q(t)-q_{\mathrm{eq}}
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
equivalent time-constant model, the P and PI controller equations, the
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
- estimate of open-loop slope `S`,
- estimate of thermal time constant `tau`,
- open-loop simulation compared with one measured trace,
- P-only simulation compared with Module 5 droop data,
- PI simulation compared with P-only simulation,
- short explanation of why the first-order model does or does not oscillate,
- windup thought-experiment answers,
- link to your GitHub modeling checkpoint.

### A3 Rubric

| Criterion | Points |
| --- | ---: |
| P-control droop and instability evidence is quantitative and reproducible | 2 |
| One-lump energy balance, equilibrium, time constant, parameters, and units are correct | 2 |
| P and PI cases use comparable conditions and quantitative transient metrics | 2 |
| Integral action, anti-windup, thermal lag, and a model limitation are explained | 2 |
| PDF, code, data links, and cited Git checkpoint are clear and on time | 2 |
