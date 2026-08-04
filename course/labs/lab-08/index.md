# Module 8: Rod Instrument, Step Response, And Stationary Fin

## Purpose

In Modules 1-7, one or two temperatures were enough to describe the TEC process.
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
| S16, Mon. Oct. 26 | Lecture: solve the finite-length one-dimensional rod; obtain the semi-infinite limit; introduce the transverse Biot number | Guided self-study begins |
| S17, Wed. Oct. 28 | Compare finite and semi-infinite predictions; calculate the rod Biot number; map and calibrate sensors | **A4: finite-length and small-Biot guided study** |
| S18, Mon. Nov. 2 | Acquire a synchronized step response; lecture on the axisymmetric radial model while the experiment runs | **C5: Rod instrument and data-acquisition chain** |
| S19, Wed. Nov. 4 | Reach steady state; fit finite-length and semi-infinite stationary profiles | Formative stationary-fin analysis |

## Outside-Class Workload Budget

| Session | Work | Planned time |
| --- | --- | ---: |
| S16 | Read this assignment, Lienhard Section 4.5, and the fin-derivation guide | 150 minutes |
| S16 | Begin A4: identify boundary conditions and organize the finite-length derivation | 75 minutes |
| S16 | **Total associated with S16** | **3 hours 45 minutes** |
| S17 | Complete and check the individual A4 calculations | 180 minutes |
| S17 | Prepare the sensor-map and calibration record | 45 minutes |
| S17 | **Total associated with S17** | **3 hours 45 minutes** |
| S18 | Prepare acquisition metadata and update the sensor map | 60 minutes |
| S18 | Organize the C5 evidence and Moodle receipt | 45 minutes |
| S18 | **Total associated with S18** | **1 hour 45 minutes** |
| S19 | Complete finite/semi-infinite fits, residuals, and uncertainty analysis | 135 minutes |
| S19 | Document, commit, and push the formative stationary analysis | 30 minutes |
| S19 | **Total associated with S19** | **2 hours 45 minutes** |

The reading allocation includes time to follow the derivation, not merely read
the prose. Save all rod measurements during class; the outside-class budget is
for theory, analysis, documentation, and submission.

## Learning Objectives

By the end of this module, you should be able to:

- define coordinates and metadata for a spatial temperature measurement,
- calibrate or cross-check several thermistors,
- acquire synchronized `T(x,t)` data with units and timestamps,
- derive the one-dimensional heat equation with side loss,
- solve the finite-length stationary problem and obtain its semi-infinite limit,
- calculate the error introduced by ignoring the far end,
- use the transverse Biot number to justify neglecting radial variation,
- distinguish a transient from a steady spatial profile,
- fit a stationary-fin model and interpret its decay coefficient,
- identify what the steady experiment can and cannot determine by itself.

## Reading And Preparation

1. Read Chapter 1 of [Lienhard and Lienhard, *A Heat Transfer Textbook*](../../references/lienhard-heat-transfer-textbook-v6.pdf).
2. Review [Theory Bridge: Fourier's Law, Heat Equation, And Biot Number](../theory-bridge-chapter-1/index.md).
3. For the S16 lecture and S17 guided study, read Lienhard Section 4.5,
   textbook pp. 163-173. Work through the derivation rather than reading only
   the final formulas.
4. Use [Fin Design: From A Finite Rod To An Infinite Rod](../fin-design-derivation/index.md)
   as the equation-by-equation guide to Lienhard Eqs. (4.27)-(4.51).
5. Complete the guided work in `A4`, including Lienhard Problems 4.12 and 4.20.

## Model

Let

\[
\theta(x,t)=T(x,t)-T_{\mathrm{room}}.
\]

For a uniform rod with cross-sectional area `A`, perimeter `P`, density `rho`,
specific heat `c`, thermal conductivity `k`, and side heat-transfer coefficient
`H`, conservation of energy gives

\[
\rho c A\frac{\partial\theta}{\partial t}
=kA\frac{\partial^2\theta}{\partial x^2}-HP\theta.
\]

Every term has units of power per unit length, watts per meter. Dividing by
`rho*c*A` gives

\[
\frac{\partial\theta}{\partial t}
=\kappa\frac{\partial^2\theta}{\partial x^2}-\nu\theta,
\qquad
\kappa=\frac{k}{\rho c},
\qquad
\nu=\frac{HP}{\rho c A}.
\]

Here `kappa` has units of square meters per second and `nu` has units of inverse
seconds.

At steady state,

\[
\frac{d^2\theta}{dx^2}-m^2\theta=0,
\qquad
m^2=\frac{HP}{kA}=\frac{\nu}{\kappa}.
\]

Far from the rod end, a useful first model is

\[
\theta(x)=\theta_0 e^{-mx}.
\]

The fitted `m` quantifies the competition between axial conduction and side
loss. It does **not** determine `k` and `H` separately. The periodic Angstrom
experiment in Module 9 supplies the second independent measurement.

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
\mathrm{Bi}_{\perp}=\frac{H(A/P)}{k}=\frac{HR}{2k}.
\]

