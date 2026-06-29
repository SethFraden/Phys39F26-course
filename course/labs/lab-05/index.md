# Lab 5 Assignment: P-Only Temperature Control

## Purpose

Lab 5 closes the feedback loop for the first time. In Lab 4 you measured how
the TEC responds when you choose a PWM command directly. In Lab 5 you ask the
computer to choose the PWM command from the temperature error.

The first controller is proportional-only:

```text
PWM command = Kp * temperature error
```

This is not yet PI or PID control. The goal is to understand what proportional
feedback does well, what it cannot do, and why too much gain can make a real
thermal system oscillate.

## Theme

**P-Only Feedback: Droop, Gain, And Instability**

Use proportional feedback to regulate TEC temperature. Measure droop versus
gain and the onset of oscillation.

## Reading

Read these short selections before class. The goal is conceptual understanding,
not mastery of all the mathematics.

1. John Bechhoefer, *Feedback for Physicists*, pp. 788-790 and 804-805.
   - Focus on feedback, error, proportional/integral/derivative action, and
     why derivative control is sensitive to noise.
   - Skim equations involving Laplace-transform notation. We will translate
     the main ideas into time-domain Arduino/Python models.
   - The PDF will be provided through Brandeis course materials. Public DOI
     link: [Feedback for Physicists](https://doi.org/10.1103/RevModPhys.77.783)
2. [Wikipedia: PID controller](https://en.wikipedia.org/wiki/PID_controller)
   - Skim for vocabulary and the block diagram.
3. [NI: PID theory explained](https://www.ni.com/en/shop/labview/pid-theory-explained.html)
   - Focus on the practical meaning of proportional gain and the onset of
     oscillation.

## Safety Boundary

Before using feedback control:

1. The Lab 4 software temperature limit is present.
2. PWM starts at zero.
3. The Python GUI shows plausible temperature.
4. Heat and cool directions have the correct sign.
5. The power supply current limit is set by the instructor.
6. The setpoint is between **20 °C and 35 °C** unless the instructor approves a
   different range.

Stop immediately if the temperature moves in the wrong direction, the GUI
freezes, the PWM saturates unexpectedly, or sustained oscillations grow in
amplitude.

## Vocabulary

- **Setpoint**, `Tset`: the desired temperature.
- **Measured temperature**, `T`: the thermistor temperature.
- **Error**, `e = Tset - T`: how far the measured temperature is from the
  setpoint.
- **Control output**, `u`: the signed PWM command sent to the TEC.
- **Proportional gain**, `Kp`: the number that converts error into command.
- **Droop**: steady-state error that remains with proportional-only control.
- **Saturation**: the controller asks for a PWM command outside the allowed
  range.
- **Instability**: the feedback loop oscillates or diverges instead of settling.

## Before Class

1. Review your Lab 4 open-loop graph of steady-state temperature versus PWM.
2. Identify the approximate open-loop slope, `S = dT/dPWM`, near room
   temperature.
3. Confirm that your Arduino safety shutdown still works.
4. Write down the sign convention you will use:

```text
positive command = heat
negative command = cool
```

## Pre-Class Questions

1. If `Tset = 30 °C` and `T = 25 °C`, should the TEC heat or cool?
2. If `u` is measured in PWM counts and `e` is measured in °C, what are the
   units of `Kp`?
3. Why does proportional control require a nonzero error to produce a nonzero
   output?
4. What experimental symptom would tell you that `Kp` is too large?

## What You Will Do

- Implement P-only control in Python or Arduino.
- Verify the sign of the feedback loop at very low gain.
- Measure steady-state droop for several values of `Kp`.
- Increase `Kp` until oscillations begin.
- Measure oscillation amplitude, period, and frequency as functions of gain.
- Compare your droop data with the simple algebraic model.

## Part 1: Draw The Feedback Loop

Draw a block diagram with these pieces:

```text
Tset -> error e -> proportional controller -> signed PWM u -> TEC/block -> T
                         ^                                  |
                         |                                  |
                         +----------- thermistor -----------+
```

Label:

- `Tset`,
- `T`,
- `e = Tset - T`,
- `u`,
- `Kp`,
- the physical TEC/block/thermistor system.

## Part 2: Implement P-Only Control

Add a P-only mode to your Python GUI or Arduino sketch.

The controller should:

1. read the measured temperature,
2. calculate `error = Tset - T`,
3. calculate `u = Kp * error`,
4. convert the sign of `u` into heat/cool direction,
5. convert the magnitude of `u` into PWM,
6. clamp PWM to the allowed range,
7. send or apply the command,
8. keep plotting temperature, PWM, direction, setpoint, and error.

Start with a very small gain. Do not tune aggressively at first.

## Part 3: Sign Test At Low Gain

Before trying to regulate temperature:

1. Choose a setpoint slightly above room temperature.
2. Use a very small `Kp`.
3. Confirm that positive error produces heating.
4. Choose a setpoint slightly below room temperature.
5. Confirm that negative error produces cooling.

If the sign is wrong, stop and fix the sign convention before continuing.

## Part 4: Measure Droop Versus Gain

Choose one setpoint, for example **30 °C**, and measure the steady-state error
for several values of `Kp`.

Use a table like this:

| `Kp` | Setpoint (°C) | Final Temperature (°C) | Droop `Tset - T` (°C) | Final PWM | Notes |
| ---: | ---: | ---: | ---: | ---: | --- |
|  |  |  |  |  |  |

For each gain:

1. Start from PWM `0`.
2. Turn on P-only control.
3. Wait for the temperature to settle or clearly fail to settle.
4. Record final temperature, error, and PWM.
5. Save a strip chart trace.

Plot droop versus `Kp`.

## Part 5: Predict Droop From Lab 4

Use the Lab 4 open-loop slope:

```text
T = Tamb + S u
```

and the P-only controller:

```text
u = Kp * (Tset - T)
```

Combine them to predict the steady-state error:

```text
droop = Tset - T = (Tset - Tamb) / (1 + S*Kp)
```

Calculate the predicted droop for each `Kp` you tested. Overlay predicted and
measured droop on the same graph.

This model will not be perfect. Its job is to explain the main trend.

## Part 6: Find The Onset Of Oscillation

Increase `Kp` carefully until the temperature no longer settles smoothly.

For each gain near the onset of oscillation, record:

- `Kp`,
- setpoint,
- approximate mean temperature,
- oscillation amplitude,
- oscillation period,
- oscillation frequency,
- whether the PWM saturates.

Use a table like this:

| `Kp` | Stable? | Amplitude (°C) | Period (s) | Frequency (Hz) | Saturation? |
| ---: | --- | ---: | ---: | ---: | --- |
|  |  |  |  |  |  |

Do not let oscillations grow without supervision. Return to manual/PWM zero if
the run becomes unsafe.

## Part 7: Explain What The Simple Model Misses

The algebraic droop model predicts steady-state error. It does not explain
oscillations.

Write a paragraph explaining which physical effects might cause instability:

- thermal delay between TEC, block, and thermistor,
- finite response time of the heat exchanger,
- sampling interval in the controller,
- sensor noise,
- PWM saturation,
- using one thermistor to represent a multi-part thermal system.

## Part 8: GitHub Checkpoint

Commit your working P-only controller and notes.

```bash
git status
git add README.md arduino python docs data
git commit -m "Measure P-only temperature control"
git push
```

## What To Submit

Submit:

- feedback-loop block diagram,
- sign-test result,
- table of droop versus `Kp`,
- plot of measured and predicted droop versus `Kp`,
- strip chart traces for at least two gains,
- table of oscillation amplitude and frequency near instability,
- your P-only control code or a link to it,
- a short paragraph explaining why P-only control has droop,
- a short paragraph explaining why high gain can oscillate.
