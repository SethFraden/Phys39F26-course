# Module 8, Part II: Conductivity, Heat Loss, And Final Synthesis

This is the second and final part of Module 8. It converts the measurements
from [Part I: The Angstrom Method](../lab-09/index.md) into physical properties
and a final test of the model.

## Purpose

Module 8 has three priorities, in this order:

1. **Measure six temperatures as functions of time.** The primary experimental
   result is the synchronized record from the TEC thermistor and rod
   thermistors `T1`-`T5`, together with the validated sensor map, any optional
   correction coefficients, positions, units, timestamps, and run metadata.
2. **Understand the Angstrom method.** Use amplitude decay and phase lag to
   connect the measured temperature histories to thermal transport.
3. **Compare experiment and theory.** Reconstruct or simulate the temperature
   field, inspect residuals and consistency, and decide where the model
   succeeds or fails.

Part II concentrates on the third priority, but the comparison is credible
only because Part I produced the six-channel measurement and established the
Angstrom analysis.

The final task is not merely to make a good-looking rod-temperature plot. You
will use the Angstrom measurements to determine two physical properties:

- the thermal conductivity `k` of the aluminum rod, and
- the convective heat-transfer coefficient `h` between the rod and room air.

You will then test whether the heat equation with those parameters reproduces
the measured temperature field.

## Schedule And Due Work

| Session | In class | Due |
| --- | --- | --- |
| S23, Wed. Nov. 18 | Convert fitted coefficients into `k` and `h`; update the finite-length and transverse-Biot checks using measured parameters | Parameter and model-validity check |
| S24, Mon. Nov. 23 | Propagate uncertainty, compare stationary and periodic estimates, and assemble the final analysis | Formative draft-results check |
| S25, Mon. Nov. 30 | Freeze data, code, parameters, figures, and model-validity evidence; perform reproducibility check | **C6 final analysis package** |
| S26, Wed. Dec. 2 | Present and defend the complete instrument-to-model chain | Final presentation and individual oral defense |

## Outside-Class Workload Budget

| Session | Work | Planned time |
| --- | --- | ---: |
| S23 | Read this assignment and organize the final parameter table | 45 minutes |
| S23 | Calculate `k` and `h` and update the model-validity checks | 150 minutes |
| S23 | Document, commit, and push the parameter checkpoint | 30 minutes |
| S23 | **Total associated with S23** | **3 hours 45 minutes** |
| S24 | Propagate uncertainty, compare accepted values, and prepare the draft-results check | 150 minutes |
| S24 | Document, commit, and push the draft | 30 minutes |
| S24 | **Total associated with S24** | **3 hours** |
| S25 | Freeze the analysis, run the reproducibility test, and prepare C6 | 240 minutes |
| S25 | **Total associated with S25** | **4 hours** |
| S26 | Prepare slides, rehearse, and practice the announced oral questions | 240 minutes |
| S26 | **Total associated with S26** | **4 hours** |

These final sessions use the full allowance. Reuse the figures, equations, and
documentation already produced during Modules 7 and 8; do not create a second parallel
analysis solely for presentation polish.

## Learning Objectives

The first three objectives preserve the Module 8 priority order. By the end of
this module, you should be able to:

1. Preserve and interpret the synchronized six-temperature record, including
   the validated sensor map, common-bath result, any optional correction
   coefficients, sensor positions, forcing history, units, timestamps, and
   uncertainty.
2. Explain how the Angstrom method converts measured amplitude decay and phase
   lag into thermal diffusivity and side-loss rate.
3. Compare measured and modeled \(T(x,t)\) using reconstruction, residuals,
   frequency consistency, and separate finite-length and transverse-Biot
   checks.

To complete that comparison, you should also be able to:

- carry units through the complete inference,
- convert diffusivity and loss rate into conductivity and heat-transfer
  coefficient,
- propagate measurement uncertainty and identify systematic error,
- compare steady and periodic estimates,
- simulate or reconstruct `T(x,t)` from a measured boundary condition,
- explain separately how finite length and transverse temperature gradients
  affect the one-dimensional model,
- judge model quality using residuals rather than appearance alone,
- make a repository reproduce the reported result,
- defend the physical reasoning without relying on AI-generated prose.

## From Angstrom Fits To Physical Properties

