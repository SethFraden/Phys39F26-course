# Module 7, Part III: Rod Instrument And Stationary Fin

This is the experimental part of Module 7. It builds on [Part I: Thermal
Transport Foundations](../theory-bridge-chapter-1/index.md) and [Part II: Finite
And Infinite Rod Theory](../fin-design-derivation/index.md).

## Purpose

Part III has three priorities, in this order:

1. **Build the six-thermistor instrument.** This is the primary objective.
   Establish one TEC-base thermistor and five rod thermistors as a checked
   measurement system. Extend the Arduino and Python software so that all six
   temperatures are acquired, displayed, and recorded together. Use the raw
   readings by default when the six sensors agree within
   \(1^{\circ}\mathrm{C}\) in a common bath; apply calibration corrections only
   if that check fails.
2. **Understand heat transport along a long, thin cylinder.** Develop and
   understand the one-dimensional heat-transport equation, its boundary
   conditions, and the finite-length and radial-validity approximations.
3. **Measure and test the stationary temperature profile.** Measure the
   steady-state temperature as a function of position along the rod, then fit
   and compare the finite insulated-tip model and the semi-infinite exponential
   model using the measured sensor positions and residuals.

Part III is where the instrument is completed and used for the principal
Module 7 physics measurement. The theory from Parts I and II predicts the
stationary profile and provides the two models to test.

**Class-time priority.** Spend no more than one hour of class time beginning
the Part I and Part II theory. Finish that work at home and bring questions to
class. Use the rest of the laboratory time for Part III: build the six-channel
thermistor setup, check all six measurement chains in a common bath, develop
and test the Arduino and Python software that displays and records all six
temperatures, retain TEC temperature control, and measure the stationary
temperature profile for comparison with the finite and semi-infinite models.
Fit calibration corrections only if the common-bath check fails.

In Modules 1-6, one or two temperatures were enough to describe the TEC process.
The aluminum rod cannot be treated as one thermal lump. Its temperature depends
on position and time:

\[
T=T(x,t).
\]

In this module you will build and validate the multichannel rod instrument and
measure the stationary temperature profile along the rod. Record the complete
approach to steady state so that you can verify when the profile has settled and
observe qualitatively how a temperature disturbance spreads. The primary
physics measurement, however, is the stationary profile and its comparison with
the finite-rod and semi-infinite models. The sinusoidal Angstrom experiment
begins in Module 8.

### Thermistor Channels And Common-Bath Check

The Arduino Uno R3 has six analog input channels, `A0` through `A5`, feeding one
multiplexed 10-bit analog-to-digital converter. Use one channel for the
thermistor in the TEC base and the other five channels for five thermistors
along the rod. The converter samples the six channels in rapid sequence rather
than at exactly the same instant. This delay is negligible on the thermal
timescales measured here.

The purpose here is to assign each thermistor a permanent channel, check all
six measurement chains under a common temperature condition, and establish the
sensor map used for the non-oscillatory step response and stationary-fin
profile. Module 8 reuses the same validated sensor map for the oscillatory
Angstrom experiment. Calibration corrections are optional rather than the
default.
The rod has more thermistor holes than the five available rod channels, so the
five rod thermistors can be distributed among selected holes to obtain a useful
range of positions and temperatures. Holes in the first group are nominally
spaced at \(1/2\)-inch intervals; holes in the second group are nominally
spaced at \(1\)-inch intervals. Treat these as
orientation values only; measure and record the actual positions you use.

The course rod is **6061-T6 aluminum** with a nominal diameter of \(1/2\) inch,
or \(12.7\ \mathrm{mm}\). The **analysis base** at \(x=0\) is the first
thermistor hole in the rod, occupied by rod thermistor 1. It is not the physical
end of the rod and it is not the thermistor embedded in the TEC. Measure the
positions of the other four rod thermistors relative to this origin. Define
the analyzed length \(L\) as the distance from the first thermistor hole to the
rod tip. Also record the rod's overall physical length, diameter \(d\), and
their uncertainties. The TEC thermistor monitors the actuator, while the
measured temperature of rod thermistor 1 supplies the boundary condition
\(T(0,t)\) for the rod model.

Use one model-testing cycle throughout Part III:

1. **Predict:** use the Part I and Part II theory to predict the qualitative
   transient, the stationary profile, and the importance of the end and radius.
2. **Measure:** acquire synchronized, checked temperature data with the
   geometry and settings needed to interpret them.
3. **Compare:** fit the finite and semi-infinite models and inspect residuals,
   parameter values, and uncertainties.
4. **Judge:** state which assumptions the evidence supports and where the
   model is inadequate.

## Schedule And Due Work

| Session | In class | Due |
| --- | --- | --- |
| S16, Mon. Oct. 26 | Use no more than the first hour to begin Parts I and II and identify questions to finish at home. Then map and common-bath-check all six sensors, calibrating only if needed; develop and test the six-channel Arduino/Python display and recording system with TEC control; begin the stationary-profile run if the instrument is ready. | Module 7 home preparation |
| S17, Wed. Oct. 28 | Complete the stationary-profile measurement, retaining the full approach to steady state; fit and compare the finite-length and semi-infinite stationary profiles | **A4: finite-rod model and validity checks**; **C5: Rod instrument and data-acquisition chain** |

### In-Class Route

Complete the experimental work in this order:

1. **Phase 1:** wire and permanently label `TEC` and `T1`-`T5`.
2. **Phase 2:** display and record all six channels while retaining TEC control.
3. **Phase 3:** perform the common-bath check and complete the sensor map.
4. **Phase 4:** choose useful rod positions and acquire the stationary profile.
5. **Phase 5:** analyze the profile and test the finite and semi-infinite models.

## Outside-Class Workload Budget

| Session | Work | Planned time |
| --- | --- | ---: |
| S16 | Complete the required Part I and Part II reading route, including the selected Lienhard sections and derivation guide | 150 minutes |
| S16 | Begin A4: identify boundary conditions and organize the finite-length derivation | 75 minutes |
| S16 | **Total associated with S16** | **3 hours 45 minutes** |
| S17 | Complete and check the individual A4 calculations | 180 minutes |
| S17 | Prepare the sensor-map and common-bath check record | 45 minutes |
| S17 | **Total associated with S17** | **3 hours 45 minutes** |

The reading allocation includes time to follow the derivation, not merely read
the prose. Save all rod measurements during class; the outside-class budget is
for theory, analysis, documentation, and submission.

## Learning Objectives

The objectives below are listed in priority order. By the end of Module 7,
Part III, you should be able to:

1. Build and demonstrate the six-thermistor instrument: assign permanent
   channels to the TEC-base thermistor and five rod thermistors, check all six
   measurement chains in a common bath, apply calibration corrections only if
   required, and extend the Arduino and Python software to display and record
   synchronized temperatures with units, timestamps, sensor positions, and
   experimental metadata.
