# Lab 4 Assignment: Open-Loop TEC Calibration And Software Safety

## Purpose

Lab 4 turns the manually controlled TEC from Lab 3 into a measured process. You
will hold the TEC at several PWM settings, wait for the temperature to settle,
and measure the steady-state relationship between PWM command and temperature.

You will also add the first software safety interlock: the Arduino must disable
the PWM command if the measured temperature exceeds a chosen limit. The hardware
thermal switch remains the final protection, but your code should not rely on
the hardware cutoff as the normal way to stop an unsafe run.

This is still open-loop control. You are not asking the Arduino or Python to
hit a target temperature automatically. You are measuring how the physical
system responds to commands.

## Theme

**Open-Loop TEC Calibration And Software Safety**

Steady-state temperature versus PWM, heating/cooling asymmetry, and a
temperature-limit interlock in Arduino code.

## Safety Boundary

Before collecting data:

1. The Lab 3 pre-power checklist is complete.
2. The H-bridge outputs have been checked with TEC power off.
3. PWM starts at zero.
4. The power supply current limit is set by the instructor.
5. The Python display is showing plausible temperature values.
6. The hardware thermal switch has been identified.

During this lab, keep the measured temperature between **10 °C and 45 °C**. Stop
the run if the temperature moves unexpectedly, the display freezes, the power
supply current rises unexpectedly, or the TEC/driver becomes hot to the touch.

## Before Class