Bring forward from Module 8, Part I the immutable raw files, validated sensor
map, common-bath result, any optional correction coefficients, sensor-position
uncertainties, exact forcing frequency, selected settled intervals, fitted
\(q\) and \(q'\) with uncertainty, residuals, and the code checkpoint that
produced them. A minimum experiment provides one usable frequency; an extended
experiment adds independently analyzed frequencies.

Part I produced preliminary values of \(\kappa\) and \(\nu\) so that you could
judge whether the experiment worked. Part II turns those estimates into final,
uncertainty-qualified values of \(k\) and \(h\), reconstructs the measured
temperature field, and determines whether the model is credible.

From Part I,

\[
\kappa=\frac{\omega}{2qq'},
\qquad
\nu=\kappa(q^2-q'^2).
\]

Use 6061-T6 aluminum density `rho` and specific heat `c`, with their sources and
uncertainties, to calculate

\[
k=\kappa\rho c.
\]

Because \(\kappa=\omega/(2qq')\), this determination of \(k\) uses the measured
amplitude-decay slope, phase slope, and forcing frequency; it does not require
an independent measurement of \(h\) or of the heat lost from the rod. This is
experimentally valuable because convection is sensitive to airflow,
orientation, surface condition, and temperature. The Angstrom measurement
separates axial diffusion from convective side loss using the same temperature
records.

For rod cross-sectional area `A` and perimeter `P`, calculate

\[
h=\frac{\nu\rho c A}{P}.
\]

Here \(h\) is the convective heat-transfer coefficient used in Newton's law of
cooling.

Report `k` in watts per meter-kelvin and `h` in watts per square
meter-kelvin. Check the dimensions explicitly before inserting numbers.

## Stage 1: Parameter Table And Uncertainty

Create one table containing every input, fitted quantity, derived result, unit,
uncertainty, and source. It must include at least:

- forcing period and angular frequency,
- sensor positions,
- rod diameter, `A`, and `P`,
- `q` and `q_prime`,
- `kappa` and `nu`,
- `rho` and `c`,
- final `k` and `h`.

Use analytic propagation, bootstrap/resampling, Monte Carlo propagation, or an
approved equivalent. Include position uncertainty because phase and amplitude
slopes depend directly on sensor coordinates.

## Stage 2: Physical And Model Checks

1. Compare `k` with an accepted range for 6061-T6 aluminum. Do not
   tune the model merely to force agreement.
2. Compare `h` with the expected scale for natural or forced convection in the
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
   used in Modules 7 and 8.
8. Use the two-stage per-sensor and spatial fits as the primary analysis. As an
   optional model-validity test, compare them with a global fit of the retained
   \(T_i(t)\) data using shared spatial parameters.

## Stage 3: Systematic Error

Discuss at least four of the following and state the expected direction of bias
when possible:

- sensor-position uncertainty,
- optional thermistor corrections and thermal contact,
- room-temperature drift,
- finite rod length and end boundary condition,
- nonuniform side convection,
- non-sinusoidal or poorly tracked base temperature,
- too few settled periods,
- phase unwrapping,
- temperature dependence or alloy dependence of material properties.

## C6 Checkoff And Final Analysis Packet

The assessments build on one another rather than asking for parallel analyses:

- **A5** is each student's derivation and acquisition plan.
- The **formative modeling app** is the team's working implementation and
  preliminary analysis of measured data.
- **C6** is the team's final reproducible inference, including uncertainty,
  physical checks, and a defensible judgment of model quality.

### Final Thermal-Transport Analysis Packet

This team analysis is graded within C6 and F1 rather than as a sixth written
assignment. Keep the report at
`docs/assessments/final_thermal_transport_analysis.md` and cite it in the C6
Moodle receipt.

Before leaving S24, preserve a formative draft containing the exact `q`, `q_prime`, geometry, material
properties, uncertainty method, accepted-value source, finite-length check,
transverse-Biot check, and code version used for the draft result.

The C6 rubric evaluates whether the stationary and periodic analyses are
reproducible; the dimensional quantities, units, uncertainties, and sources
are correct; and residuals, accepted-value comparisons, and model-validity
checks support the conclusions.

### C6 Submission

Demonstrate C6 during S25. The `C6 Team Checkoff` Moodle receipt is due by
**11:55 AM** and must cite the frozen, pushed analysis commit. Use the
[C6 rubric and oral-question bank](../../assessment.md#c6-final-thermal-transport-package).

The final repository must contain:

- raw data and an immutable description of the run,
- validated sensor map, common-bath result, and any optional correction
  coefficients,
- runnable analysis/model code,
- a README with exact reproduction steps,
- amplitude, phase, residual, and measured-versus-modeled plots,
- `q`, `q_prime`, `kappa`, `nu`, aluminum `k`, and side-loss `h`, all with units
  and uncertainty,
- accepted-value and model-limitation discussion,
- the finite-length error calculation and final transverse-Biot-number check,
- a record of meaningful AI assistance.

For the C6 demonstration, a fresh run from the documented repository must
reproduce the principal numbers and figures. Each student will answer short
individual questions about the Angstrom inference, finite-length effects, and
the transverse-Biot criterion.

## Final Presentation

One team member submits `F1_Lastname_Lastname_slides.pdf` to Moodle before the
S26 presentation and cites the final repository commit. Every student prepares
the announced [C6/F1 oral questions](../../assessment.md#c6-oral-questions).

The presentation should tell one connected story:

1. How the Arduino, thermistors, TEC, H-bridge, Python GUI, and PI controller
   create a measurable boundary-value experiment.
2. How conservation of energy and Fourier's law produce the rod model.
3. How the data produce `q` and `q_prime`.
4. How those slopes produce `k` and `h`.
5. Whether the results are credible, what limits them, and what you would do
   next.

Every team member must speak and must be prepared to answer an individual
question about hardware, software, control, or thermal physics.
