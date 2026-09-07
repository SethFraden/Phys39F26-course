# Module 4 Assignment: Open-Loop TEC Calibration And Software Safety

## Module At A Glance

Module 4 turns the manually controlled TEC from Module 3 into a measured process. You
will hold the TEC at several PWM settings, wait for the temperature to settle,
and measure the steady-state relationship between PWM command and temperature.

You will also add the first software safety interlock: the Arduino must disable
the PWM command if the measured temperature exceeds a chosen limit. The hardware
thermal switch remains the final protection, but your code should not rely on
the hardware cutoff as the normal way to stop an unsafe run.

This is still open-loop control. You are not asking the Arduino or Python to
hit a target temperature automatically. You are measuring how the physical
system responds to commands.

## Before Class

1. Review your Module 3 Arduino sketch and Python GUI.
2. Confirm that you can set PWM and heat/cool direction manually.
3. Review how your Python program records or displays temperature versus time.
4. Read the [hardware page section on the thermal safety switch](../../hardware.md#thermal-safety-switch).
5. Read the [hardware page section on the TEC](../../hardware.md#thermoelectric-cooler).

## Outside-Class Workload Budget For S8

| Work | Planned time |
| --- | ---: |
| Read this assignment and review the safety boundary | 30 minutes |
| Prepare the direction/PWM table, steady-state criterion, and data-file plan | 45 minutes |
| Analyze the in-class runs and make the required graph | 120 minutes |
| Write, check, commit, push, and submit A2 | 60 minutes |
| **Total outside class associated with S8** | **3 hours 15 minutes** |

All physical runs and safety tests occur in class. If analysis reveals that a
measurement must be repeated, identify it for the next supervised opportunity
rather than exceeding the four-hour outside-class limit.

## Pre-Class Questions

1. What does it mean for the TEC/block temperature to reach steady state?
2. Why should you wait before recording a steady-state temperature?
3. Why might heating and cooling have different slopes in a plot of temperature
   versus PWM?
4. Why is a software temperature limit useful even when a hardware thermal
   switch is present?

## Part 1: Prepare The Instrument And Add The Safety Interlock

Start from your working Module 3 setup.

### Safety And Startup Checklist

Start with the actuator power supply turned off and disconnected. This current
path was built in Module 3, but it must be inspected before calibration.

1. Confirm that 18 AWG stranded copper wire is used for every high-current
   connection:
   - power supply to H-bridge `B+` and `B-`,
   - H-bridge `M+` and `M-` to the TEC circuit, and
   - both wires connected to the thermal switch.
2. Confirm that both Module 3 female spade crimps remain secure and that a
   multimeter shows continuity through the closed thermal switch.
3. Confirm that the thermal switch remains in series with the TEC current path
   so opening the switch interrupts TEC current independently of the Arduino
   software.
4. Confirm that the H-bridge outputs were checked with TEC power off in Module 3.
5. Upload the Arduino sketch that receives PWM and heat/cool commands from
   Python, start the Python GUI, and confirm that PWM begins at `0`.
6. Confirm that the displayed temperature is plausible.
7. Draw the complete high-current path in your notebook and ask the instructor
   to inspect the wire gauge, polarity, spade connections, thermal-switch
   placement, and power-supply current limit.

Do not enable actuator power until the instructor approves the completed
wiring.

During this module, keep the measured temperature between **10 °C and 45 °C**.
Stop the run if the temperature moves unexpectedly, the display freezes, the
power-supply current rises unexpectedly, or the TEC or H-bridge becomes hot to
the touch.

### Add And Verify The Software Temperature Limit

Continue using the measurement sequence from Module 2: average between 100 and
1000 raw thermistor-voltage measurements before calculating each temperature.
This applies to the displayed temperature, recorded data, and software safety
check.

Before collecting calibration data, modify the Arduino sketch so that it
disables TEC PWM if the measured temperature exceeds **60 °C**. The hardware
thermal switch opens near 70 °C and remains the independent final protection.

Your code should:

- define a named constant for the software temperature limit,
- check the averaged temperature every loop,
- set both H-bridge PWM outputs to zero when the limit is exceeded,
- continue printing serial data so the Python GUI shows what happened, and
- report clearly in the serial output when the safety shutdown is active.

Do not intentionally heat the apparatus to 60 °C. With TEC power off, temporarily
set the software limit just below the measured room temperature and verify that
the shutdown activates and both PWM outputs are set to zero. Then restore the
limit to 60 °C and show the result to the instructor.

### Start The TEC

After the wiring and software interlock are approved:

1. Confirm again that PWM begins at `0` and the temperature is plausible.
2. Enable the power supply using the instructor-approved voltage and current
   limit.
3. At low PWM, test both heat and cool and confirm that the temperature responds
   plausibly. In the strip chart, the PWM trace should be red during heating and
   blue during cooling.

Record the Arduino sketch filename, Python filename, serial port, power-supply
voltage, and power-supply current limit in your module notes.

## Part 2: Choose Direction And PWM Values

The Arduino treats **PWM as an 8-bit nonnegative magnitude** and uses a separate
**1-bit heat/cool value** to select direction. Record both quantities for every
measurement. The Python strip chart communicates the heat/cool bit visually by
drawing the PWM trace red for heat and blue for cool.

Begin with a cautious exploratory sweep in each direction. Start at low PWM and
increase it gradually while watching the temperature and power-supply current.
Identify a maximum useful PWM magnitude for heating and another for cooling.
The maxima may differ. They should span a useful temperature range without
driving the apparatus outside **10 °C to 45 °C**.

For each direction, use five PWM magnitudes: `0`, approximately 25%, 50%, and
75% of that direction's maximum useful PWM, and the maximum useful PWM itself.
Record the exact integer values that you actually use.

## Part 3: Measure Steady-State Temperature

For each PWM value:

1. Set heat/cool direction.
2. Set PWM.
3. Watch the temperature trace.
4. Wait until the temperature changes slowly enough to call it steady for this
   module.
5. Record the steady-state temperature.

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

Make a graph of steady-state temperature $T$ versus PWM magnitude. Plot the
heating and cooling measurements as separate data sets: use red for heating and
blue for cooling, matching the color convention in the strip chart.

You may use Python, a spreadsheet, or another tool. The graph should show:

- red heating data,
- blue cooling data,
- labeled axes,
- units for temperature,
- a caption or short note explaining how steady state was chosen.

For each direction, estimate the **temperature susceptibility**

\[
\chi_T = \frac{dT}{d(\mathrm{PWM})}.
\]

It tells you how much the steady-state temperature changes for one PWM count
while the heat/cool direction is held fixed. Its units are **°C per PWM count**.
A simple estimate is:

```text
dT/dPWM = change in steady-state temperature / change in PWM
```

If the graph is not very linear, say so. The slope is still useful as a local
or approximate measure of open-loop response.

## Part 5: Explain Heating/Cooling Asymmetry

Compare the magnitude of $\chi_T$ for heating and cooling.

Write a short explanation of why the slopes may differ. Your explanation should
refer to the physical apparatus, not only to the code. Useful ideas include:

- the TEC moves heat in one direction while also producing Joule heat,
- the heat exchanger transfers heat from the TEC to the room but is not an infinite heat sink,
- the thermistor measures one location, not the entire thermal system,
- thermal contact, heat capacity, and room-temperature boundary conditions
  matter.

## Part 6: Assemble And Submit A2

Complete all physical runs and safety tests during S7-S8. Fill the data table
and write short observations while each run is fresh. Before shutting down or
changing the apparatus, make sure you have the evidence needed for A2.

### A2: Open-Loop TEC Instrument Note

- **Type:** team, 10 points
- **Due:** Monday, September 28, at **6:00 PM**
- **Moodle file:** `A2_Lastname_Lastname.pdf`
- **Moodle submission:** Each student uploads the team PDF separately;
  teammates may upload the same PDF
- **Repository file:** `docs/assessments/a2_open_loop_tec.md`

This early formal assessment establishes expectations for dimensional graphs,
physical interpretation, reproducible code/data links, safety evidence, and a
clear Git checkpoint. Reserve about **60 minutes** to finish the paper and
submission after the in-class measurements and graph are complete.

Use `docs/module_notes/module_04_open_loop_tec.md` for the working note,
`data/module_04/` for raw data, `docs/figures/module_04/` for figures, and
`docs/assessments/a2_open_loop_tec.md` for the repository version of A2.

Submit a short instrument note containing:

- a wiring diagram showing the 18 AWG high-current path and the thermal switch
  in series with the TEC,
- the power-supply and software safety settings,
- the direction/PWM-magnitude table and the criterion you used to identify
  steady state,
- the retained raw time-series data and one labeled trace for each direction,
- a dimensional graph of steady-state temperature versus PWM magnitude, with
  separate red heating and blue cooling data,
- the heating and cooling values of $\chi_T$ in °C per PWM count,
- your explanation of heating/cooling asymmetry,
- links to the exact Arduino safety-limit code and Python program used,
- evidence that the safety test set both H-bridge outputs to zero while serial
  reporting continued, and
- a link to the GitHub commit or repository containing the organized Module 4 work.

### GitHub Checkpoint

Commit the organized work before submitting A2.

```bash
git status
git add README.md arduino python docs data
git commit -m "Measure open-loop TEC response and add safety limit"
git push
```

Do not commit duplicate drafts or large accidental data files. Your repository
should make it clear which Arduino sketch, Python program, data, and figures
support the submitted note.

### A2 Rubric

| Criterion | Points |
| --- | ---: |
| Direction/PWM-magnitude table, steady-state criterion, and retained raw data are complete | 2 |
| Heating/cooling traces and dimensional steady-temperature plot are credible | 2 |
| Asymmetry, susceptibility, saturation, and operating limits are interpreted physically | 2 |
| Software and hardware safety behavior are demonstrated and explained | 2 |
| PDF, code/data links, and cited Git checkpoint are clear and on time | 2 |

## Appendix: Optional AI Prompt For The Safety Edit

You may ask an AI coding assistant for help, but you must test and understand
the result. After using AI, identify the lines that changed and explain how the
safety limit works.

<details markdown="1">
<summary>Show a possible prompt</summary>

```text
My Arduino sketch measures TEC temperature from a thermistor, receives PWM
magnitude and heat/cool commands from a Python GUI, and drives an H-bridge using
pins 9 and 10. Add a software temperature safety limit without removing the
existing measurement, serial reporting, or command parser.

Average 100 to 1000 thermistor readings before calculating temperature. Define
temperatureLimitC as 60.0. Above that limit, set the commanded PWM to 0, write 0
to both H-bridge PWM outputs, continue serial reporting, and report that safety
shutdown is active. Keep the code simple and comment the new logic.
```

</details>
