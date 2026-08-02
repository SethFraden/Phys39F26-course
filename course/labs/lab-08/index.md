# Lab 8: Rod Instrument, Step Response, And Stationary Fin

## Purpose

In Labs 1-7, one or two temperatures were enough to describe the TEC process.
The aluminum rod cannot be treated as one thermal lump. Its temperature depends
on position and time:

\[
T=T(x,t).
\]

In this lab you will build and validate the multichannel rod instrument,
measure a step response, and measure the steady temperature profile. The steady
profile gives the first quantitative evidence of heat loss from the rod's side.

## Schedule And Due Work

| Meeting | In class | Due |
| --- | --- | --- |
| M17, Wed. Oct. 28 | Map and calibrate sensors; acquire baseline data | Heat-equation and dimensional-analysis derivation |
| M18, Mon. Nov. 2 | Acquire synchronized step response | **C5: Rod instrument and data-acquisition chain** |
| M19, Wed. Nov. 4 | Reach steady state; fit the stationary-fin profile | Stationary-fin analysis |

## Learning Objectives

By the end of this lab, you should be able to:

- define coordinates and metadata for a spatial temperature measurement,
- calibrate or cross-check several thermistors,
- acquire synchronized `T(x,t)` data with units and timestamps,
- derive the one-dimensional heat equation with side loss,
- distinguish a transient from a steady spatial profile,
- fit a stationary-fin model and interpret its decay coefficient,
- identify what the steady experiment can and cannot determine by itself.

## Reading And Preparation

1. Read Chapter 1 of [Lienhard and Lienhard, *A Heat Transfer Textbook*](../../references/lienhard-heat-transfer-textbook-v6.pdf).
2. Review [Theory Bridge: Fourier's Law, Heat Equation, And Biot Number](../theory-bridge-chapter-1/index.md).
3. Before M17, submit a dimensional derivation beginning with conservation of
   energy for a rod slice of length `dx`.

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
experiment in Lab 9 supplies the second independent measurement.

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

At M18, demonstrate:

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
4. Fit the exponential model or a finite-rod model if the end condition matters.
5. Plot residuals and report `m` in inverse meters with uncertainty.
6. Calculate the characteristic decay length `1/m` in meters.
7. Discuss the effects of sensor-position error, room-temperature drift,
   imperfect contact, and the finite rod end.

## Stationary-Fin Submission

Submit one reproducible analysis containing:

- the dimensional governing equation and assumptions,
- the sensor map and calibration result,
- baseline and step-response plots,
- steady `theta(x)` data, model fit, and residuals,
- fitted `m` and `1/m` with units and uncertainty,
- a short explanation of why this result alone cannot separate `k` from `H`.

