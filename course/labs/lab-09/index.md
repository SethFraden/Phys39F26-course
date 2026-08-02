# Lab 9: The Angstrom Method

## Purpose

In this lab the TEC controller creates a sinusoidal temperature boundary at the
base of the aluminum rod. Thermal diffusion causes the oscillation amplitude to
decrease and its phase to lag with distance. Measuring both effects allows you
to separate thermal diffusion from heat loss to the air.

## Schedule And Due Work

| Meeting | In class | Due |
| --- | --- | --- |
| M20, Mon. Nov. 9 | Tune sinusoidal base-temperature tracking; collect a pilot run | Angstrom reading questions |
| M21, Wed. Nov. 11 | Fit pilot amplitudes and phases; choose production period | Angstrom derivation and experiment plan |
| M22, Mon. Nov. 16 | Acquire settled production data at one or more periods | Data-readiness check |
| M23, Wed. Nov. 18 | Fit spatial decay and phase slopes; infer `kappa` and `nu` | Modeling-app draft |

## Learning Objectives

By the end of this lab, you should be able to:

- impose and verify a sinusoidal temperature boundary with PI control,
- choose a useful forcing period using physical and practical constraints,
- fit a sinusoid to noisy temperature data,
- distinguish temporal frequency from spatial decay and phase coefficients,
- unwrap phase and maintain consistent sign conventions,
- determine thermal diffusivity and side-loss rate with uncertainty,
- test the model using residuals and frequency consistency.

## Periodic Solution

Use excess temperature `theta = T - T_room` and the rod equation

\[
\frac{\partial\theta}{\partial t}
=\kappa\frac{\partial^2\theta}{\partial x^2}-\nu\theta.
\]

Drive the measured base temperature approximately as

\[
\theta(0,t)=\theta_b\cos(\omega t),
\qquad
\omega=\frac{2\pi}{\tau},
\]

where `tau` is the period. After transients decay, the semi-infinite-rod
solution has the form

\[
\theta(x,t)=B_0e^{-qx}\cos(\omega t-q'x+\phi_0).
\]

The amplitude-decay coefficient `q` and phase coefficient `q_prime` both have
units of inverse meters:

\[
q=\sqrt{\frac{\nu+\sqrt{\nu^2+\omega^2}}{2\kappa}},
\qquad
q'=\sqrt{\frac{-\nu+\sqrt{\nu^2+\omega^2}}{2\kappa}}.
\]

The useful inverse relations are

\[
\kappa=\frac{\omega}{2qq'},
\qquad
\nu=\kappa(q^2-q'^2).
\]

## Part 1: Establish The Boundary Condition

1. Choose a safe mean base temperature and an amplitude of approximately
   5-10 degrees Celsius unless the instructor specifies otherwise.
2. Begin with a period in the range 100-300 seconds.
3. Tune PI settings so measured base temperature is close to sinusoidal without
   strong clipping, drift, or phase jumps.
4. Record setpoint, measured base temperature, PWM, and all rod temperatures.
5. Quantify boundary tracking with amplitude error, phase error, and residuals.
6. If tracking is imperfect, use the measured base temperature rather than the
   requested setpoint as the model boundary condition.

## Part 2: Pilot Analysis And Experiment Plan

For each sensor, fit

\[
T_i(t)=a_i+B_i\cos(\omega t+\phi_i).
\]

1. Remove the initial transient or justify the selected fitting interval.
2. Fit at least five complete settled periods.
3. Plot the data and fitted sinusoid for every sensor.
4. Plot amplitude `B_i` versus position on a logarithmic vertical scale.
5. Unwrap phase and plot phase versus position.
6. Select a production period for which several sensors have measurable
   amplitude and phase differences while the run still fits available time.

Your experiment plan must state the period, mean, amplitude, run duration,
sampling interval, safety limits, settling criterion, channels, files, and the
tests you will use to decide whether the run is usable.

## Part 3: Production Data

1. Record at least five complete settled periods.
2. Repeat the run at a second period if time and signal quality permit.
3. Keep the rod geometry and sensor map unchanged.
4. Record room temperature and check for drift.
5. Preserve raw data. Apply calibration and exclusions in analysis code, not by
   overwriting the original file.

## Part 4: Spatial Fits And Modeling-App Draft

Fit

\[
B(x)=B_0e^{-qx},
\qquad
\phi(x)=\phi_0-q'x.
\]

Your Python app, notebook, or script must visibly show:

- imported raw data and selected fitting interval,
- measured base tracking,
- sinusoid fit for every retained sensor,
- amplitude and unwrapped phase versus position,
- fitted `q` and `q_prime` with units and uncertainty,
- calculated `kappa` and `nu`,
- residuals and any excluded data with justification.

## Modeling-App Draft Submission

Submit runnable code, a short README with the exact command or procedure, the
data file or stable link, intermediate plots, preliminary `kappa` and `nu`, and
a note describing any AI assistance. Every team member must be able to explain
the input format and the sequence of fits.

