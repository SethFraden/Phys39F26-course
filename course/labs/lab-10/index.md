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
| S24, Mon. Nov. 23 | Convert fitted coefficients into `k` and `H`; update the earlier finite-length and finite-radius checks using measured parameters | Formative draft-results check |
| S25, Mon. Nov. 30 | Freeze data, code, parameters, figures, and model-validity evidence; perform reproducibility check | **C6 final analysis package** |
| S26, Wed. Dec. 2 | Present and defend the complete instrument-to-model chain | Final presentation and individual oral defense |

## Outside-Class Workload Budget

| Session | Work | Planned time |
| --- | --- | ---: |
| S24 | Read this assignment and organize the final parameter table | 45 minutes |
| S24 | Propagate uncertainty, compare accepted values, and prepare the draft-results check | 150 minutes |
| S24 | Document, commit, and push the draft | 30 minutes |
| S24 | **Total associated with S24** | **3 hours 45 minutes** |
| S25 | Freeze the analysis, run the reproducibility test, and prepare C6 | 240 minutes |
| S25 | **Total associated with S25** | **4 hours** |
| S26 | Prepare slides, rehearse, and practice the announced oral questions | 240 minutes |
| S26 | **Total associated with S26** | **4 hours** |

These final sessions use the full allowance. Reuse the figures, equations, and
documentation already produced during Modules 8-9; do not create a second parallel
analysis solely for presentation polish.

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

One team member submits `F1_Lastname_Lastname_slides.pdf` to Moodle before the
S26 presentation and cites the final repository commit. Every student prepares
the announced [C6/F1 oral questions](../../assessment.md#c6-oral-questions).

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
