# Module 4 Assignment: Open-Loop TEC Calibration And Software Safety

## Purpose

Turn the manually controlled TEC from Module 3 into a measured open-loop
process. You will measure how its steady-state temperature responds to PWM,
analyze why heating and cooling differ, and add a software temperature limit
while retaining the independent hardware thermal switch.

## Learning Objectives

By the end of this module, you should be able to:

- operate the TEC safely using independent hardware and software protection;
- measure the steady-state temperature response to signed PWM and determine
  the heating and cooling susceptibilities;
- explain unequal heating and cooling slopes using Peltier transport, Joule
  heating, and passive conduction; and
- extract relevant manufacturer specifications from a data sheet and evaluate
  whether experimental measurements are consistent with them.

## Before Class

1. Review your Module 3 Arduino sketch and Python GUI.
2. Confirm that you can set PWM and heat/cool direction manually.
3. Review how your Python program records or displays temperature versus time.
4. Read the [hardware page section on the thermal safety switch](../../hardware.md#thermal-safety-switch).
5. Read the [hardware page section on the TEC](../../hardware.md#thermoelectric-cooler).

## Outside-Class Workload Budget For S8

| Work | Planned time |
| --- | ---: |
| Read this assignment, review the safety boundary, and plan the data table | 30 minutes |
| Make the calibration graph and extract its two slopes | 15 minutes |
| Complete the guided A2 energy-balance analysis | 30 minutes |
| Check and submit A2 | 15 minutes |
| **Total outside class associated with S8** | **1 hour 30 minutes** |

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

For each direction, use five PWM magnitudes: 0%, approximately 25%, 50%, and
75% and 100% of that direction's maximum useful PWM.
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

Make a graph of steady-state temperature $T$ versus signed PWM, in which negative PWM is for cooling and positive PWM is for heating. Plot the
heating and cooling measurements as separate data sets: use red for heating and
blue for cooling, matching the color convention in the strip chart.

You may use Python, a spreadsheet, or another tool. The graph should show:

- red heating data,
- blue cooling data,
- labeled axes,
- units for temperature,
- a caption or short note explaining how steady state was chosen.

For each direction, estimate the **temperature susceptibility**, e.g. the slope of the curves,

\[
\chi_T = \frac{dT}{d(\mathrm{PWM})}.
\]

It tells you how much the steady-state temperature changes for one PWM count
while the heat/cool direction is held fixed. Its units are **°C per PWM count**.
A simple finite-difference estimate is

\[
\chi_T \approx \frac{\Delta T}{\Delta(\mathrm{PWM})}.
\]

If the graph is not very linear, say so. The slope is still useful as a local
or approximate measure of open-loop response.

## Part 5: Guided Heating/Cooling Energy-Balance Analysis

Complete the measurements and safety tests in class. At home, use the graph
from Part 4 to complete the following guided analysis. No additional physical
measurements are required.

### 1. Measure The Two Slopes

From the approximately linear region of your graph, determine

\[
m_h=\frac{dT_h}{d(\mathrm{PWM})},
\qquad
m_c=\frac{dT_c}{d(\mathrm{PWM})},
\qquad
r=\frac{m_h}{|m_c|}.
\]

Report both slopes with units of $^\circ\mathrm{C}$ per PWM count. State the
PWM range used for each fit and note any visible curvature.

### 2. Use Steady-State Energy Balance

Recall the full object-face TEC heat-flow equation from the
[Hardware discussion of the thermoelectric cooler](../../hardware.md#thermoelectric-cooler):

\[
\left\langle\dot Q_o\right\rangle
=S_M T_o\langle I\rangle
+\frac{1}{2}R_M\left\langle I^2\right\rangle
+K_M(T_r-T_o).
\]

The subscript $o$ denotes the **object face** of the TEC, which is attached to
the controlled metal block; the subscript $r$ denotes the **reservoir face**,
which is coupled to the heat exchanger. Thus $T_o$ and $T_r$ are the absolute
temperatures of those two faces.

The first term is Peltier transport, the second is the share of Joule heating
delivered to the object face, and the third is passive conduction through the
TEC. In the simplified model below, $\dot Q_{\mathrm{TEC}}$ represents the two
current-dependent terms. The TEC conduction term and the apparatus's other
passive heat leaks are combined into the effective conductance term
$-G(T-T_0)$. Do not count TEC conduction a second time inside
$\dot Q_{\mathrm{TEC}}$.

Let $C$ be the thermal capacitance of the controlled object, $T_0$ its
zero-PWM temperature, and $G$ the effective passive thermal conductance from
the object to its surroundings. Write the simplified energy balance as

\[
C\frac{dT}{dt}=\dot Q_{\mathrm{TEC}}-G(T-T_0).
\]

At steady state, $dT/dt=0$. The individual heat flows are generally not zero;
their sum is zero. Therefore,

\[
G(T-T_0)=\dot Q_{\mathrm{TEC}}.
\]

Before writing the TEC heat rate, derive how PWM averages current. During one
PWM period $\tau$, let the current be $I$ for a time $D\tau$ and zero for the
remaining $(1-D)\tau$, where $D$ is the duty cycle. Starting from

\[
\langle I\rangle=\frac{1}{\tau}\int_0^\tau I(t)\,dt,
\qquad
\langle I^2\rangle=\frac{1}{\tau}\int_0^\tau I^2(t)\,dt,
\]

show that

\[
\boxed{\langle I\rangle=DI},
\qquad
\boxed{\langle I^2\rangle=DI^2}.
\]

Explain why $\langle I^2\rangle$ is not generally equal to
$\langle I\rangle^2$, and connect this distinction to your measured
susceptibility. The Peltier term is proportional to $\langle I\rangle=DI$,
and Joule heating is proportional to $\langle I^2\rangle=DI^2$. For fixed
on-state current, both ideal contributions are therefore linear in $D$, giving
an approximately constant susceptibility. If one incorrectly used
$\langle I^2\rangle=\langle I\rangle^2=D^2I^2$, the predicted Joule term would
be quadratic in duty cycle and the susceptibility would vary with $D$. Compare
that prediction with the approximate linearity or curvature of your measured
temperature-versus-PWM graph.

Near room temperature, let the positive quantities $\dot Q_P$ and $\dot Q_J$
be the Peltier and object-face Joule heat rates, in watts, when the PWM is fully
on. With $D$ the dimensionless duty cycle, the cycle-averaged heat rates are
$D\dot Q_P$ and $D\dot Q_J$. The Peltier term changes sign when current
reverses, whereas Joule heating does not. Thus

\[
\dot Q_{\mathrm{TEC},h}=D(\dot Q_P+\dot Q_J),
\qquad
\dot Q_{\mathrm{TEC},c}=D(-\dot Q_P+\dot Q_J).
\]

Substitute each expression into the steady-state balance and solve for
$T_h(D)-T_0$ and $T_c(D)-T_0$. Differentiate with respect to $D$ to show that

\[
\frac{dT_h}{dD}=\frac{\dot Q_P+\dot Q_J}{G},
\qquad
\left|\frac{dT_c}{dD}\right|=\frac{\dot Q_P-\dot Q_J}{G}.
\]

PWM count is proportional to $D$, so the conversion factor cancels from the
ratio of the measured slopes. Show that

\[
\boxed{\frac{\dot Q_J}{\dot Q_P}=\frac{r-1}{r+1}}.
\]

Evaluate $\dot Q_J/\dot Q_P$ using your measured value of $r$. As an algebra
check, if $r=2$, the result should be $\dot Q_J/\dot Q_P=1/3$.

### 3. Find And Use The Laird Maximum-Current Data

Open the [Laird CP14-127-045 data sheet](../../references/laird-tec-cp14-127-045.pdf).
Manufacturer data sheets contain the information needed to design with a
component, but they are written for many users and can be difficult to read.
Part of this exercise is deciding which entries and operating conditions apply
to the class TEC.

Find the table or column for the class model at a hot-side temperature of
$27\ ^\circ\mathrm{C}$. Locate and record all of the following, with units:

- module resistance, $R_M$;
- maximum current, $I_{\max}$;
- maximum cold-side heat pumping at $\Delta T=0$, $Q_{c,\max}$; and
- maximum temperature difference, $\Delta T_{\max}$.

In one sentence each, explain what the quantity means and
state the operating condition attached to it. Do not ask an AI system for the
numbers before you have found them yourself. Afterward, you may give the data
sheet and your interpretation to an AI system and ask it to check whether you
selected the correct values and conditions.

These are data-sheet maximum-current conditions. They are not necessarily the
conditions in your apparatus when $D=1$: full duty means that the H-bridge is
continuously on, while the actual current depends on the power-supply voltage
and current limit, H-bridge voltage drop, wiring, and TEC resistance.

At $\Delta T=0$ the passive conduction term is zero. The simple symmetric TEC
model assigns half of the total Joule heat to each face, so calculate the
object-face Joule heat rate at the data-sheet maximum current:

\[
\dot Q_{J,\max}=\frac12 I_{\max}^2R_M.
\]

Cooling at the object face is the Peltier heat pumping minus this Joule heat:

\[
Q_{c,\max}=\dot Q_{P,\max}-\dot Q_{J,\max}.
\]

All three quantities in this equation are heat-transfer rates in watts. Use
this relation to find $\dot Q_{P,\max}$, and then calculate the data-sheet
maximum-current prediction

\[
r_{\mathrm{Laird},\max}
=\frac{\dot Q_{P,\max}+\dot Q_{J,\max}}
{\dot Q_{P,\max}-\dot Q_{J,\max}}.
\]

### 4. Interpret The Comparison

Compare $r_{\mathrm{Laird},\max}$ with your measured $r$. Do not assume that
they should agree. State why $D=1$ does not necessarily imply
$I=I_{\max}$. Also consider PWM rather than steady DC, finite temperature
differences, passive heat paths, changing material properties, and fitting a
slightly curved graph with one slope.

Also answer: when the object is hotter than room temperature, which way does
passive heat flow? What about when the object is colder? Explain why
approximately symmetric passive conduction opposes both heating and cooling
but does not by itself explain unequal slope magnitudes.

## Part 6: Submit A2

### A2: TEC Heating And Cooling Analysis

- **Type:** team, 10 points
- **Due:** Monday, October 5, at **6:00 PM**
- **Moodle file:** `A2_Lastname_Lastname.pdf`
- **Moodle submission:** Each student uploads the team PDF separately;
  teammates may upload the same PDF
- **Repository file:** none required for this short analysis

Submit a **one-to-two-page PDF** containing:

1. your Part 4 graph, showing the heating and cooling measurements as separate
   data sets with fitted lines over the ranges used;
2. your measured heating and cooling slopes, their units, and their ratio $r$;
3. the PWM average-current proof, the steady-state slope derivation, and its
   numerical result;
4. the cited Laird data-sheet values, your explanation of their meanings and
   conditions, and the resulting calculation and predicted ratio;
5. a comparison of the measured and data-sheet ratios;
6. your answer about passive conduction; and
7. a concise conclusion of approximately 100-150 words explaining what the
   measurements imply about Peltier transport, Joule heating, and conduction.

Do not repeat the C2/C3 circuit sketches, apparatus descriptions,
safety demonstration, or code documentation in A2. Retain the class data and
working code for later modules, but no new Git checkpoint is required for this
short assignment.

### A2 Rubric

| Criterion | Points |
| --- | ---: |
| Part 4 graph, measured slopes, units, fitting ranges, and ratio are clearly presented | 2 |
| PWM averaging proof, steady-state energy balance, and slope-ratio derivation are correct | 3 |
| Relevant Laird values and operating conditions are correctly located, cited, interpreted, and used in a dimensionally clear calculation | 2 |
| Comparison and passive-conduction explanation show sound physical reasoning | 2 |
| PDF is concise, legible, and complete | 1 |

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