1. Review your Lab 3 Arduino sketch and Python GUI.
2. Confirm that you can set PWM and heat/cool direction manually.
3. Review how your Python program records or displays temperature versus time.
4. Read the [hardware page section on the thermal safety switch](../../hardware.md#thermal-safety-switch).
5. Read the [hardware page section on the TEC](../../hardware.md#thermoelectric-cooler).

## Pre-Class Questions

1. What does it mean for the TEC/block temperature to reach steady state?
2. Why should you wait before recording a steady-state temperature?
3. Why might heating and cooling have different slopes in a plot of temperature
   versus PWM?
4. Why is a software temperature limit useful even when a hardware thermal
   switch is present?

## What You Will Do

- Use your Lab 3 Python GUI and Arduino sketch to command the TEC manually.
- Measure steady-state temperature for several heating PWM values.
- Measure steady-state temperature for several cooling PWM values.
- Plot steady-state temperature versus PWM.
- Estimate $dT/dPWM$ for heating and cooling.
- Explain the asymmetry between heating and cooling.
- Add Arduino code that disables PWM if temperature exceeds 60 °C.
- Verify the safety logic without intentionally overheating the apparatus.

## Part 1: Prepare The Instrument

Start from your working Lab 3 setup.

1. Upload the Arduino sketch that receives PWM and heat/cool commands from
   Python.
2. Start the Python GUI.
3. Confirm that PWM begins at `0`.
4. Confirm that the measured temperature is plausible.
5. With TEC power off, verify on the oscilloscope that the Python command
   changes pins `9` and `10` as expected.
6. After instructor approval, connect TEC power.

Record the Arduino sketch filename, Python filename, serial port, power-supply
voltage, and power-supply current limit in your lab notes.

## Part 2: Choose PWM Values

Choose about four or five PWM values for heating and about four or five PWM
values for cooling. Include PWM `0`.

The exact values may depend on the apparatus, but the goal is to span a useful
range while keeping the temperature between **10 °C and 45 °C**.

Example planning table:

| Direction | PWM Values To Try |
| --- | --- |
| Heat | 0, 40, 80, 120, 160 |
| Cool | 0, 40, 80, 120, 160 |

Do not use a value just because it is in the example table. Adjust the range if
the temperature changes too quickly or approaches the safety boundary.

## Part 3: Measure Steady-State Temperature

For each PWM value:

1. Set heat/cool direction.
2. Set PWM.
3. Watch the temperature trace.
4. Wait until the temperature changes slowly enough to call it steady for this
   lab.
5. Record the steady-state temperature.
6. Return PWM to zero before switching direction or choosing a much larger PWM.

Use a table like this:

| Direction | PWM | Start Temperature (°C) | Steady Temperature (°C) | Time Waited (s) | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| Heat | 0 |  |  |  |  |
| Heat |  |  |  |  |  |
| Cool | 0 |  |  |  |  |
| Cool |  |  |  |  |  |

Also save at least one temperature-versus-time trace for heating and one for
cooling.

## Part 4: Plot Temperature Versus PWM

Make a graph of steady-state temperature $T$ versus PWM.

You may use Python, a spreadsheet, or another tool. The graph should show:

- heating data,
- cooling data,
- labeled axes,
- units for temperature,
- a caption or short note explaining how steady state was chosen.

Estimate $dT/dPWM$ for heating and cooling. A simple estimate is:

```text
dT/dPWM = change in steady-state temperature / change in PWM
```

If the graph is not very linear, say so. The slope is still useful as a local
or approximate measure of open-loop response.

## Part 5: Explain Heating/Cooling Asymmetry

Compare the magnitude of $dT/dPWM$ for heating and cooling.

Write a short explanation of why the slopes may differ. Your explanation should
refer to the physical apparatus, not only to the code. Useful ideas include:

- the TEC moves heat in one direction while also producing Joule heat,
- the heat exchanger rejects heat to the room but is not an infinite heat sink,
- the thermistor measures one location, not the entire thermal system,
- thermal contact, heat capacity, and room-temperature boundary conditions
  matter.

## Part 6: Add A Software Temperature Limit

Modify the Arduino sketch so that it disables TEC PWM if the measured
temperature exceeds **60 °C**.

The hardware thermal switch opens near 70 °C. That hardware switch protects the
apparatus even if software fails, but your Arduino code should act first.

Your code should:

- define a named constant for the software limit,
- check the measured temperature every loop,
- set both H-bridge PWM outputs to zero when the limit is exceeded,
- keep printing serial data so the Python GUI shows what happened,
- make it obvious in the serial output that the safety limit is active.

Do not test this by intentionally heating the apparatus to 60 °C. Instead, ask
the instructor how to verify the logic safely. For example, you may temporarily
lower the software limit to a temperature just above room temperature, confirm
that PWM shuts off, and then restore the 60 °C limit.

## Part 7: AI Prompt For The Safety Edit

You may ask an AI coding assistant for help, but test and understand the result.
A useful prompt is:

```text
I have an Arduino sketch for a TEC temperature-control lab. The sketch measures
temperature from a thermistor, receives PWM and heat/cool commands from a Python
GUI, and drives an H-bridge with PWM on pins 9 and 10.

Modify the sketch to add a software temperature safety limit.

Requirements:
- Define a named constant called temperatureLimitC with value 60.0.
- If measured temperature is greater than temperatureLimitC, set commanded PWM
  to 0 and write 0 to both H-bridge PWM outputs.
- Keep printing serial output so the Python GUI continues to update.
- Add a field to the serial output that says whether safety shutdown is active.
- Do not remove the existing temperature measurement or serial command parser.
- Keep the code simple and explain the new safety logic in comments.
```

After using AI, identify exactly which lines were changed and explain how the
safety limit works.

## Part 8: GitHub Checkpoint

Commit your work when the lab is complete.

```bash
git status
git add README.md arduino python docs data
git commit -m "Measure open-loop TEC response and add safety limit"
git push
```

Do not commit duplicate drafts or large accidental data files. Your repository
should make it clear which Arduino sketch and Python program were used for this
lab.

## What To Submit

Submit a short lab note containing:

- the PWM values used for heating and cooling,
- the steady-state data table,
- one heating trace and one cooling trace,
- a graph of steady-state temperature versus PWM,
- estimated $dT/dPWM$ for heating and cooling,
- your explanation of heating/cooling asymmetry,
- the Arduino safety-limit code or a link to it,
- a short description of how you verified the safety logic,
- a link to the GitHub commit or repository containing the organized Lab 4 work.

