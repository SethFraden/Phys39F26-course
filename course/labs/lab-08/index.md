# Module 7, Part III: Rod Instrument, Step Response, And Stationary Fin

This is the experimental part of Module 7. It builds on [Part I: Thermal
Transport Foundations](../theory-bridge-chapter-1/index.md) and [Part II: Finite
And Infinite Rod Theory](../fin-design-derivation/index.md).

## Purpose

In Modules 1-6, one or two temperatures were enough to describe the TEC process.
The aluminum rod cannot be treated as one thermal lump. Its temperature depends
on position and time:

\[
T=T(x,t).
\]

In this module you will build and validate the multichannel rod instrument,
measure a step response, and measure the steady temperature profile. The steady
profile gives the first quantitative evidence of heat loss from the rod's side.

## Schedule And Due Work

| Session | In class | Due |
| --- | --- | --- |
| S16, Mon. Oct. 26 | Review the finite-rod theory prepared at home; compare finite and semi-infinite predictions; calculate the transverse Biot number; map and calibrate sensors; begin baseline and step-response measurements | Module 7 home preparation |
| S17, Wed. Oct. 28 | Complete the synchronized step response and stationary profile; fit finite-length and semi-infinite stationary profiles | **A4: finite-length and small-Biot guided study**; **C5: Rod instrument and data-acquisition chain** |

## Outside-Class Workload Budget

| Session | Work | Planned time |
| --- | --- | ---: |
| S16 | Read this assignment, Lienhard Section 4.5, and the fin-derivation guide | 150 minutes |
| S16 | Begin A4: identify boundary conditions and organize the finite-length derivation | 75 minutes |
| S16 | **Total associated with S16** | **3 hours 45 minutes** |
| S17 | Complete and check the individual A4 calculations | 180 minutes |
| S17 | Prepare the sensor-map and calibration record | 45 minutes |
| S17 | **Total associated with S17** | **3 hours 45 minutes** |

The reading allocation includes time to follow the derivation, not merely read
the prose. Save all rod measurements during class; the outside-class budget is
for theory, analysis, documentation, and submission.

## Learning Objectives

The objectives below are listed in priority order. By the end of Module 7,
Part III, you should be able to:

1. Build and document a spatial temperature measurement by defining sensor
   coordinates, cross-checking the thermistors, and acquiring synchronized
   $T(x,t)$ data with units, timestamps, and experimental metadata.
2. Use the finite-length solution and transverse Biot number to make separate,
   quantitative decisions about whether the far end and radial temperature
   variation may be neglected.
3. Distinguish a transient from a steady spatial profile and explain why a
   temperature disturbance arrives later and is smaller farther from the
   heated base.
4. Fit finite-length and semi-infinite stationary-fin models, examine their
   residuals, and interpret the fitted decay coefficient and decay length.
5. Explain what the steady experiment can determine and why it cannot determine
   the thermal conductivity and side heat-transfer coefficient separately.

## Part III Vocabulary And Notation

