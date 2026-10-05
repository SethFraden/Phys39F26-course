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

!!! important "C4 and A2 deadlines"
    Complete the **C4 open-loop TEC calibration checkoff in class on Monday,
    October 5 (S10)**. The Moodle `C4 Team Checkoff` receipt is due by the end
    of class at **11:55 AM**. The separate A2 team PDF is due the same day at
    **6:00 PM**.

## Before Class

1. Review your Module 3 Arduino sketch and Python GUI.
2. Confirm that you can set PWM and heat/cool direction manually.
3. Review how your Python program records or displays temperature versus time.
4. Read the [hardware page section on the thermal safety switch](../../hardware.md#thermal-safety-switch).
5. Read the [hardware page section on the TEC](../../hardware.md#thermoelectric-cooler).

## Outside-Class Workload Budget For S8-S9

| Work | Planned time |
| --- | ---: |
| Read this assignment, review the safety boundary, and plan the data table | 30 minutes |
| Make the calibration graph and extract its two slopes | 15 minutes |
| Complete the guided A2 energy-balance analysis | 30 minutes |
| Check and submit A2 | 15 minutes |
| **Total outside class associated with S8-S9** | **1 hour 30 minutes** |

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

Continue using the measurement sequence from Module 2: average 
1000 raw thermistor-voltage measurements before calculating each temperature. Your data should update about once a second. If it is slower, something is wrong.
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

Do not intentionally heat the apparatus to 60 °C. Set the software limit to about 30C and verify that
the shutdown activates when you warm it up above that temperature and both PWM outputs are set to zero. Then restore the
limit to 60 °C and show the result to the instructor.

### Start The TEC

After the wiring and software interlock are approved:

1. Confirm again that PWM begins at `0` and the temperature is plausible.
2. Enable the power supply.
3. At low PWM, test both heat and cool and confirm that the temperature responds
   plausibly. In the strip chart, the PWM trace should be red during heating and
   blue during cooling.

Record the Arduino sketch filename, Python filename, serial port, power-supply
voltage, and power-supply current limit in your module notes. The latter values are written on the side of the power supply.

## Part 2: Choose Direction And PWM Values

The Arduino treats **PWM as an 8-bit nonnegative magnitude** and uses a separate
**1-bit heat/cool value** to select direction. Record both quantities for every
measurement. The Python strip chart communicates the heat/cool bit visually by
drawing the PWM trace red for heat and blue for cool.

Find one heating PWM value that produces **45 °C ± 2 °C at steady
state**. Separately, find one cooling PWM value that
produces **10 °C ± 1 °C at steady state**.
Those two endpoint values define the maximum useful PWM magnitude for heating
and cooling, respectively. The two maxima will generally differ.



For each direction, use five selected PWM magnitudes: 0%, approximately 25%,
50%, 75%, and 100% of **that direction's own** maximum useful PWM. Thus the
heating set should extend from 0 to the PWM that gives 45 °C ± 2 °C at
steady state, while the cooling set should extend from 0 to the PWM that gives
10 °C ± 1 °C at steady state. Record the exact integer values that you
actually use.

## Part 3: Measure Steady-State Temperature

Before collecting the steady-state measurements, modify the fixed temperature
y-axis used in Module 3 so small drifts are visible. Give GitHub Copilot the
following prompt:

<details markdown="1">
<summary>Suggested AI prompt: automatically scale the temperature axis</summary>

```text
Modify my existing PySide6 and pyqtgraph TEC strip-chart program. In Module 3,
the temperature y-axis was fixed. For Module 4, replace that fixed y-axis with
an automatically scaled temperature y-axis.

After every accepted temperature measurement, find the minimum and maximum
temperature among the samples currently visible in the rolling time window.
Set the temperature y-axis to extend 1 °C below the minimum and 1 °C above the
maximum. Always use at least a 6 °C total y-axis span; if the measured range is
smaller, center that 6 °C span on the measured temperatures. Update the y-axis
each time new data arrive, with no extra automatic padding.

Do not autoscale the PWM axis. Preserve the rolling time axis, controls, serial
communication, CSV logging, and red/blue PWM traces. Use a light, preferably
white, plot background so small temperature slopes remain visible. Comment the
new autoscaling code for a Python beginner.

The goal is to give enough magnification to see slow temperature drift without
making normal measurement noise dominate the display.
```

</details>

Measure steady state only at the five selected heating values and the five
selected cooling values from Part 2. Do not make a continuous 0–255 PWM
sweep. In each direction, work through only the five chosen values, beginning
at low PWM. After a sudden PWM change—for example, from 25% to 50%—the
temperature approaches its new value approximately exponentially. It never
becomes mathematically stationary: after one time constant it has completed
about 63% of the change, after two it has completed about 86% (14% remains),
and after three it has completed about 95% (5% remains).

Use the following practical definition of steady state for this lab. Estimate the time constant
from the response to a PWM step, wait about three time constants, and
then watch the trace for one additional minute. Because the temperature trace
has noise, do not expect a perfectly horizontal line. Call the temperature
steady when its net drift over that minute is no larger than the ordinary
short-term noise (the usual up-and-down wiggles) in the trace. If a clear
upward or downward drift remains, wait longer. Every recorded temperature in
this part is a **steady-state** temperature.

Use a table like this:

| Direction | PWM | Start Temperature (°C) | Steady Temperature (°C) | Time Waited (s) | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| Heat | 0 |  |  |  |  |
| Heat |  |  |  |  |  |
| Heat |  |  |  |  |  |
| Heat |  |  |  |  |  |
| Heat |  |  |  |  |  |
| Cool | 0 |  |  |  |  |
| Cool |  |  |  |  |  |
| Cool |  |  |  |  |  |
| Cool |  |  |  |  |  |
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
\chi_T = \frac{dT}{du},
\qquad u=\text{signed PWM}.
\]

It tells you how much the steady-state temperature changes for one PWM count
while the heat/cool direction is held fixed. Its units are **°C per PWM count**.
Here $u$ is positive for heating and negative for cooling. Both slopes are
positive: increasing $u$ raises the temperature on either branch. Moving
farther into negative PWM lowers the temperature. The heating branch is
typically steeper; a heating slope about twice the cooling slope is an
experimental observation to investigate, not a required result.
A simple finite-difference estimate is

\[
\chi_T \approx \frac{\Delta T}{\Delta u}.
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
m_h=\frac{dT_h}{du},
\qquad
m_c=\frac{dT_c}{du},
\qquad
r=\frac{m_h}{m_c}.
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

Here $o$ denotes the object face attached to the controlled block, and $r$
denotes the reservoir face coupled to the heat exchanger. For this analysis,
combine the TEC's passive conduction and all other passive heat leaks into one
effective conductance $G$. The simplified object energy balance is

\[
C\frac{dT}{dt}=\dot Q_{\mathrm{TEC}}-G(T-T_0).
\]

At steady state, conservation of energy requires all heat rates into and out of
the object to sum to zero. With the heat flows grouped into the two terms used
in this simplified model, that requirement becomes

\[
G(T-T_0)=\dot Q_{\mathrm{TEC}}.
\]

Complete the following three steps.

**Step 1 — Interpret the steady-state balance.** Identify the heat flows
represented by each term. For heating and cooling, state whether each heat
flow is into or out of the object.

**Step 2 — Average the PWM current.** Starting from

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

Explain why $\langle I^2\rangle\ne\langle I\rangle^2$ for PWM and compare the
predicted duty-cycle dependence with the linearity or curvature of your
measured graph.

**Step 3 — Derive the heating-to-cooling slope ratio.** Define signed duty
cycle $d=u/255$, with $D=|d|$. Let the positive quantities $\dot Q_P$ and
$\dot Q_J$ be the full-on Peltier and object-face Joule heat rates. Begin with

\[
\dot Q_{\mathrm{TEC}}=d\dot Q_P+|d|\dot Q_J.
\]

Derive the two branch slopes and show that

\[
\frac{dT_h}{dd}=\frac{\dot Q_P+\dot Q_J}{G},
\qquad
\frac{dT_c}{dd}=\frac{\dot Q_P-\dot Q_J}{G}.
\]

Both derivatives are positive in the cooling regime $\dot Q_P>\dot Q_J$,
and the heating derivative is larger. Since $d=u/255$, each measured slope
with respect to signed PWM includes a factor of $1/255$, which cancels from
their ratio $r=m_h/m_c$. Show that

\[
\boxed{\frac{\dot Q_J}{\dot Q_P}=\frac{r-1}{r+1}}.
\]

Evaluate $\dot Q_J/\dot Q_P$ using your measured $r$. If $r=2$, your
expression should give $\dot Q_J/\dot Q_P=1/3$.

<details markdown="1">
<summary>Show guidance: from the full TEC equation to the simplified balance</summary>

The first term in the full TEC equation is Peltier transport, the second is the
share of Joule heating delivered to the object face, and the third is passive
conduction through the TEC. In the simplified model,
$\dot Q_{\mathrm{TEC}}$ represents only the two current-dependent terms. The
TEC conduction term and the apparatus's other passive heat leaks are included
in $-G(T-T_0)$. Do not count TEC conduction again inside
$\dot Q_{\mathrm{TEC}}$.

Here $C$ is the thermal capacitance of the controlled object, and $T_0$ is its
zero-PWM temperature. At steady state, the individual heat flows need not be
zero; their sum is zero.

</details>

<details markdown="1">
<summary>Show guidance: average the PWM current</summary>

During one PWM period $\tau$, the current is the signed on-state value $I$ for
$D\tau$ and zero for the remaining $(1-D)\tau$, where $D=|u|/255$. Insert
these two time intervals into the integrals in step 2.

The Peltier term is proportional to $\langle I\rangle=DI$, while Joule heating
is proportional to $\langle I^2\rangle=DI^2$. For fixed on-state current, both
are linear in $D$. If one incorrectly used
$\langle I^2\rangle=\langle I\rangle^2=D^2I^2$, the predicted Joule term would
be quadratic in duty cycle and the susceptibility would vary with $D$. For a
continuously variable DC current rather than PWM,
$\langle I^2\rangle=\langle I\rangle^2$.

</details>

<details markdown="1">
<summary>Show guidance: derive the slope ratio</summary>

The Peltier term changes sign when current reverses, whereas Joule heating does
not. Therefore,

\[
\dot Q_{\mathrm{TEC},h}=d(\dot Q_P+\dot Q_J),
\qquad
\dot Q_{\mathrm{TEC},c}=d(\dot Q_P-\dot Q_J).
\]

Substitute each expression into the steady-state balance, solve for
$T_h(d)-T_0$ and $T_c(d)-T_0$, and differentiate with respect to $d$. Since
$d=u/255$, both slopes with respect to signed PWM contain the same factor of
$1/255$, which cancels from $r=m_h/m_c$.

</details>

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

Use the following numbered headings so each result can be matched to the work
in Parts 4 and 5. Show intermediate algebra, units, and substitutions clearly
enough that another student could reproduce each numerical result.

1. **Part 4: Graph and fits.** Include your temperature-versus-signed-PWM
   graph. Show heating and cooling as separate data sets, the fitted lines, and
   the PWM ranges used for each fit. Label both axes and give units.
2. **Part 5.1: Measured slopes.** Report the heating slope $m_h$, cooling-slope
   magnitude $m_c$, their units, and the measured ratio
   $r=m_h/m_c$. State whether either data set shows visible curvature and how
   that affected your choice of fitting range.
3. **Part 5.2: PWM and the slope-ratio model.** Prove that PWM gives
   $\langle I\rangle=DI$ and $\langle I^2\rangle=DI^2$. Then use the
   steady-state energy balance to derive the heating and cooling slopes and
   show that
   $\dot Q_J/\dot Q_P=(r-1)/(r+1)$. Substitute your measured $r$ and report
   the resulting numerical value of $\dot Q_J/\dot Q_P$.
4. **Part 5.3: Laird data-sheet calculation.** Cite the data-sheet page or
   table from which you obtained $R_M$, $I_{\max}$, $Q_{c,\max}$, and
   $\Delta T_{\max}$. Give each value, its units, meaning, and stated operating
   conditions. Calculate $\dot Q_{J,\max}$, infer $\dot Q_{P,\max}$, and then
   calculate
   $r_{\mathrm{Laird},\max}=(\dot Q_{P,\max}+\dot Q_{J,\max})/
   (\dot Q_{P,\max}-\dot Q_{J,\max})$. This is the heating-to-cooling slope
   ratio predicted from those maximum-current data.
5. **Part 5.4: Compare the ratios.** Compare your measured $r$ with
   $r_{\mathrm{Laird},\max}$. Explain why agreement need not be exact,
   including why duty cycle $D=1$ does not necessarily mean
   $I=I_{\max}$.
6. **Part 5.4: Passive conduction.** State the direction of passive heat flow
   when the object is hotter than room temperature and when it is colder.
   Explain why approximately symmetric passive conduction opposes both heating
   and cooling but does not, by itself, explain unequal slope magnitudes.

Do not repeat the C2/C3 circuit sketches, apparatus descriptions,
safety demonstration, or code documentation in A2. Retain the class data and
working code for later modules, but no new Git checkpoint is required for this
short assignment.

### A2 Rubric

| Criterion | Points |
| --- | ---: |
| Items 1-2: Part 4 graph, measured slopes, units, fitting ranges, and ratio are clearly presented | 2 |
| Item 3: PWM averaging proof, steady-state energy balance, slope-ratio derivation, and numerical result are correct | 3 |
| Item 4: Relevant Laird values and operating conditions are correctly located, cited, interpreted, and used in a dimensionally clear calculation | 2 |
| Items 5-6: Comparison and passive-conduction explanation show sound physical reasoning | 2 |
| PDF is concise, legible, and complete | 1 |

## C4 Oral Questions: Open-Loop TEC Calibration

These questions carry the Module 4 learning objectives into the announced C4
checkoff during class on **Monday, October 5 (S10)**. Prepare to answer one
primary question and, when useful, one brief follow-up using your apparatus,
graph, or the Laird data sheet. One team member submits the Moodle
`C4 Team Checkoff` receipt by **11:55 AM**.

1. Explain how the software temperature limit and the hardware thermal switch
   protect the TEC independently. How did you test the software limit without
   intentionally heating the apparatus to its limit?
2. Use your temperature-versus-signed-PWM graph to explain how you identified
   steady state and obtained the heating and cooling susceptibilities. State
   the units, fitting ranges, and any visible curvature.
3. Why can the heating and cooling susceptibility magnitudes differ? Explain
   what happens to the Peltier, Joule-heating, and passive-conduction terms when
   the current direction reverses.
4. Locate the required class-TEC specifications in the Laird data sheet and
   explain their meanings and operating conditions. Is your measured slope
   ratio consistent with the manufacturer data, and why does full duty cycle
   not necessarily mean maximum current?

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

Average exactly 1000 thermistor readings before calculating temperature. Define
temperatureLimitC as 60.0. Above that limit, set the commanded PWM to 0, write 0
to both H-bridge PWM outputs, continue serial reporting, and report that safety
shutdown is active. Keep the code simple and comment the new logic.
```

</details>