The small-Biot condition \(\mathrm{Bi}_{\perp}\ll1\) means radial conduction
is fast enough that a cross section can be represented by one temperature.
Calculate \(\mathrm{Bi}_{\perp}\) using the rod radius and a justified range of
\(H\) and \(k\). This is a separate test from the finite-length test.

### A4 Guided Self-Study

Submit an individual solution that:

1. uses conservation of energy, Fourier's law, and Newton's law of cooling to
   derive the stationary fin equation with side heat loss,
2. follows the finite-fin solution in Lienhard Section 4.5 and identifies the
   two boundary conditions,
3. completes Problem 4.12 to obtain the semi-infinite limit,
4. uses Example 4.8 and Problem 4.20 to quantify the effect of a tip-boundary
   approximation,
5. calculates \(mL\) and \(\epsilon_T(x)\) for each course-rod sensor, using
   supplied parameters if measured values are not yet available,
6. calculates \(\mathrm{Bi}_{\perp}\), and
7. gives two separate conclusions: whether the rod may be treated as
   semi-infinite and whether it may be treated as one-dimensional.

### Radial-Model Lecture During S18

While the long step-response experiment is running, the lecture will retain
radial variation and introduce the axisymmetric heat equation. The goal is to
identify the new radial derivative and surface boundary condition, and to
distinguish surface, centerline, and cross-sectional mean temperature. The
guided numerical solution follows in Module 9 before the Angstrom analysis.

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

## Part 2: Baseline And Step Response

1. Record room temperature and all rod channels before changing the base.
2. Apply a safe temperature step at the base using PI control.
3. Record long enough to see the disturbance arrive at several positions.
4. Plot all temperatures against the same time axis.
5. Explain why farther sensors respond later and with smaller excursions.
6. Save the commanded base temperature and measured base temperature. The
   measured base is the actual boundary condition.

## C5 Checkoff

At S18, demonstrate:

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

### Evidence To Save During S17-S19

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
solutions, Problems 4.12 and 4.20, sensor-by-sensor error, transverse Biot
calculation, dimensional checks, and separate conclusions about length and
radius.

### C5: Rod Instrument And Data-Acquisition Chain

Demonstrate C5 during S18. The `C5 Team Checkoff` Moodle receipt is due by
**11:55 AM** and must cite the pushed acquisition-code and evidence commit.
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
- a short explanation of why this result alone cannot separate `k` from `H`.

### A4 Rubric

| Criterion | Points |
| --- | ---: |
| Stationary rod equation is derived from conservation, Fourier's law, and Newton's law | 2 |
| Finite insulated-tip solution follows from the stated boundary conditions | 2 |
| Semi-infinite limit and sensor-by-sensor finite-length errors are correct | 2 |
| Transverse Biot number and the separate radius conclusion are correct | 2 |
| Individual PDF and cited Git checkpoint are clear and on time | 2 |

The instructor will give feedback on the stationary-fin record during the rod
work. It is judged by whether the data, both fits, residuals, dimensional
parameters, uncertainty, and interpretation are ready to reuse in C6.
