# Module 10: Aluminum Conductivity, Side Heat Loss, And Final Synthesis

## Purpose

The final task is not merely to make a good-looking rod-temperature plot. You
will use the Angstrom measurements to determine two physical properties:

- the thermal conductivity `k` of the aluminum rod, and
- the side heat-transfer coefficient `H` between the rod and its surroundings.

You will then test whether the heat equation with those parameters reproduces
the measured temperature field.

## Schedule And Due Work

| Session | In class | Due |
| --- | --- | --- |
| S24, Mon. Nov. 23 | Convert fitted coefficients into `k` and `H`; update the earlier finite-length and finite-radius checks using measured parameters | **A11: draft conductivity and heat-loss results** |
| S25, Mon. Nov. 30 | Freeze data, code, parameters, figures, and model-validity evidence; perform reproducibility check | **C6 and final analysis packet** |
| S26, Wed. Dec. 2 | Present and defend the complete instrument-to-model chain | Final presentation and individual oral defense |

## Learning Objectives

By the end of this module, you should be able to:

- carry units through the complete inference,
- convert diffusivity and loss rate into conductivity and heat-transfer
  coefficient,
- propagate measurement uncertainty and identify systematic error,
- compare steady and periodic estimates,
- simulate or reconstruct `T(x,t)` from a measured boundary condition,
- explain separately when finite length and finite radius may be ignored,
- judge model quality using residuals rather than appearance alone,
- make a repository reproduce the reported result,
- defend the physical reasoning without relying on AI-generated prose.

## From Angstrom Fits To Physical Properties

From Module 9,

\[
\kappa=\frac{\omega}{2qq'},
\qquad
\nu=\kappa(q^2-q'^2).
\]

Use aluminum density `rho` and specific heat `c`, with their sources and
uncertainties, to calculate

\[
k=\kappa\rho c.
\]

For rod cross-sectional area `A` and perimeter `P`, calculate

\[
H=\frac{\nu\rho c A}{P}.
\]

Report `k` in watts per meter-kelvin and `H` in watts per square
meter-kelvin. Check the dimensions explicitly before inserting numbers.

## Part 1: Parameter Table And Uncertainty

Create one table containing every input, fitted quantity, derived result, unit,
uncertainty, and source. It must include at least:

- forcing period and angular frequency,
- sensor positions,
- rod diameter, `A`, and `P`,
- `q` and `q_prime`,
- `kappa` and `nu`,
- `rho` and `c`,
- final `k` and `H`.

Use analytic propagation, bootstrap/resampling, Monte Carlo propagation, or an
approved equivalent. Include position uncertainty because phase and amplitude
slopes depend directly on sensor coordinates.

## Part 2: Physical And Model Checks

1. Compare `k` with an accepted range for the relevant aluminum alloy. Do not
   tune the model merely to force agreement.
2. Compare `H` with the expected scale for natural or forced convection in the
   actual apparatus.
3. Compare `m^2` from the stationary-fin fit with `nu/kappa` from the periodic
   fit.
4. If two forcing periods were measured, calculate parameters independently
   and test consistency.
5. Reconstruct or numerically simulate `T(x,t)` using the measured base
   temperature as the boundary condition.
6. Plot measured-versus-modeled traces and residuals for several positions.
7. Recalculate `mL`, finite-length error, and the transverse Biot number using
   the final fitted or inferred parameters rather than the preliminary values
   used in Modules 8 and 9.

## Part 3: Systematic Error

Discuss at least four of the following and state the expected direction of bias
when possible:

- sensor-position uncertainty,
- thermistor calibration and thermal contact,
- room-temperature drift,
- finite rod length and end boundary condition,
- nonuniform side convection,
- radiation loss,
- non-sinusoidal or poorly tracked base temperature,
- too few settled periods,
- phase unwrapping,
- temperature dependence or alloy dependence of material properties.

## C6 Checkoff And Final Analysis Packet

The final repository must contain:

- raw data and an immutable description of the run,
- sensor map and calibration information,
- runnable analysis/model code,
- a README with exact reproduction steps,
- amplitude, phase, residual, and measured-versus-modeled plots,
- `q`, `q_prime`, `kappa`, `nu`, aluminum `k`, and side-loss `H`, all with units
  and uncertainty,
- accepted-value and model-limitation discussion,
- the finite-length error calculation and final transverse-Biot-number check,
- the guided numerical comparison of one-dimensional and finite-radius models
  completed before the Angstrom production analysis,
- a record of meaningful AI assistance.

For the C6 demonstration, a fresh run from the documented repository must
reproduce the principal numbers and figures. Each student will answer short
individual questions about the Angstrom inference and about when length or
radius may be neglected.

## Final Presentation

The presentation should tell one connected story:

1. How the Arduino, thermistors, TEC, H-bridge, Python GUI, and PI controller
   create a measurable boundary-value experiment.
2. How conservation of energy and Fourier's law produce the rod model.
3. How the data produce `q` and `q_prime`.
4. How those slopes produce `k` and `H`.
5. Whether the results are credible, what limits them, and what you would do
   next.

Every team member must speak and must be prepared to answer an individual
question about hardware, software, control, or thermal physics.
