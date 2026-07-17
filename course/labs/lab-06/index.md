# Lab 6 Assignment: Modeling P And PI Temperature Control

## Purpose

Lab 6 slows down the theory. Lab 5 showed that proportional feedback reduces
steady-state error but can become unstable. Lab 6 builds simple models that
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
2. Review your Lab 4 and Lab 5 data.
3. Optional after class: Bechhoefer pp. 795-797 on feedback and stability.

Do not try to learn all of transient heat transfer at once. For this lab, you
need the idea that a physical object has heat capacity, exchanges heat with its
environment, and responds over a time scale.

## Vocabulary

- **Thermal capacitance**, `C`: how much heat is needed to change temperature.
- **Thermal resistance**, `R`: how strongly the object is thermally connected
  to its surroundings.
- **Time constant**, `tau = R*C`: the approximate response time of a first-order
  thermal system.
- **Open-loop slope**, `S`: steady-state temperature change per PWM command.
- **P control**: command proportional to current error.
- **I control**: command proportional to accumulated error.
- **Windup**: integral term grows while the actuator is saturated.

## Before Class

Bring:

- your Lab 4 steady-state `T` versus PWM data,
- your Lab 5 droop versus `Kp` data,
- one Lab 5 strip chart trace at a stable gain,
- one Lab 5 strip chart trace near oscillation,
- your current Python plotting/modeling environment.

## Pre-Class Questions

1. What physical part of the apparatus stores heat?
2. What physical paths let heat leave the measured block?
3. What evidence from your data suggests a thermal time constant?
4. Why does the algebraic droop model not predict oscillation?

## What You Will Do

- Derive the algebraic P-control droop model.
- Fit or estimate an open-loop thermal slope from Lab 4.
- Fit or estimate a time constant from a temperature step.
- Simulate a first-order TEC/block model.
- Add P-only feedback to the simulation.
- Compare simulated droop with measured droop.
- Add a simple PI controller in simulation.
- Explain why integral action reduces droop and why windup is a problem.

## Part 1: Algebraic Droop Model

Start with the steady-state open-loop relationship from Lab 4:

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
droop. Compare the prediction with Lab 5.

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

Use a temperature step from Lab 4 or Lab 5.

Use a trace in which every temperature value was calculated after averaging
between 100 and 1000 raw thermistor-voltage measurements, as required in Labs
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

Compare with Lab 5. The first-order model should capture some trends, but it
may not reproduce oscillations.

## Part 6: Why The First-Order Model May Not Oscillate

If your first-order model does not oscillate, that is useful. It means one
thermal mass with instantaneous measurement and actuation is too simple.

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

## What To Submit

Submit:

- derivation of the P-control droop equation,
- estimate of open-loop slope `S`,
- estimate of thermal time constant `tau`,
- open-loop simulation compared with one measured trace,
- P-only simulation compared with Lab 5 droop data,
- PI simulation compared with P-only simulation,
- short explanation of why the first-order model does or does not oscillate,
- windup thought-experiment answers,
- link to your GitHub modeling checkpoint.