2. Explain and apply the one-dimensional heat-transport equation for a long,
   thin cylinder, then use the finite-length solution and transverse Biot
   number to make separate quantitative decisions about whether the far end
   and radial temperature variation may be neglected.
3. Measure the stationary temperature profile along the rod, fit finite-length
   and semi-infinite stationary-fin models, examine their residuals, and
   interpret the fitted decay coefficient and decay length.
4. Explain what the steady experiment can determine and why it cannot determine
   the thermal conductivity and side heat-transfer coefficient separately.
5. Use the recorded approach to steady state to justify the selected stationary
   interval and explain qualitatively why more distant sensors respond later
   and with smaller temperature changes.

## Part III Vocabulary And Notation

Review the [foundational vocabulary in Part
I](../theory-bridge-chapter-1/index.md#module-7-vocabulary-and-notation) and the
[fin-model vocabulary in Part
II](../fin-design-derivation/index.md#part-ii-vocabulary-and-notation). The
terms below connect that theory to the experiment and its analysis.

| Term | Meaning |
| --- | --- |
| Temperature field, \(T(x,t)\) | Temperature as a function of both position along the rod and time. |
| Environmental temperature, \(T_\infty\) | The temperature of the environment far from the rod. In this experiment, it is the room temperature measured away from the heated apparatus. |
| Excess temperature, \(\theta(x,t)=T(x,t)-T_\infty\) | Rod temperature measured relative to the environment. |
| Thermal diffusivity, \(\alpha=k/(\rho c)\) | The coefficient controlling axial spreading in the Part III model; units m\(^2\)/s. This is Lienhard's notation. |
| Side-loss rate, \(\nu=hP/(\rho cA)\) | The fractional rate, in s\(^{-1}\), at which side convection removes excess thermal energy in the one-dimensional model. |
| Decay coefficient, \(m=\sqrt{hP/(kA)}=\sqrt{\nu/\alpha}\) | The spatial decay rate of the stationary profile; \(1/m\) is the decay length. |
| Sensor map | A record of each channel name, thermistor position, coordinate origin and direction, and position uncertainty. |
| Common-bath check | A comparison under a common temperature condition used to identify sensor offsets or other channel differences. If the full spread of the six readings remains below \(1^{\circ}\mathrm{C}\), use the raw readings without calibration corrections. |
| Baseline | Measurements made before the imposed temperature change, used to establish room temperature and initial sensor readings. |
| Step response | The measured evolution of \(T(x,t)\) after the base-temperature command changes. |
| Boundary condition | The measured or prescribed behavior at a boundary. For the rod model, the measured temperature of rod thermistor 1 at the first hole is the boundary condition \(T(0,t)\); the TEC setpoint and TEC-thermistor temperature describe the actuator that creates it. |
| Stationary profile | The position-dependent temperature after changes with time have become negligible according to a stated criterion. |
| Model fit | Estimation of model parameters by comparing a predicted curve with measured data. |
| Residual | Measured value minus model prediction at the same position or time. Residual structure can reveal model inadequacy. |
| Uncertainty | A quantitative estimate of the plausible range of a measured or fitted result. |
| Metadata | Information needed to interpret and reproduce a run, including units, timestamps, channel labels, geometry, settings, and experimental notes. |

## Reading And Preparation

1. Read selectively in [Lienhard and Lienhard, *A Heat Transfer Textbook*](../../references/lienhard-heat-transfer-textbook-v6.pdf),
   Section 1.3, pp. 11-26, following the reading guide in Part I.
2. Review [Module 7, Part I: Thermal Transport Foundations](../theory-bridge-chapter-1/index.md).
3. For the S16 lecture and S17 guided study, read Lienhard Section 4.5,
   textbook pp. 163-173. Work through the derivation rather than reading only
   the final formulas.
4. Use [Fin Design: From A Finite Rod To An Infinite Rod](../fin-design-derivation/index.md)
   as the equation-by-equation guide to Lienhard Eqs. (4.27)-(4.51).
5. Complete `A4`, including Lienhard Problems 1.3, 4.12,
   and 4.20. Problem 1.3 is assigned in
   [Module 7, Part I](../theory-bridge-chapter-1/index.md#a4-part-i-lienhard-problem-13).

## Model

Part II set the energy-storage term to zero to obtain the stationary fin
equation. We now restore that term while retaining distributed side cooling,
so the model describes both the transient response and the stationary profile
that it approaches.

Let

\[
\theta(x,t)=T(x,t)-T_\infty,
\]

where $T_\infty$ is the temperature of the environment far from the rod. For
the course experiment, $T_\infty$ is the room temperature measured away from
the heated apparatus.

For a uniform rod with cross-sectional area $A$, perimeter $P$, density $\rho$,
specific heat $c$, thermal conductivity $k$, and side heat-transfer coefficient
$h$, conservation of energy gives

\[
\rho c A\frac{\partial\theta}{\partial t}
=kA\frac{\partial^2\theta}{\partial x^2}-hP\theta.
\]

Every term has units of power per unit length, watts per meter. Dividing by
$\rho cA$ gives

\[
\frac{\partial\theta}{\partial t}
=\alpha\frac{\partial^2\theta}{\partial x^2}-\nu\theta,
\qquad
\alpha=\frac{k}{\rho c},
\qquad
\nu=\frac{hP}{\rho c A}.
\]

Here $\alpha$ has units of square meters per second and $\nu$ has units of
inverse seconds.

At steady state,

\[
\frac{d^2\theta}{dx^2}-m^2\theta=0,
\qquad
m^2=\frac{hP}{kA}=\frac{\nu}{\alpha}.
\]

This second-order equation requires two boundary conditions. For the analyzed
section, rod thermistor 1 supplies the measured temperature at the analysis
base \(x=0\), and the tip is treated as insulated. Part II then gives the
complete finite-rod profile

\[
\frac{\theta(x)}{\theta(0)}
=\frac{\cosh[m(L-x)]}{\cosh(mL)}.
\]

### Explore The Finite-Rod Model

Open the [interactive TEC and finite-rod simulator](../../simulators/tec-rod-control/),
developed by Tim Hebert, and use a constant setpoint. The simulator numerically evolves the
one-dimensional transient conduction equation with side heat loss, a finite
rod, and a dynamic TEC boundary. Move the probe along the rod and observe both
the approach to steady state and the final spatial profile. Use it to predict
which parts of the measured rod should be sensitive to the far-end boundary
condition before fitting the experimental data.

**Suggested high-gain exploration.** Place the probe at $x=0$, use
proportional control only, and compare successively larger values of $K_p$,
for example 8, 80, and 800. At modest gain, an overshoot can decay. At large
gain, the simulator can instead settle into a sustained oscillation while the
PWM repeatedly saturates or reverses. This oscillation is produced by the
dynamic TEC actuator included in the simulator; it is absent from the ideal
one-lump P-control model. Identify approximately where the qualitative change
occurs, and compare the oscillation period with the thermal response times
visible in the TEC and rod. Then hold $K_p=800$ fixed and move the probe from
$x=0$ to a few positions farther along the rod, resetting between trials.
Observe qualitatively that the oscillation frequency generally increases as
the probe is moved closer to the TEC.

<details markdown="1">
<summary>What physical model is inside this simulator?</summary>

The rod is divided into finite-difference elements that obey the
one-dimensional transient heat equation

\[
\rho cA\frac{\partial T}{\partial t}
=kA\frac{\partial^2T}{\partial x^2}-hP(T-T_\infty).
\]

The simulator does **not** substitute the analytical cosh or exponential
solution. It replaces the axial second derivative with centered finite
differences on 24-100 rod elements and advances the resulting coupled ordinary
differential equations with a 0.01 s numerical substep. The TEC balances and
thermistor equation are advanced with the same substep, while the controller
updates every 0.1 s. The analytical stationary profiles derived in Part II are
therefore predictions that can be compared with the numerical long-time limit,
not formulas built into the simulation.

The far tip has zero axial heat flux. The driven end is coupled to a dynamic
TEC model. It is not an ideal heat source. The model has a cold-side
temperature $T_c$ and hot-side temperature $T_h$, with separate heat
capacities $C_c$ and $C_h$. A signed duty command $u$ applies the averaged
voltage $V=uV_s$ to the TEC. The code calculates the signed current from this
voltage, the TEC electrical resistance, and the Seebeck back-emf, then limits
the current to the allowed range.

Using the conventional current $I_c$ that is positive in the cooling
direction, the heat absorbed at the cold side and rejected at the hot side are

\[
\dot Q_c
=S I_c T_{c,K}-\frac{1}{2}I_c^2R-K_{\mathrm{TEC}}(T_h-T_c),
\]

\[
\dot Q_h
=S I_c T_{h,K}+\frac{1}{2}I_c^2R-K_{\mathrm{TEC}}(T_h-T_c).
\]

Here $S$ is the effective Seebeck coefficient, $R$ is the electrical
resistance, $K_{\mathrm{TEC}}$ is the passive thermal conductance through the
TEC, and the temperatures marked $K$ are absolute temperatures. The terms
proportional to $SI_cT$ describe Peltier transport, the $I_c^2R/2$ terms split
Joule heating between the two faces, and the final terms describe ordinary
conduction from the hot face toward the cold face.

The two TEC temperatures obey separate energy balances:

\[
C_c\frac{dT_c}{dt}
=-\dot Q_c+G_c[T(0,t)-T_c]+G_{\mathrm{leak}}(T_\infty-T_c),
\]

\[
C_h\frac{dT_h}{dt}
=\dot Q_h-\frac{T_h-T_\infty}{R_{\mathrm{hs}}}.
\]

The contact conductance $G_c=h_{\mathrm{contact}}A$ couples the cold-side plate
to the first finite-difference element of the rod. The hot side loses heat to
the room through the heat-sink resistance $R_{\mathrm{hs}}$, while
$G_{\mathrm{leak}}$ represents an additional cold-side leak to the room. The
default parameters approximate a TEC1-12706-type device: $S=0.0513$ V/K,
$R=1.861\ \Omega$, $K_{\mathrm{TEC}}=0.560$ W/K, $C_c=12$ J/K,
$C_h=180$ J/K, $R_{\mathrm{hs}}=0.55$ K/W, and a 12 V supply. These values are
model parameters, not measurements of the particular classroom TEC.

The rod is the distributed thermal load on this two-state actuator. Its first
element exchanges heat with $T_c$ through $G_c$; the remaining elements
conduct heat axially and lose heat from their sides. The movable thermistor
measures the local rod temperature through a first-order sensor response with
a 2 s time constant. The controller samples that measured temperature every
0.1 s and limits the signed PWM command to the range from $-100\%$ to
$+100\%$.

**High-gain P-control exploration.** Put the probe at $x=0$, turn off I and D,
and keep all settings except $K_p$ fixed. Reset the simulation for each trial.
Begin with $K_p=8$, then try $K_p=80$ and $K_p=800$, adding intermediate
values to locate the transition. For each run, decide whether the response is
monotonic, shows damped oscillations, or reaches a sustained oscillation.
Record whether the PWM remains proportional or spends most of each cycle at
$+100\%$ and $-100\%$, and compare the oscillation period with the visible TEC
and rod response times.

Next set $K_p=800$ and move the probe between $x=0$ and a few downstream
positions. Reset at each position and compare only the qualitative oscillation
rate. The oscillations are generally faster near the TEC and slower when
feedback is based on a more distant temperature.

For P control,

\[
u_{\mathrm{unsat}}=K_p[T_{\mathrm{set}}-T_s],
\qquad
u=\operatorname{sat}(u_{\mathrm{unsat}}).
\]

As $K_p\rightarrow\infty$, almost any nonzero error drives the command to one
limit or the other. This is the **bang-bang limit**: full heating for one sign
of the error and full cooling for the other. Reversing the command at the
setpoint does not reverse the temperature immediately. Energy already stored
in the TEC faces and rod keeps the temperature moving, so the system
overshoots, reverses, and may form a bounded limit cycle.

The phase lag is cumulative. The separate $C_c$ and $C_h$ states give the TEC
its own two-lump actuator lag. Finite contact conductance, the distributed
diffusion modes of the rod, the thermistor response, and digital sampling add
further lag. Placing the probe at $x=0$ removes the additional propagation
delay associated with measuring farther down the rod, but it does not remove
the TEC dynamics or the rod's distributed thermal load. At sufficiently high
loop gain, enough phase lag can make nominally negative feedback reinforce an
oscillation at some frequency; PWM saturation then bounds its amplitude. This
behavior is absent from the elementary one-lump P-control model, whose single
closed-loop mode remains stable for positive parameters.

Moving the probe downstream adds thermal-diffusion delay and attenuates the
measured oscillation. The controller therefore reacts to an older, weaker
indication of what the actuator has done; in this simulator the sustained
oscillations generally become slower as the probe moves away from the TEC. The
exact distance scaling is not the point here because the TEC, rod, sensor, and
saturation dynamics all contribute. The practical control-design lesson is
more general: place the feedback sensor close to the actuator when the goal is
fast, stable regulation, unless the temperature at a remote location is itself
the quantity that must be controlled.

The model is intentionally idealized. It does not include every contact,
temperature dependence, electronic delay, or three-dimensional heat-flow
path in the physical apparatus.

</details>

When the far end has negligible influence over the measured region, this
finite profile approaches the semi-infinite approximation

\[
\theta(x)=\theta_0 e^{-mx}.
\]

The fitted $m$ quantifies the competition between axial conduction and side
loss. It does **not** determine $k$ and $h$ separately. The periodic Angstrom
experiment in Module 8, Part I, supplies the second independent measurement.

## Before The Experiment: Model-Validity Checks

### Length: Solve It First

For the section of rod extending a distance \(L\) from the first thermistor
hole to the insulated tip, the exact normalized stationary solution is

\[
\Theta_{\mathrm{finite}}(x)
=\frac{\theta(x)}{\theta(0)}
=\frac{\cosh[m(L-x)]}{\cosh(mL)}.
\]

The semi-infinite model is the limiting expression

\[
\Theta_\infty(x)=e^{-mx}.
\]

Calculate the relative error at every sensor position:

\[
\epsilon_T(x)=
\frac{\left|\Theta_{\mathrm{finite}}(x)-\Theta_\infty(x)\right|}
{\left|\Theta_{\mathrm{finite}}(x)\right|}.
\]

State an acceptable error before deciding whether the far end may be ignored.
A reasonable starting criterion is \(\epsilon_T<5\%\) at every sensor used in
the analysis, but record and justify a different threshold if the intended
measurement requires one. The product \(mL\) is useful, but the answer also
depends on which sensor and which observable you use.

### Radius: Check The Transverse Biot Number

For a circular rod,

\[
\mathrm{Bi}_{\perp}=\frac{h(A/P)}{k}=\frac{hR}{2k}.
\]

This validity check is performed in two stages. **Before the experiment**, make
a provisional estimate using a literature value or range for the conductivity
of 6061-T6 aluminum and the measured rod geometry. For natural convection from
the half-inch rod in still room air, use the planning value

\[
h=10\ \mathrm{W\,m^{-2}K^{-1}}.
\]

Treat this as a provisional convection value, not as a measurement of \(h\).

The small-Biot condition \(\mathrm{Bi}_{\perp}\ll1\) means radial conduction
is fast enough that a cross section can be represented by one temperature.
Before the experiment, estimate \(\mathrm{Bi}_{\perp}\) using the rod radius
and \(h=10\ \mathrm{W\,m^{-2}K^{-1}}\), together with a justified literature
value or range for \(k\). At this stage, proceed with the
one-dimensional model under the **provisional assumption** that
\(\mathrm{Bi}_{\perp}\ll1\). You cannot yet test that assumption using the
measured profile because \(m\) has not yet been measured.

**After the experiment**, return to this question using the fitted stationary
profile. This is a measurement-based self-consistency check rather than another
estimate of \(h\). The fitted spatial decay coefficient obeys

\[
m^2=\frac{hP}{kA},
\]

so

\[
\frac{h}{k}=m^2\frac{A}{P},
\qquad
\boxed{\mathrm{Bi}_{\perp}
=m^2\left(\frac{A}{P}\right)^2}.
\]

For a circular rod, \(A/P=R/2=d/4\), and therefore

\[
\boxed{\mathrm{Bi}_{\perp}=\left(\frac{mR}{2}\right)^2
=\left(\frac{md}{4}\right)^2}.
\]

Use the following measurement procedure:

1. Calculate \(\theta_i=T_i-T_\infty\) from the stationary temperatures.
2. Fit the **finite-length** profile first to obtain \(m\) and its uncertainty.
   This avoids assuming the semi-infinite limit before testing it.
3. Use the measured diameter and the fitted \(m\) to calculate
   \(\mathrm{Bi}_{\perp}\). Propagate the uncertainties in \(m\) and \(d\).
4. Decide whether \(\mathrm{Bi}_{\perp}\ll1\) adequately supports the
   assumption of a uniform temperature across each cross section.

This final calculation is a **self-consistency check**, not a logically
independent proof: the one-dimensional profile used to fit \(m\) already
assumes negligible radial temperature variation. If the fitted value gives
\(\mathrm{Bi}_{\perp}\ll1\), the assumption used at the beginning is
self-consistent. If it does not, reject the one-dimensional interpretation of
the fitted \(m\); a model with radial temperature variation would be required.

The same fitted \(m\) also completes the length check above. Calculate \(mL\)
and evaluate \(\epsilon_T(x_i)\) at every sensor position. If the finite and
semi-infinite profiles differ by less than your stated criterion throughout
the measured region, the semi-infinite approximation is adequate there. If
not, retain the finite-length solution. Thus \(\mathrm{Bi}_{\perp}\) tests the
radial approximation, while \(mL\) and \(\epsilon_T(x_i)\) test whether the far
end can be ignored; they are separate conclusions obtained from the same fit.

### A4: Finite-Rod Model And Validity Checks

`A4` is a 10-point individual written assignment based on Module 7, Parts I
and II. It does not require temperature-profile data from Part III. Use the
measured rod geometry and your planned sensor positions, together with a
literature range for \(k\) and the provisional value
\(h=10\ \mathrm{W\,m^{-2}K^{-1}}\)
given above. These calculations are predictions to record before heating the
rod; they are not the final measurement-based validity checks. Submit one PDF
organized under the following four headings. Show units and dimensional checks
throughout.

**Part 1. Apply Fourier's law.** Complete Lienhard Problem 1.3 as assigned in
[Part I](../theory-bridge-chapter-1/index.md#a4-part-i-lienhard-problem-13).
Show how Fourier's law produces each result, include units, and identify any
physically unreasonable result.

**Part 2. Build the stationary finite-rod model.** Starting from conservation
of energy, Fourier's law, and Newton's law of cooling, derive the stationary
fin equation with side heat loss. Follow the finite-fin solution in Lienhard
Section 4.5, showing the principal steps from the differential equation to the
solution. State the two boundary conditions and explain what each means
physically.

**Part 3. Make a provisional finite-length prediction.** Complete Lienhard
Problem 4.12 to obtain the semi-infinite limit. Use Example 4.8 and Problem
4.20 to quantify the effect of approximating the tip boundary condition. From
the provisional value of \(h\) and literature range for \(k\), calculate a range for
\(m\), then calculate \(mL\) and \(\epsilon_T(x)\) at every planned course-rod
sensor position. State whether you expect the course rod to be adequately
semi-infinite over the measured region, and state the positions, parameter
ranges, and error criterion on which this prediction depends.

**Part 4. Make a provisional one-dimensional prediction.** Calculate a range
for \(\mathrm{Bi}_{\perp}\) using the same provisional value of \(h\) and
literature range for \(k\). State whether you expect each cross section to
be represented adequately by one temperature. Do not combine this radius
conclusion with the finite-length conclusion from Part 3.

Then answer this brief application question: compare the same electronic heat
sink in still air and in forced airflow. Which case should have the larger
convective coefficient \(h\), and how should the larger \(h\) change the decay
length \(1/m\)?

The [submission details and rubric](#a4-submission-and-rubric) appear near the
end of this page.

### Prediction Record Before Heating

Before applying heat to the course rod, record the provisional values of
\(\mathrm{Bi}_{\perp}\), \(mL\), and \(\epsilon_T(x)\) at every sensor.
Predict:

1. the order in which the sensors will respond to a base-temperature step,
2. how the response amplitude will change with distance from the base,
3. the qualitative shape of the stationary temperature profile, and
4. whether the measured region should reveal the finite tip.

Use the measured rod geometry and the sensor positions you initially plan to
use. If the placement pilot leads you to move a sensor, preserve the original
prediction and repeat the calculation using the final measured position.
Return to these predictions after fitting the stationary data and state which
were supported by the evidence.

## Phase 1: Wire And Label The Six Thermistors

Build the complete measurement circuit before modifying the software or
preparing the common bath.

1. Prepare six thermistors using **26 AWG paired insulated wire** for the sensor
   leads. Separate the pair near the thermistor and insulate the two solder
   joints individually so they cannot touch. Use the heat-shrink tubing
   specified and supplied by the instructor. Slide both pieces onto the wires
   before soldering, keep the joints compact, and stagger the joints so the
   finished end is not unnecessarily bulky.

   At the breadboard end, terminate the flexible 26 AWG pair with short
   **22 AWG solid-wire pigtails** so the connections are reliable in the
   solderless breadboard. Use a meter to measure the actual resistance of each
   nominal
   \(100\ \mathrm{k}\Omega\) fixed resistor before it is connected in its
   voltage divider, and record the measured value with its channel assignment.
   Follow the established thermistor voltage-divider circuit; do not change
   the TEC power or safety wiring.
2. Label the TEC-base thermistor `TEC` and the five rod thermistors `T1`
   through `T5`. Use durable, water-resistant labels attached securely to the
   dry portions of the leads. The labels must survive handling, the common-bath
   check, installation, and the rest of the semester without falling off or
   moving to another lead.
3. Assign `TEC` to `A0` and `T1` through `T5` to `A1` through `A5`, unless your
   documented apparatus requires a different assignment. Record every sensor,
   analog input, divider, and wire color in the sensor map.
4. Check every connection for exposed conductors, loose joints, and accidental
   shorts before powering the Arduino. Keep the TEC power disabled during the
   first sensor tests.

Photograph the labeled, wired measurement chain before proceeding. From this
point onward, keep each physical thermistor paired with its assigned divider,
Arduino input, software label, and CSV column.

## Phase 2: Develop The Six-Channel Display And Recording Software

Keep the tested Module 6 files unchanged as a working checkpoint. Make new
Module 7 copies of both the Arduino sketch and Python GUI, give the copies
clear Module 7 filenames, and extend those copies for the rod experiment. For
example, use `arduino/module_07_rod_controller/module_07_rod_controller.ino`
and `python/module_07_rod_acquisition_gui.py` in your repository. The TEC-base
thermistor remains the feedback and safety sensor. The five rod thermistors
are additional measurement channels; they do not enter the PI-control law.

Develop and test the software in the steps below. Keep each step working
before asking Copilot to make the next change. Copilot may write code, but you
are responsible for checking the pin assignments, serial interface, units,
safety behavior, and saved data.

Do not begin the hot-water common-bath check until the Arduino and Python software
can display and record all six correctly labeled channels.

### Step 2A: Extend The Arduino Measurement

Use all six Uno analog inputs. Unless your documented wiring requires a
different assignment, use `A0` for the TEC-base thermistor and `A1` through
`A5` for rod thermistors 1 through 5. The Uno has one analog-to-digital
converter and selects the six inputs sequentially. Read and average each
channel, then send all six temperatures together in one measurement record.
The resulting time offsets between channels are negligible compared with the
rod's thermal response, but the Arduino time must be measured and transmitted
with every record.

The revised sketch must:

- retain the existing PI control, zero-PWM startup, H-bridge pin assignments,
  temperature limit, and hardware-safety instructions,
- use the TEC-base thermistor alone for feedback and the software temperature
  limit,
- calculate all six temperatures with the same thermistor conversion,
- label every transmitted field unambiguously,
- emit exactly one complete measurement record per acquisition cycle, and
- continue accepting the existing commands from the Python GUI.

Use a stable serial record such as

```text
DATA,time_s,tec_C,rod1_C,rod2_C,rod3_C,rod4_C,rod5_C,pwm,heat_cool,setpoint_C,safety
DATA,12.50,23.41,23.38,23.36,23.34,23.31,23.29,120,1,45.00,OK
```

The first line is a header printed once at startup; each later `DATA` line is
one measurement. Status and error messages must not begin with `DATA`. This
distinction lets both Python and the serial microSD logger recognize valid
records without confusing them with diagnostic text.

<details markdown="1">
<summary>Suggested Copilot prompt: six-channel Arduino acquisition</summary>

```text
Inspect the working Module 6 Arduino TEC-controller sketch that is open in VS
Code. First copy it to a new Module 7 sketch named
arduino/module_07_rod_controller/module_07_rod_controller.ino. Leave the
Module 6 file unchanged and edit only the new Module 7 copy. Preserve its PI
control, serial-command parser, H-bridge pins, zero-PWM startup, software
temperature limit, and all safety behavior.

Use A0 for the TEC-base thermistor and A1-A5 for rod thermistors 1-5. The A0
temperature must remain the only temperature used by the PI controller and
software safety limit. Read and average all six analog channels and convert
each reading with the sketch's existing thermistor-conversion function. Keep
the number of averages as a named constant. Record the Arduino elapsed time
after the six measurements have been acquired.

At startup, print this header once:
DATA,time_s,tec_C,rod1_C,rod2_C,rod3_C,rod4_C,rod5_C,pwm,heat_cool,setpoint_C,safety

For every acquisition cycle, print exactly one comma-separated line beginning
with DATA and containing those fields in that order. Diagnostic, command-ack,
and error lines must not begin with DATA. Keep accepting the existing Python
commands without changing their format. Comment the new pin definitions,
six-channel acquisition loop, and serial-output block for an Arduino beginner.
After editing, summarize every function and line of control logic that you
preserved unchanged.
```

</details>

Before connecting TEC power, test this sketch with Serial Monitor. Warm one
thermistor at a time with your fingers and verify that only its named column
changes. Confirm that the Arduino starts with PWM zero and still responds to a
zero-power command. Close Serial Monitor before opening the Python GUI because
only one program can own the serial port at a time.

### Step 2B: Extend The Python Display And Raw-Data Record

Modify the Module 6 GUI so that it parses the new `DATA` record and displays
six simultaneous temperature traces. Retain the existing setpoint, controller,
PWM, and safety displays. Give each trace a stable label and color, make the
TEC-base trace visually distinct, and provide checkboxes or a legend that
makes crowded plots readable.

Every accepted record must be written to a new CSV file with at least these
columns:

```text
time_s,tec_C,rod1_C,rod2_C,rod3_C,rod4_C,rod5_C,pwm,heat_cool,setpoint_C,safety
```

These are raw measured temperatures. Do not replace them with calibrated
values. Reject incomplete or malformed lines without stopping the program,
flush saved data regularly, and never silently overwrite an existing run.

<details markdown="1">
<summary>Suggested Copilot prompt: six-temperature GUI and CSV logger</summary>

```text
Inspect both the new Module 7 Arduino sketch and my working Module 6 PySide6
and pyqtgraph TEC-control GUI. First copy the Module 6 GUI to a new file named
python/module_07_rod_acquisition_gui.py. Leave the Module 6 file unchanged and
edit only the new Module 7 copy. Do not create a different controller or change
the Arduino command format. Preserve all PI controls, PWM and direction
displays, serial command sending, safety display, and zero-output stop
behavior.

Parse only complete Arduino lines beginning with DATA. The fields are:
time_s, tec_C, rod1_C, rod2_C, rod3_C, rod4_C, rod5_C, pwm, heat_cool,
setpoint_C, and safety. Ignore headers, acknowledgments, diagnostics, and
malformed lines without crashing.

Plot TEC and rod1-rod5 temperatures together against Arduino time. Give every
trace a fixed label and color and make the TEC trace thicker than the rod
traces. Add live numerical displays for all six temperatures. Preserve the
existing rolling-window behavior and controls.

Write every accepted raw record to a new CSV file with exactly those column
names. Do not apply calibration corrections and do not overwrite an existing
file; create a timestamped filename or require a new filename. Flush the file
regularly so a long run is not lost if the GUI closes unexpectedly. Add a
visible count of accepted and rejected serial lines. Keep the code readable
for a Python beginner and comment the parser, data storage, CSV writing, and
plot updates. At the end, explain how I can verify that every plotted trace is
being written to the correct CSV column.
```

</details>

Test with TEC power off. Compare several consecutive Arduino `DATA` records
with the corresponding Python numerical display and CSV rows. The field order,
values, and units must agree before the program is used for the common-bath
check.

### Step 2C: Integration Check Before The Common-Bath Test

Demonstrate the complete measurement chain before collecting the cooling-bath
record:

1. Show that warming one sensor changes only its assigned Arduino and Python
   channel.
2. Verify that one Arduino `DATA` line, one set of displayed values, and one
   saved CSV row agree.
3. Disconnect one rod thermistor temporarily and verify that the fault is
   visible without defeating the TEC-base safety shutdown.
4. Restart both programs and confirm that PWM begins at zero and that a new
   data file is created.
5. Record the Arduino-sketch and Python-GUI filenames and their Git commit hash
   in the sensor map.

## Phase 3: Common-Bath Check And Sensor Map

Complete these tasks in order. Do not prepare the hot water until Phases 1 and
2 are complete.

1. Confirm that the six thermistors are securely labeled `TEC` and `T1`
   through `T5`, wired to their permanent channels, and documented in the
   sensor map.
2. Demonstrate that the Arduino and GUI display all six temperatures and save
   them in six correctly labeled CSV columns.
3. Open the common-bath popup below and perform the check. Display all six
   temperatures simultaneously and observe them after the mixed bath has
   settled at several temperatures.
4. At each observation, calculate the full spread
   \(T_{\max}-T_{\min}\) across the six thermistors. If the spread remains less
   than \(1^{\circ}\mathrm{C}\), record that the sensors passed and apply no
   calibration corrections or calibration-specific GUI changes. This is the
   default outcome. If the spread reaches or exceeds
   \(1^{\circ}\mathrm{C}\), continue to the subsequent Record/Pause and fitting
   steps in the popup.
5. After the common-bath check, record the rod material as 6061-T6 aluminum.
   Measure its diameter \(d\), overall physical length, and analysis length
   \(L\) from the first thermistor hole to the tip. Calculate its
   cross-sectional area \(A\) and perimeter \(P\) in SI units. Install rod
   thermistor 1 in the first rod hole and define that hole as the analysis base
   \(x=0\). Measure the other four rod-sensor
   positions and the tip relative to this origin, so that the tip is at (x=L).
   Estimate the uncertainty of every position and of \(L\).
6. Save a diagram or photograph showing the permanent sensor labels, Arduino
   channel assignments, coordinate direction, and measured rod positions.

<details class="note" markdown="1">
<summary>Common-bath procedure and optional relative calibration</summary>

### Common-Bath Check

The rod experiment measures temperature differences and spatial temperature
gradients. It does not require an absolute temperature calibration. It does
require a common-bath check so that a large channel-to-channel difference is
not mistaken for a temperature gradient along the rod.

The default is **not** to fit or apply calibration corrections. If the full
spread of all six readings remains below \(1^{\circ}\mathrm{C}\) at every
retained bath temperature, document that result and use the raw readings. Use
the **TEC** thermistor as the reference and continue to the optional correction
steps only if this criterion fails.

**Step 1. Confirm the Phase 1 prerequisites.** Perform the check before
installing the thermistors in the apparatus. Confirm that `TEC` and `T1`-`T5`
retain their secure, water-resistant labels and that only their waterproof
sensing ends will be immersed.

**Step 2. Confirm the Phase 2 prerequisites.** Use the permanent voltage
dividers, Arduino inputs, acquisition code, and sample rate. Confirm that the
GUI displays and records six correctly labeled channels, then warm one sensor
at a time to verify its display and CSV column.

**Step 3. Heat the water.** Put water in a glass beaker and warm the beaker in
the microwave. Only the beaker and water go into the microwave; never microwave
the thermistors, wires, or any electrical hardware. Swirl the beaker carefully
after heating so that the water temperature is reasonably uniform. Handle the
hot glass and water cautiously. The calibration range should remain below
approximately \(60^{\circ}\mathrm{C}\).

**Step 4. Prepare the common bath.** Pour the warm water from the glass beaker
into a stable Styrofoam cup. Place all six waterproof sensing ends close
together in the water. Keep labels, electrical joints, connectors, and exposed
conductors dry, and do not allow the sensing ends to touch the cup walls or
bottom. Place the meter's thermocouple probe near the six sensing ends without
allowing it to touch them or the cup.

**Step 5. Mix and observe.** Run the basic six-temperature GUI. Gently swirl
the cup or stir the water so that every sensor experiences the same bath
temperature. Watch the six live traces and numerical readings. After mixing,
allow any motion-induced fluctuations to settle. If one trace remains much
noisier than the others, check its connection before using the readings.

**Step 6. Decide whether calibration is needed.** At several bath temperatures
spanning the range expected in the rod experiment, mix the water, allow the
display to settle, and note the six simultaneous readings and the thermocouple
temperature. Calculate \(T_{\max}-T_{\min}\). If the spread remains less than
\(1^{\circ}\mathrm{C}\), save a screenshot or short check record, state that no
correction is required, and stop here. Do not add Record/Pause code merely for
this check.

If the spread reaches or exceeds \(1^{\circ}\mathrm{C}\), continue with the
remaining steps.

**Step 7. Only if needed, add Record/Pause.** Extend the GUI with a clearly
labeled **Record/Pause** control. Live numerical values and plots must continue
updating in both states. In **Record**, append each accepted `DATA` record to
the calibration CSV. In **Pause**, append no temperature rows, allowing the
bath to be mixed and the readings to settle without adding those transients to
the fitting data. Start in Pause, display the current state prominently, flush
the file whenever recording is paused, and preserve the continuous Arduino
timestamp so that gaps in the saved record are unambiguous.

<details markdown="1">
<summary>Suggested Copilot prompt: add Record/Pause only after the check fails</summary>

```text
The six-temperature Arduino acquisition and Python GUI already work. The
common-bath check found a spread of at least 1 degree C, so modify the existing
Module 7 GUI to support calibration data collection. Do not change the Arduino
code, serial format, controller, safety behavior, live numerical displays, or
live plots.

Add a prominent Record/Pause button that controls only CSV writing. Start in
Pause. While paused, continue parsing and plotting all six temperatures but do
not append DATA rows. While recording, append every accepted DATA row to the
calibration CSV. When recording resumes, continue using Arduino time without
resetting it. Show the current state clearly and flush the file whenever the
state changes to Pause.

Comment the new state variable, button callback, and conditional CSV-writing
logic for a Python beginner. Explain how to verify that the display continues
in Pause, the CSV row count remains fixed in Pause, and recording resumes
without resetting Arduino time.
```

</details>

**Step 8. Collect quiet fitting intervals.** Use the **TEC** channel as the
reference. At several temperatures, keep the GUI paused while mixing the bath
and waiting for the displayed readings to settle. Press **Record** and retain
at least 60 seconds of simultaneous data. Record the thermocouple temperature
for that interval, then press **Pause** before stirring again. Repeat the
pause-mix-settle-record-pause sequence as the water cools.

**Step 9. Verify the saved calibration record.** Open the calibration CSV and
confirm that it contains timestamps and six populated temperature columns with
the expected labels. Compare several rows with the GUI and confirm that each
recorded interval has a corresponding thermocouple measurement.

**Step 10. Fit each channel to the reference.** Plot each rod-sensor reading,
\(T_i\), against the simultaneous TEC-thermistor reading,
\(T_{\mathrm{TEC}}\). Do the data fall on a straight line? If so, fit

\[
T_{\mathrm{TEC}}=a_i+b_iT_i.
\]

Apply this fitted relation as the correction:

\[
T_{i,\mathrm{corrected}}=a_i+b_iT_i.
\]

**Step 11. Check the corrected differences.** Plot

\[
\Delta T_i
=T_{i,\mathrm{corrected}}-T_{\mathrm{TEC}}
\]

against $T_{\mathrm{TEC}}$. Report the mean difference, scatter, and any
remaining trend with temperature. Choose and record an acceptance criterion
before evaluating the correction. A useful starting criterion is a corrected
mean difference smaller than $0.2^{\circ}\mathrm{C}$ for every channel, with
no residual trend larger than $0.2^{\circ}\mathrm{C}$ across the calibration
range. Revise this criterion if the measured noise and resolution justify a
different value.

**Step 12. Preserve the raw readings.** Store the correction coefficients
separately and apply them during analysis; never overwrite the original data.

The thermocouple measurement provides an independent check on the approximate
bath temperature and common-bath range. The channel corrections are still
obtained by treating the `TEC` thermistor as the common reference. The
corrected channels may therefore share a common absolute bias, but that bias
does not affect temperature differences or the measured spatial profile.

### If Needed, Analyze And Preserve The Correction

Only if the \(1^{\circ}\mathrm{C}\) agreement criterion fails, write a separate
Python analysis program for the optional correction. It must read the raw CSV
rather than modify the acquisition program. For each rod channel, fit

\[
T_{\mathrm{TEC}}=a_i+b_iT_i,
\]

make the comparison and residual plots required above, and save the fitted
coefficients and fit-quality measures in a separate calibration file. Keep the
raw CSV unchanged. Later analyses may read both files and calculate additional
columns named `rod1_corrected_C` through `rod5_corrected_C`. Record the
calibration-script filename and Git commit hash in the sensor map.

<details markdown="1">
<summary>Suggested Copilot prompt: relative-calibration analysis</summary>

```text
Write a separate Python calibration-analysis script for my six-thermistor CSV
file. Do not modify or overwrite the raw data. The raw columns are time_s,
tec_C, rod1_C, rod2_C, rod3_C, rod4_C, rod5_C, pwm, heat_cool, setpoint_C, and
safety.

Treat tec_C as the reference. For each rod channel i, perform a linear
least-squares fit tec_C = a_i + b_i * rod_i_C over a user-selected calibration
time or temperature range. Plot each rod temperature against tec_C with the
identity line and fitted line. Then plot the corrected residual
(a_i + b_i * rod_i_C) - tec_C against tec_C.

Print and save a table containing channel, a_i, b_i, number of fitted points,
calibration temperature range, residual mean, residual standard deviation,
and maximum absolute residual. Save this table to a separate CSV file. Also
write a separate corrected-data CSV that retains every original raw column and
adds rod1_corrected_C through rod5_corrected_C. Never replace a raw column.
Include clear axis labels with units and comment the file input, range
selection, fitting, residual calculation, and output sections for a Python
beginner.
```

</details>

</details>

## Phase 4: Configure And Acquire The Stationary Profile

For the initial Part III prediction, use

\[
h=10\ \mathrm{W\,m^{-2}K^{-1}}
\]

as a reasonable guess for natural convection from the rod in still room air.
This is a planning value, not a measurement. The stationary profile will be
used to test the model and determine the fitted decay coefficient \(m\).

1. Install rod thermistor 1 in the first rod hole and use that hole as the
   analysis base \(x=0\). It is neither the physical rod end nor the separate
   thermistor embedded in the TEC. Its measured signal \(T(0,t)\) is the
   boundary condition for the rod model.
2. For a steady placement pilot, begin with the TEC set to
   \(45^{\circ}\mathrm{C}\). A lower temperature generally reaches steady state
   faster but may produce temperature differences that are too small to resolve.
   A higher temperature improves the spatial signal but increases equilibration
   time and heat loss. If you change the pilot temperature, use the lowest
   setpoint that gives a clear profile and **never exceed
   \(55^{\circ}\mathrm{C}\)**.
3. Move the other four thermistors among the available fixed holes and measure
   the resulting steady temperatures. No advance calculation of the positions
   is required. Choose locations for which the steady excess temperature drops
   by at least a factor of \(e\) from rod thermistor 1 to the farthest retained
   sensor:

    \[
    0<\theta_5(x_5,\infty)
    \leq\frac{\theta_1(0,\infty)}{e}.
    \]

    Plot the pilot values as \(\ln\theta\) versus \(x\) while selecting the
    holes. The retained points should be spread across the semilog plot rather
    than clustered near one end. Do not retain a position whose excess
    temperature is indistinguishable from noise or room drift.

4. Once you have identified useful locations, leave the thermistors in those
   holes. Measure and record every selected position and its uncertainty.
5. Set the TEC to \(20^{\circ}\mathrm{C}\) and allow the entire rod to
   equilibrate. Record room temperature and all six thermistor channels. Verify
   that the rod channels agree within the common-bath acceptance criterion.
6. Before heating, review the prediction record and select a numerical
   steady-state criterion. A useful starting criterion is
   \( |dT_i/dt|<0.02^{\circ}\mathrm{C}/\mathrm{min} \) at every sensor for at
   least 10 minutes; justify any different criterion.
7. Apply a non-oscillatory TEC step from \(20^{\circ}\mathrm{C}\) to
   \(45^{\circ}\mathrm{C}\) using PI control. Record continuously until the
   selected steady-state criterion is satisfied. The purpose of retaining
   this complete time history is to document equilibration and select the
   stationary interval; a quantitative transient-model fit is not required.
8. Plot all temperatures against the same time axis. Use this plot to justify
   when the profile became stationary and explain qualitatively why farther
   sensors respond later and with smaller changes.
9. Save the commanded TEC temperature, measured TEC temperature, and measured
   rod temperature \(T(0,t)\). The rod thermistor at \(x=0\), rather than the
   TEC command or TEC thermistor, supplies the model boundary condition.

## C5 Checkoff

At S17, demonstrate:

- a documented common-bath check and any necessary corrections,
- documented sensor coordinates and wiring,
- synchronized multichannel logging,
- a live six-channel record showing the approach toward a stationary profile,
- files containing timestamps, units, channel labels, and experimental notes,
- individual understanding of the measurement chain and one dominant
  uncertainty.

## Phase 5: Analyze And Test The Stationary-Fin Models

At the constant \(45^{\circ}\mathrm{C}\) TEC setpoint, the final stationary
\(T(x)\) profile is the principal physics measurement in Module 7. Analyze the
record acquired in Phase 4 and compare it quantitatively with both the finite
insulated-tip solution and the semi-infinite exponential approximation.
**You must perform both fits.** Do not assume in advance that the rod is long
enough for the semi-infinite approximation; use the fitted curves, residuals,
and parameter uncertainties to decide whether ignoring the finite end is
adequate over the measured sensor positions.

1. Select the final interval of the Phase 4 record and confirm that it
   satisfies the stated steady-state criterion. No separate heating run is
   required.
2. Average each sensor over a justified final interval. Five minutes is a
   reasonable starting interval after the steady-state criterion has been met.
3. Plot \(\theta\) versus \(x\) with error bars.
4. Fit both the exact finite-length model and the semi-infinite exponential.
5. Plot both sets of residuals and report \(m\) in inverse meters with uncertainty.
6. Calculate the characteristic decay length \(1/m\) in meters.
7. Report how much the fitted \(m\) changes when the finite end is ignored and
   compare that shift with the fit uncertainty.
8. Discuss sensor-position error, room-temperature drift, imperfect contact,
   and the measured evidence for the tip boundary condition.
9. Compare the measured profile and residuals with the prediction record.
    State which assumptions are supported, which model is more adequate, and
    what discrepancy remains unexplained.

## Stationary-Fin Analysis Record

### Evidence To Save During S16-S17

Keep the sensor map, common-bath check record, any optional calibration
coefficients, geometry, raw baseline, complete synchronized temperature
history, commanded and measured TEC temperature, measured rod-base
temperature, steady profile, run
metadata, and exact acquisition code as each item is produced. Use
`docs/module_notes/module_07_rod_instrument.md`, `data/module_07/`, and
`docs/figures/module_07/`. Never overwrite raw rod data with corrected data.

### A4 Submission And Rubric

- **Type:** individual, 10 points
- **Due:** Wednesday, October 28, at **9:05 AM**
- **Moodle file:** `A4_Lastname.pdf`
- **Repository file:** `docs/assessments/a4_finite_length_biot.md`

The four required parts are listed in
[A4: Finite-Rod Model And Validity Checks](#a4-finite-rod-model-and-validity-checks).
Submit all four parts in the single PDF and repository file named above. Put
your name, assignment code, date, repository URL, and the exact Git commit hash
on the first page.

### C5: Rod Instrument And Data-Acquisition Chain

Demonstrate C5 during S17 on Wednesday, October 28. The `C5 Team Checkoff`
Moodle receipt is due by **11:55 AM** and must cite the pushed acquisition-code
and evidence commit.
Prepare the [C5 oral questions](../../assessment.md#c5-rod-instrument-and-data-acquisition-chain).

### Formative Stationary-Fin Analysis

There is no separate Moodle paper for this step. Keep the team note at
`docs/module_notes/module_07_stationary_fin.md` and authoritative analysis code
under `python/analysis/`. The result becomes evidence for C6 and the
final presentation.

Submit one reproducible analysis containing:

- the dimensional governing equation and assumptions,
- the sensor map, common-bath result, and any optional correction,
- a time-history plot documenting the approach to the selected stationary
  interval,
- steady $\theta(x)$ data, finite and semi-infinite fits, and both residual sets,
- fitted $m$ and $1/m$ with units and uncertainty,
- the sensor-by-sensor finite-length error and transverse Biot-number check,
- a short explanation of why this result alone cannot separate `k` from `h`.

### A4 Rubric

| Criterion | Points |
| --- | ---: |
| Part 1 correctly applies Fourier's law, units, and physical judgment to Problem 1.3 | 1 |
| Part 2 derives the stationary rod equation and finite insulated-tip solution from the stated laws and boundary conditions | 3 |
| Part 3 obtains the semi-infinite limit and correctly evaluates the tip approximation and sensor-by-sensor finite-length errors | 3 |
| Part 4 correctly calculates the transverse Biot number, gives a separate radius conclusion, and explains how airflow changes \(h\) and the decay length | 2 |
| The individual submission is complete, dimensionally checked, clearly organized, and cites the exact Git checkpoint | 1 |

The instructor will give feedback on the stationary-fin record during the rod
work. It is judged by whether the data, both fits, residuals, dimensional
parameters, uncertainty, and interpretation are ready to reuse in C6.

## Instructor Notes

<details class="note" markdown="1">
<summary>Instructor preparation for the hot-water common-bath check</summary>

- Provide a microwave and microwave-safe glass beakers or flasks for heating
  water. Thermistors, wires, and electrical hardware must never be placed in
  the microwave.
- Prepare eight functioning digital meters with thermocouple probes. Students
  will use resistance mode to measure the nominal \(100\ \mathrm{k}\Omega\)
  divider resistors and the thermocouple probes to measure the common-bath
  temperature.
- Provide 26 AWG paired insulated wire, short 22 AWG solid-wire breadboard
  pigtails, and suitable heat-shrink tubing for the individual joints.
- **Heat-shrink purchasing note:** Koowin \(3/32\)-inch-diameter tubing with a
  3:1 shrink ratio has been ordered. Test it on the actual 26 AWG paired wire
  and solder joints, and update the student specification only after confirming
  the fit.
- Fill the 4-liter water dispenser in the laboratory and bring it to the
  classroom, 401 Abelson, before class.
- Provide Styrofoam cups for the six-thermistor common bath.
- The drinking fountain outside the classroom can be used as the drain when
  the bath water is discarded.

</details>