Review the [foundational vocabulary in Part
I](../theory-bridge-chapter-1/index.md#module-7-vocabulary-and-notation) and the
[fin-model vocabulary in Part
II](../fin-design-derivation/index.md#part-ii-vocabulary-and-notation). The
terms below connect that theory to the experiment and its analysis.

| Term | Meaning |
| --- | --- |
| Temperature field, \(T(x,t)\) | Temperature as a function of both position along the rod and time. |
| Excess temperature, \(\theta(x,t)=T(x,t)-T_{\mathrm{room}}\) | Rod temperature measured relative to room temperature. |
| Thermal diffusivity, \(\kappa=k/(\rho c)\) | The coefficient controlling axial spreading in the Part III model. It is the same physical property denoted \(\alpha\) in Part I. |
| Side-loss rate, \(\nu=hP/(\rho cA)\) | The fractional rate, in s\(^{-1}\), at which side convection removes excess thermal energy in the one-dimensional model. |
| Decay coefficient, \(m=\sqrt{hP/(kA)}=\sqrt{\nu/\kappa}\) | The spatial decay rate of the stationary profile; \(1/m\) is the decay length. |
| Sensor map | A record of each channel name, thermistor position, coordinate origin and direction, and position uncertainty. |
| Calibration or cross-check | A comparison under a common temperature condition used to identify sensor offsets or other channel differences. |
| Baseline | Measurements made before the imposed temperature change, used to establish room temperature and initial sensor readings. |
| Step response | The measured evolution of \(T(x,t)\) after the base-temperature command changes. |
| Boundary condition | The measured or prescribed behavior at a boundary. The measured base temperature, rather than only its commanded value, is the experimental thermal boundary condition. |
| Stationary profile | The position-dependent temperature after changes with time have become negligible according to a stated criterion. |
| Model fit | Estimation of model parameters by comparing a predicted curve with measured data. |
| Residual | Measured value minus model prediction at the same position or time. Residual structure can reveal model inadequacy. |
| Uncertainty | A quantitative estimate of the plausible range of a measured or fitted result. |
| Metadata | Information needed to interpret and reproduce a run, including units, timestamps, channel labels, geometry, settings, and experimental notes. |

## Reading And Preparation

1. Read Chapter 1 of [Lienhard and Lienhard, *A Heat Transfer Textbook*](../../references/lienhard-heat-transfer-textbook-v6.pdf).
2. Review [Module 7, Part I: Thermal Transport Foundations](../theory-bridge-chapter-1/index.md).
3. For the S16 lecture and S17 guided study, read Lienhard Section 4.5,
   textbook pp. 163-173. Work through the derivation rather than reading only
   the final formulas.
4. Use [Fin Design: From A Finite Rod To An Infinite Rod](../fin-design-derivation/index.md)
   as the equation-by-equation guide to Lienhard Eqs. (4.27)-(4.51).
5. Complete the guided work in `A4`, including Lienhard Problems 1.3, 4.12,
   and 4.20. Problem 1.3 is assigned in
   [Module 7, Part I](../theory-bridge-chapter-1/index.md#a4-part-i-lienhard-problem-13).

## Model

Let

\[
\theta(x,t)=T(x,t)-T_{\mathrm{room}}.
\]

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
=\kappa\frac{\partial^2\theta}{\partial x^2}-\nu\theta,
\qquad
\kappa=\frac{k}{\rho c},
\qquad
\nu=\frac{hP}{\rho c A}.
\]

Here $\kappa$ has units of square meters per second and $\nu$ has units of
inverse seconds.

At steady state,

\[
\frac{d^2\theta}{dx^2}-m^2\theta=0,
\qquad
m^2=\frac{hP}{kA}=\frac{\nu}{\kappa}.
\]

Far from the rod end, a useful first model is

\[
\theta(x)=\theta_0 e^{-mx}.
\]

The fitted $m$ quantifies the competition between axial conduction and side
loss. It does **not** determine $k$ and $h$ separately. The periodic Angstrom
experiment in Module 8, Part I, supplies the second independent measurement.

## Part 0: Which Geometry May We Ignore?

### Length: Solve It First

For a rod of finite length \(L\), prescribed base temperature, and insulated
tip, the exact normalized stationary solution is

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
The product \(mL\) is useful, but the answer also depends on which sensor and
which observable you use.

### Radius: Check The Transverse Biot Number

For a circular rod,

\[
\mathrm{Bi}_{\perp}=\frac{h(A/P)}{k}=\frac{hR}{2k}.
\]

The small-Biot condition \(\mathrm{Bi}_{\perp}\ll1\) means radial conduction
is fast enough that a cross section can be represented by one temperature.
Calculate \(\mathrm{Bi}_{\perp}\) using the rod radius and a justified range of
\(h\) and \(k\). This is a separate test from the finite-length test.

### A4 Guided Self-Study

Submit an individual solution that:

1. completes Lienhard Problem 1.3 as assigned in
   [Part I](../theory-bridge-chapter-1/index.md#a4-part-i-lienhard-problem-13),
2. uses conservation of energy, Fourier's law, and Newton's law of cooling to
   derive the stationary fin equation with side heat loss,
3. follows the finite-fin solution in Lienhard Section 4.5 and identifies the
   two boundary conditions,
4. completes Problem 4.12 to obtain the semi-infinite limit,
5. uses Example 4.8 and Problem 4.20 to quantify the effect of a tip-boundary
   approximation,
6. calculates \(mL\) and \(\epsilon_T(x)\) for each course-rod sensor, using
   supplied parameters if measured values are not yet available,
7. calculates \(\mathrm{Bi}_{\perp}\), and
8. gives two separate conclusions: whether the rod may be treated as
   semi-infinite and whether it may be treated as one-dimensional.

### Radial Model Preview

The next module retains radial variation and introduces the axisymmetric heat
equation. Its goal is to identify the new radial derivative and surface
boundary condition, and to distinguish surface, centerline, and
cross-sectional mean temperature. The guided numerical solution begins in
Module 8, Part I, before the Angstrom analysis.

## Part 1: Sensor Map And Calibration

1. Measure the rod diameter and record `A` and `P` in SI units.
2. Assign each thermistor a permanent channel name.
3. Measure each sensor position from the defined origin and estimate its
   position uncertainty.
4. Hold all sensors at nearly the same temperature and record at least 60
   seconds of data.
5. Plot channel differences. Decide whether offsets require correction.
6. Save a diagram or photograph showing the coordinate direction and channel
   positions.

### Relative Thermistor Cross-Calibration

The rod experiment measures temperature differences and spatial temperature
gradients. It does not require an absolute temperature calibration. It does
require all thermistor channels to give the same reading when they experience
the same temperature; otherwise, channel-to-channel offsets could be mistaken
for a temperature gradient along the rod.

Use the TEC thermistor as the reference channel and cross-calibrate the rod
thermistors as follows:

**Step 1. Arrange the sensors.** Label all the thermistors. Label your existing TEC thermistor "TEC". Label the others 1 - 5. It is important that the labels do not fall off for the rest of the semester. Place all six thermistor sensing ends close
together in a Styrofoam cup of warm water. You are interested in the approximate temperature range $60^{\circ} \mathrm{C} > T > 20^{\circ}\mathrm{C}$. Immerse only waterproof sensing ends
and keep electrical joints dry. Do not allow the sensors to touch the cup walls
or bottom.

**Step 2. Use the experimental measurement chain.** Make sure the corresonding Arduino circuit and thermistor are always used together. Use the same voltage
dividers, Arduino inputs, acquisition code, and sample rate that will be used
for the rod experiment.

**Step 3. Keep the bath uniform.** Stir the water gently and continuously so
that all sensors experience the same temperature.

**Step 4. Record the common cooling history.** Record every channel
simultaneously while the water cools slowly through the temperature range
expected in the rod experiment.

**Step 5. Fit each channel to the reference.** Plot each rod-sensor reading,
$T_i$, against the simultaneous TEC-thermistor reading, $T_{\mathrm{TEC}}$,
and fit

\[
T_{\mathrm{TEC}}=a_i+b_iT_i.
\]

**Step 6. Check the corrected differences.** Plot

\[
\Delta T_i
=T_{i,\mathrm{corrected}}-T_{\mathrm{TEC}}
\]

against $T_{\mathrm{TEC}}$. Report the mean difference, scatter, and any
remaining trend with temperature.

**Step 7. Preserve the raw readings.** Store the correction coefficients
separately and apply them during analysis; never overwrite the original data.

No independent reference thermometer is required for this relative
cross-calibration. The corrected channels may share a common absolute bias,
but that bias does not affect temperature differences or the measured spatial
profile.

## Part 2: Baseline And Step Response

1. Record room temperature and all rod channels before changing the base.
2. Apply a safe temperature step at the base using PI control.
3. Record long enough to see the disturbance arrive at several positions.
4. Plot all temperatures against the same time axis.
5. Explain why farther sensors respond later and with smaller excursions.
6. Save the commanded base temperature and measured base temperature. The
   measured base is the actual boundary condition.

## C5 Checkoff

At S17, demonstrate:

- calibrated or cross-checked rod thermistors,
- documented sensor coordinates and wiring,
- synchronized multichannel logging,
- baseline and initial step-response data,
- files containing timestamps, units, channel labels, and experimental notes,
- individual understanding of the measurement chain and one dominant
  uncertainty.

## Part 3: Stationary-Fin Profile

1. Hold the base at a constant safe temperature until the profile changes more
   slowly than your stated steady-state criterion.
2. Average each sensor over a justified final time interval.
3. Plot `theta` versus `x` with error bars.
4. Fit both the exact finite-length model and the semi-infinite exponential.
5. Plot both sets of residuals and report `m` in inverse meters with uncertainty.
6. Calculate the characteristic decay length `1/m` in meters.
7. Report how much the fitted `m` changes when the finite end is ignored and
   compare that shift with the fit uncertainty.
8. Discuss sensor-position error, room-temperature drift, imperfect contact,
   and the measured evidence for the tip boundary condition.

## Stationary-Fin Analysis Record

### Evidence To Save During S16-S17

Keep the sensor map, calibration record, geometry, raw baseline, synchronized
step response, commanded and measured base temperature, steady profile, run
metadata, and exact acquisition code as each item is produced. Use
`docs/module_notes/module_08_rod_instrument.md`, `data/module_08/`, and
`docs/figures/module_08/`. Never overwrite raw rod data with corrected data.

### A4: Finite-Length And Small-Biot Guided Study

- **Type:** individual, 10 points
- **Due:** Wednesday, October 28, at **9:05 AM**
- **Moodle file:** `A4_Lastname.pdf`
- **Repository file:** `docs/assessments/a4_finite_length_biot.md`

The required content is listed in [A4 Guided Self-Study](#a4-guided-self-study).
Submit the governing-equation derivation, finite and semi-infinite analytical
solutions, Problems 1.3, 4.12, and 4.20, sensor-by-sensor error, transverse
Biot calculation, dimensional checks, and separate conclusions about length
and radius.

### C5: Rod Instrument And Data-Acquisition Chain

Demonstrate C5 during S17 on Wednesday, October 28. The `C5 Team Checkoff`
Moodle receipt is due by **11:55 AM** and must cite the pushed acquisition-code
and evidence commit.
Prepare the [C5 oral questions](../../assessment.md#c5-rod-instrument-and-data-acquisition-chain).

### Formative Stationary-Fin Analysis

There is no separate Moodle paper for this step. Keep the team note at
`docs/module_notes/module_08_stationary_fin.md` and authoritative analysis code
under `python/analysis/`. The result becomes evidence for C6 and the
final presentation.

Submit one reproducible analysis containing:

- the dimensional governing equation and assumptions,
- the sensor map and calibration result,
- baseline and step-response plots,
- steady `theta(x)` data, finite and semi-infinite fits, and both residual sets,
- fitted `m` and `1/m` with units and uncertainty,
- the sensor-by-sensor finite-length error and transverse Biot-number check,
- a short explanation of why this result alone cannot separate `k` from `h`.

### A4 Rubric

| Criterion | Points |
| --- | ---: |
| Problem 1.3 correctly applies Fourier's law, units, and physical judgment | 1 |
| Stationary rod equation is derived from conservation, Fourier's law, and Newton's law | 1 |
| Finite insulated-tip solution follows from the stated boundary conditions | 2 |
| Semi-infinite limit and sensor-by-sensor finite-length errors are correct | 2 |
| Transverse Biot number and the separate radius conclusion are correct | 2 |
| Individual PDF and cited Git checkpoint are clear and on time | 2 |

The instructor will give feedback on the stationary-fin record during the rod
work. It is judged by whether the data, both fits, residuals, dimensional
parameters, uncertainty, and interpretation are ready to reuse in C6.
