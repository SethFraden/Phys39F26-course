# Module 7, Part III: Rod Instrument, Step Response, And Stationary Fin

This is the experimental part of Module 7. It builds on [Part I: Thermal
Transport Foundations](../theory-bridge-chapter-1/index.md) and [Part II: Finite
And Infinite Rod Theory](../fin-design-derivation/index.md).

## Purpose

In Modules 1-6, one or two temperatures were enough to describe the TEC process.
The aluminum rod cannot be treated as one thermal lump. Its temperature depends
on position and time:

\[
T=T(x,t).
\]

In this module you will build and validate the multichannel rod instrument,
measure a non-oscillatory step response, and measure the steady temperature
profile. The steady profile gives the first quantitative evidence of heat loss
from the rod's side. The sinusoidal Angstrom experiment begins in Module 8.

### Thermistor Channels And Calibration

The Arduino Uno R3 has six analog input channels, `A0` through `A5`, feeding one
multiplexed 10-bit analog-to-digital converter. Use one channel for the
thermistor in the TEC base and the other five channels for five thermistors
along the rod. The converter samples the six channels in rapid sequence rather
than at exactly the same instant. This delay is negligible on the thermal
timescales measured here.

The purpose here is to assign each thermistor a permanent channel,
cross-calibrate all six measurement chains, and establish the sensor map used
for the non-oscillatory step response and stationary-fin profile. Module 8
reuses the same calibrated sensor map for the oscillatory Angstrom experiment.
The rod has more thermistor holes than the five available rod channels, so the
five rod thermistors can be distributed among selected holes to obtain a useful
range of positions and temperatures. Holes in the first group are nominally
spaced at \(1/2\)-inch intervals; holes in the second group are nominally
spaced at \(1\)-inch intervals. Treat these as
orientation values only; measure and record the actual positions you use.

The course rod is **6061-T6 aluminum** with a nominal diameter of \(1/2\) inch,
or \(12.7\ \mathrm{mm}\). The **analysis base** at \(x=0\) is the first
thermistor hole in the rod, occupied by rod thermistor 1. It is not the physical
end of the rod and it is not the thermistor embedded in the TEC. Measure the
positions of the other four rod thermistors relative to this origin. Define
the analyzed length \(L\) as the distance from the first thermistor hole to the
rod tip. Also record the rod's overall physical length, diameter \(d\), and
their uncertainties. The TEC thermistor monitors the actuator, while the
measured temperature of rod thermistor 1 supplies the boundary condition
\(T(0,t)\) for the rod model.

Use one model-testing cycle throughout Part III:

1. **Predict:** use the Part I and Part II theory to predict the qualitative
   transient, the stationary profile, and the importance of the end and radius.
2. **Measure:** acquire synchronized, calibrated temperature data with the
   geometry and settings needed to interpret them.
3. **Compare:** fit the finite and semi-infinite models and inspect residuals,
   parameter values, and uncertainties.
4. **Judge:** state which assumptions the evidence supports and where the
   model is inadequate.

## Schedule And Due Work

| Session | In class | Due |
| --- | --- | --- |
| S16, Mon. Oct. 26 | Review the finite-rod theory prepared at home; compare finite and semi-infinite predictions; calculate the transverse Biot number; map and calibrate sensors; begin baseline and step-response measurements | Module 7 home preparation |
| S17, Wed. Oct. 28 | Complete the synchronized step response and stationary profile; fit finite-length and semi-infinite stationary profiles | **A4: finite-rod model and validity checks**; **C5: Rod instrument and data-acquisition chain** |

## Outside-Class Workload Budget

| Session | Work | Planned time |
| --- | --- | ---: |
| S16 | Complete the required Part I and Part II reading route, including the selected Lienhard sections and derivation guide | 150 minutes |
| S16 | Begin A4: identify boundary conditions and organize the finite-length derivation | 75 minutes |
| S16 | **Total associated with S16** | **3 hours 45 minutes** |
| S17 | Complete and check the individual A4 calculations | 180 minutes |
| S17 | Prepare the sensor-map and calibration record | 45 minutes |
| S17 | **Total associated with S17** | **3 hours 45 minutes** |

The reading allocation includes time to follow the derivation, not merely read
the prose. Save all rod measurements during class; the outside-class budget is
for theory, analysis, documentation, and submission.

## Learning Objectives

The objectives below are listed in priority order. By the end of Module 7,
Part III, you should be able to:

1. Build and document a spatial temperature measurement by defining sensor
   coordinates, cross-checking the thermistors, and acquiring synchronized
   $T(x,t)$ data with units, timestamps, and experimental metadata.
2. Use the finite-length solution and transverse Biot number to make separate,
   quantitative decisions about whether the far end and radial temperature
   variation may be neglected.
3. Distinguish a transient from a steady spatial profile and explain why a
   temperature disturbance arrives later and is smaller farther from the
   heated base.
4. Fit finite-length and semi-infinite stationary-fin models, examine their
   residuals, and interpret the fitted decay coefficient and decay length.
5. Explain what the steady experiment can determine and why it cannot determine
   the thermal conductivity and side heat-transfer coefficient separately.

## Part III Vocabulary And Notation

Review the [foundational vocabulary in Part
I](../theory-bridge-chapter-1/index.md#module-7-vocabulary-and-notation) and the
[fin-model vocabulary in Part
II](../fin-design-derivation/index.md#part-ii-vocabulary-and-notation). The
terms below connect that theory to the experiment and its analysis.

| Term | Meaning |
| --- | --- |
| Temperature field, \(T(x,t)\) | Temperature as a function of both position along the rod and time. |
| Environmental temperature, \(T_\infty\) | The temperature of the environment far from the rod. In this experiment, it is the room temperature measured away from the heated apparatus. |
| Excess temperature, \(\theta(x,t)=T(x,t)-T_\infty\) | Rod temperature measured relative to the environment. |
| Thermal diffusivity, \(\alpha=k/(\rho c)\) | The coefficient controlling axial spreading in the Part III model; units m\(^2\)/s. This is Lienhard's notation. |
| Side-loss rate, \(\nu=hP/(\rho cA)\) | The fractional rate, in s\(^{-1}\), at which side convection removes excess thermal energy in the one-dimensional model. |
| Decay coefficient, \(m=\sqrt{hP/(kA)}=\sqrt{\nu/\alpha}\) | The spatial decay rate of the stationary profile; \(1/m\) is the decay length. |
| Sensor map | A record of each channel name, thermistor position, coordinate origin and direction, and position uncertainty. |
| Calibration or cross-check | A comparison under a common temperature condition used to identify sensor offsets or other channel differences. |
| Baseline | Measurements made before the imposed temperature change, used to establish room temperature and initial sensor readings. |
| Step response | The measured evolution of \(T(x,t)\) after the base-temperature command changes. |
| Boundary condition | The measured or prescribed behavior at a boundary. For the rod model, the measured temperature of rod thermistor 1 at the first hole is the boundary condition \(T(0,t)\); the TEC setpoint and TEC-thermistor temperature describe the actuator that creates it. |
| Stationary profile | The position-dependent temperature after changes with time have become negligible according to a stated criterion. |
| Model fit | Estimation of model parameters by comparing a predicted curve with measured data. |
| Residual | Measured value minus model prediction at the same position or time. Residual structure can reveal model inadequacy. |
| Uncertainty | A quantitative estimate of the plausible range of a measured or fitted result. |
| Metadata | Information needed to interpret and reproduce a run, including units, timestamps, channel labels, geometry, settings, and experimental notes. |

## Reading And Preparation

1. Read Chapter 1 of [Lienhard and Lienhard, *A Heat Transfer Textbook*](../../references/lienhard-heat-transfer-textbook-v6.pdf).
2. Review [Module 7, Part I: Thermal Transport Foundations](../theory-bridge-chapter-1/index.md).
3. For the S16 lecture and S17 guided study, read Lienhard Section 4.5,
   textbook pp. 163-173. Work through the derivation rather than reading only
   the final formulas.
4. Use [Fin Design: From A Finite Rod To An Infinite Rod](../fin-design-derivation/index.md)
   as the equation-by-equation guide to Lienhard Eqs. (4.27)-(4.51).
5. Complete `A4`, including Lienhard Problems 1.3, 4.12,
   and 4.20. Problem 1.3 is assigned in
   [Module 7, Part I](../theory-bridge-chapter-1/index.md#a4-part-i-lienhard-problem-13).

## Model

Part II set the energy-storage term to zero to obtain the stationary fin
equation. We now restore that term while retaining distributed side cooling,
so the model describes both the transient response and the stationary profile
that it approaches.

Let

\[
\theta(x,t)=T(x,t)-T_\infty,
\]

where $T_\infty$ is the temperature of the environment far from the rod. For
the course experiment, $T_\infty$ is the room temperature measured away from
the heated apparatus.

For a uniform rod with cross-sectional area $A$, perimeter $P$, density $\rho$,
specific heat $c$, thermal conductivity $k$, and side heat-transfer coefficient
$h$, conservation of energy gives

\[
\rho c A\frac{\partial\theta}{\partial t}
=kA\frac{\partial^2\theta}{\partial x^2}-hP\theta.
\]

Every term has units of power per unit length, watts per meter. Dividing by
$\rho cA$ gives

\[
\frac{\partial\theta}{\partial t}
=\alpha\frac{\partial^2\theta}{\partial x^2}-\nu\theta,
\qquad
\alpha=\frac{k}{\rho c},
\qquad
\nu=\frac{hP}{\rho c A}.
\]

Here $\alpha$ has units of square meters per second and $\nu$ has units of
inverse seconds.

At steady state,

\[
\frac{d^2\theta}{dx^2}-m^2\theta=0,
\qquad
m^2=\frac{hP}{kA}=\frac{\nu}{\alpha}.
\]

This second-order equation requires two boundary conditions. For the analyzed
section, rod thermistor 1 supplies the measured temperature at the analysis
base \(x=0\), and the tip is treated as insulated. Part II then gives the
complete finite-rod profile

\[
\frac{\theta(x)}{\theta(0)}
=\frac{\cosh[m(L-x)]}{\cosh(mL)}.
\]

When the far end has negligible influence over the measured region, this
finite profile approaches the semi-infinite approximation

\[
\theta(x)=\theta_0 e^{-mx}.
\]

The fitted $m$ quantifies the competition between axial conduction and side
loss. It does **not** determine $k$ and $h$ separately. The periodic Angstrom
experiment in Module 8, Part I, supplies the second independent measurement.

## Before The Experiment: Model-Validity Checks

### Length: Solve It First

For the section of rod extending a distance \(L\) from the first thermistor
hole to the insulated tip, the exact normalized stationary solution is

\[
\Theta_{\mathrm{finite}}(x)
=\frac{\theta(x)}{\theta(0)}
=\frac{\cosh[m(L-x)]}{\cosh(mL)}.
\]

The semi-infinite model is the limiting expression

\[
\Theta_\infty(x)=e^{-mx}.
\]

Calculate the relative error at every sensor position:

\[
\epsilon_T(x)=
\frac{\left|\Theta_{\mathrm{finite}}(x)-\Theta_\infty(x)\right|}
{\left|\Theta_{\mathrm{finite}}(x)\right|}.
\]

State an acceptable error before deciding whether the far end may be ignored.
A reasonable starting criterion is \(\epsilon_T<5\%\) at every sensor used in
the analysis, but record and justify a different threshold if the intended
measurement requires one. The product \(mL\) is useful, but the answer also
depends on which sensor and which observable you use.

### Radius: Check The Transverse Biot Number

For a circular rod,

\[
\mathrm{Bi}_{\perp}=\frac{h(A/P)}{k}=\frac{hR}{2k}.
\]

The small-Biot condition \(\mathrm{Bi}_{\perp}\ll1\) means radial conduction
is fast enough that a cross section can be represented by one temperature.
Calculate \(\mathrm{Bi}_{\perp}\) using the rod radius and a justified range of
\(h\) and \(k\). This is a separate test from the finite-length test.

### A4: Finite-Rod Model And Validity Checks

`A4` is a 10-point individual written assignment based on Module 7, Parts I
and II. It does not require the temperature data collected in Part III. Submit
one PDF organized under the following four headings. Show units and dimensional
checks throughout.

**Part 1. Apply Fourier's law.** Complete Lienhard Problem 1.3 as assigned in
[Part I](../theory-bridge-chapter-1/index.md#a4-part-i-lienhard-problem-13).
Show how Fourier's law produces each result, include units, and identify any
physically unreasonable result.

**Part 2. Build the stationary finite-rod model.** Starting from conservation
of energy, Fourier's law, and Newton's law of cooling, derive the stationary
fin equation with side heat loss. Follow the finite-fin solution in Lienhard
Section 4.5, showing the principal steps from the differential equation to the
solution. State the two boundary conditions and explain what each means
physically.

**Part 3. Test the finite-length approximation.** Complete Lienhard Problem
4.12 to obtain the semi-infinite limit. Use Example 4.8 and Problem 4.20 to
quantify the effect of approximating the tip boundary condition. Calculate
\(mL\) and \(\epsilon_T(x)\) for every course-rod sensor. Use the supplied
course-rod parameters and sensor positions if your measured values are not yet
available. Conclude whether the course rod may be treated as semi-infinite,
and state the sensor positions and error criterion on which your conclusion
depends.

**Part 4. Test the one-dimensional approximation.** Calculate
\(\mathrm{Bi}_{\perp}\) for the course rod. Conclude separately whether each
cross section may be represented by one temperature. Do not combine this
radius conclusion with the finite-length conclusion from Part 3.

Then answer this brief application question: an electronic heat sink in air
and a spacecraft radiator both use extended surfaces. Which one can be modeled
with Newton's law of cooling? Explain why convection is absent in space and
write the radiative heat-flux law that replaces it.

The [submission details and rubric](#a4-submission-and-rubric) appear near the
end of this page.

### Prediction Record Before Heating

Before applying heat to the course rod, record the provisional values of
\(\mathrm{Bi}_{\perp}\), \(mL\), and \(\epsilon_T(x)\) at every sensor.
Predict:

1. the order in which the sensors will respond to a base-temperature step,
2. how the response amplitude will change with distance from the base,
3. the qualitative shape of the stationary temperature profile, and
4. whether the measured region should reveal the finite tip.

Use supplied parameters when measured values are not yet available. Return to
these predictions after fitting the stationary data and state which were
supported by the evidence.

## Software Extension For Six-Channel Rod Measurements

Do not replace the working temperature-control system from Module 6. Extend
the Arduino sketch and Python GUI that you have already tested. The TEC-base
thermistor remains the feedback and safety sensor. The five rod thermistors
are additional measurement channels; they do not enter the PI-control law.

Develop and test the software in the stages below. Keep each stage working
before asking Copilot to make the next change. Copilot may write code, but you
are responsible for checking the pin assignments, serial interface, units,
safety behavior, and saved data.

### Stage 1: Extend The Arduino Measurement

Use all six Uno analog inputs. Unless your documented wiring requires a
different assignment, use `A0` for the TEC-base thermistor and `A1` through
`A5` for rod thermistors 1 through 5. The Uno has one analog-to-digital
converter and selects the six inputs sequentially. Read and average each
channel, then send all six temperatures together in one measurement record.
The resulting time offsets between channels are negligible compared with the
rod's thermal response, but the Arduino time must be measured and transmitted
with every record.

The revised sketch must:

- retain the existing PI control, zero-PWM startup, H-bridge pin assignments,
  temperature limit, and hardware-safety instructions,
- use the TEC-base thermistor alone for feedback and the software temperature
  limit,
- calculate all six temperatures with the same thermistor conversion,
- label every transmitted field unambiguously,
- emit exactly one complete measurement record per acquisition cycle, and
- continue accepting the existing commands from the Python GUI.

Use a stable serial record such as

```text
DATA,time_s,tec_C,rod1_C,rod2_C,rod3_C,rod4_C,rod5_C,pwm,heat_cool,setpoint_C,safety
DATA,12.50,23.41,23.38,23.36,23.34,23.31,23.29,120,1,45.00,OK
```

The first line is a header printed once at startup; each later `DATA` line is
one measurement. Status and error messages must not begin with `DATA`. This
distinction lets both Python and the serial microSD logger recognize valid
records without confusing them with diagnostic text.

<details markdown="1">
<summary>Suggested Copilot prompt: six-channel Arduino acquisition</summary>

```text
Inspect the working Module 6 Arduino TEC-controller sketch that is open in VS
Code. Extend this sketch; do not replace it with a new program. Preserve its PI
control, serial-command parser, H-bridge pins, zero-PWM startup, software
temperature limit, and all safety behavior.

Use A0 for the TEC-base thermistor and A1-A5 for rod thermistors 1-5. The A0
temperature must remain the only temperature used by the PI controller and
software safety limit. Read and average all six analog channels and convert
each reading with the sketch's existing thermistor-conversion function. Keep
the number of averages as a named constant. Record the Arduino elapsed time
after the six measurements have been acquired.

At startup, print this header once:
DATA,time_s,tec_C,rod1_C,rod2_C,rod3_C,rod4_C,rod5_C,pwm,heat_cool,setpoint_C,safety

For every acquisition cycle, print exactly one comma-separated line beginning
with DATA and containing those fields in that order. Diagnostic, command-ack,
and error lines must not begin with DATA. Keep accepting the existing Python
commands without changing their format. Comment the new pin definitions,
six-channel acquisition loop, and serial-output block for an Arduino beginner.
After editing, summarize every function and line of control logic that you
preserved unchanged.
```

</details>

Before connecting TEC power, test this sketch with Serial Monitor. Warm one
thermistor at a time with your fingers and verify that only its named column
changes. Confirm that the Arduino starts with PWM zero and still responds to a
zero-power command. Close Serial Monitor before opening the Python GUI because
only one program can own the serial port at a time.

### Stage 2: Extend The Python Display And Raw-Data Record

Modify the Module 6 GUI so that it parses the new `DATA` record and displays
six simultaneous temperature traces. Retain the existing setpoint, controller,
PWM, and safety displays. Give each trace a stable label and color, make the
TEC-base trace visually distinct, and provide checkboxes or a legend that
makes crowded plots readable.

Every accepted record must be written to a new CSV file with at least these
columns:

```text
time_s,tec_C,rod1_C,rod2_C,rod3_C,rod4_C,rod5_C,pwm,heat_cool,setpoint_C,safety
```

These are raw measured temperatures. Do not replace them with calibrated
values. Reject incomplete or malformed lines without stopping the program,
flush saved data regularly, and never silently overwrite an existing run.

<details markdown="1">
<summary>Suggested Copilot prompt: six-temperature GUI and CSV logger</summary>

```text
Inspect both the open Arduino sketch and my working Module 6 PySide6 and
pyqtgraph TEC-control GUI. Modify the existing Python program; do not create a
different controller or change the Arduino command format. Preserve all PI
controls, PWM and direction displays, serial command sending, safety display,
and zero-output stop behavior.

Parse only complete Arduino lines beginning with DATA. The fields are:
time_s, tec_C, rod1_C, rod2_C, rod3_C, rod4_C, rod5_C, pwm, heat_cool,
setpoint_C, and safety. Ignore headers, acknowledgments, diagnostics, and
malformed lines without crashing.

Plot TEC and rod1-rod5 temperatures together against Arduino time. Give every
trace a fixed label and color and make the TEC trace thicker than the rod
traces. Add live numerical displays for all six temperatures. Preserve the
existing rolling-window behavior and controls.

Write every accepted raw record to a new CSV file with exactly those column
names. Do not apply calibration corrections and do not overwrite an existing
file; create a timestamped filename or require a new filename. Flush the file
regularly so a long run is not lost if the GUI closes unexpectedly. Add a
visible count of accepted and rejected serial lines. Keep the code readable
for a Python beginner and comment the parser, data storage, CSV writing, and
plot updates. At the end, explain how I can verify that every plotted trace is
being written to the correct CSV column.
```

</details>

Test with TEC power off. Compare several consecutive Arduino `DATA` records
with the corresponding Python numerical display and CSV rows. The field order,
values, and units must agree before the program is used for calibration.

### Stage 3: Write The Relative-Calibration Analysis

Write a separate Python analysis program for the common-bath calibration. It
must read the raw CSV rather than modify the acquisition program. For each rod
channel, fit

\[
T_{\mathrm{TEC}}=a_i+b_iT_i,
\]

make the comparison and residual plots required below, and save the fitted
coefficients and fit-quality measures in a separate calibration file. Keep the
raw CSV unchanged. Later analyses may read both files and calculate additional
columns named `rod1_corrected_C` through `rod5_corrected_C`.

<details markdown="1">
<summary>Suggested Copilot prompt: relative-calibration analysis</summary>

```text
Write a separate Python calibration-analysis script for my six-thermistor CSV
file. Do not modify or overwrite the raw data. The raw columns are time_s,
tec_C, rod1_C, rod2_C, rod3_C, rod4_C, rod5_C, pwm, heat_cool, setpoint_C, and
safety.

Treat tec_C as the reference. For each rod channel i, perform a linear
least-squares fit tec_C = a_i + b_i * rod_i_C over a user-selected calibration
time or temperature range. Plot each rod temperature against tec_C with the
identity line and fitted line. Then plot the corrected residual
(a_i + b_i * rod_i_C) - tec_C against tec_C.

Print and save a table containing channel, a_i, b_i, number of fitted points,
calibration temperature range, residual mean, residual standard deviation,
and maximum absolute residual. Save this table to a separate CSV file. Also
write a separate corrected-data CSV that retains every original raw column and
adds rod1_corrected_C through rod5_corrected_C. Never replace a raw column.
Include clear axis labels with units and comment the file input, range
selection, fitting, residual calculation, and output sections for a Python
beginner.
```

</details>

### Stage 4: Integration Check Before Calibration

Demonstrate the complete measurement chain before collecting the cooling-bath
record:

1. Show that warming one sensor changes only its assigned Arduino and Python
   channel.
2. Verify that one Arduino `DATA` line, one set of displayed values, and one
   saved CSV row agree.
3. Disconnect one rod thermistor temporarily and verify that the fault is
   visible without defeating the TEC-base safety shutdown.
4. Restart both programs and confirm that PWM begins at zero and that a new
   data file is created.
5. Record the Arduino sketch, Python GUI, and calibration-script filenames and
   their Git commit hash in the sensor map.

## Part 1: Sensor Map And Calibration

1. Record the rod material as 6061-T6 aluminum. Measure its diameter \(d\),
   overall physical length, and analysis length \(L\) from the first thermistor
   hole to the tip. Calculate its cross-sectional area \(A\) and perimeter
   \(P\) in SI units.
2. Assign permanent names to the TEC-base thermistor and the five rod
   thermistors, and record the corresponding Arduino channels `A0` through
   `A5`.
3. Hold all sensors at the same temperature and record at least 60
   seconds of data.
4. Plot channel differences. Decide whether offsets require correction.
5. After calibration, install rod thermistor 1 in the first rod hole and define
   that hole as the analysis base \(x=0\). Measure the other four rod-sensor
   positions and the tip relative to this origin, so that the tip is at (x=L).
   Estimate the uncertainty of every position and of \(L\).
6. Save a diagram or photograph showing the permanent sensor labels, Arduino
   channel assignments, coordinate direction, and measured rod positions.

### Relative Thermistor Cross-Calibration

The rod experiment measures temperature differences and spatial temperature
gradients. It does not require an absolute temperature calibration. It does
require all thermistor channels to give the same reading when they experience
the same temperature; otherwise, channel-to-channel offsets could be mistaken
for a temperature gradient along the rod.

Use the TEC thermistor as the reference channel and cross-calibrate the rod
thermistors as follows:

**Step 1. Arrange the sensors.** Complete this cross-calibration before the
thermistors are permanently installed in the TEC base and rod. All six sensing
ends must remain accessible; do not immerse the assembled TEC, heater, or
electrical hardware. If you don't have enough prepared thermistors, solder
wires to the thermistors and insulate each joint with heat shrink. The hardware
page shows how the finished sensor should look.

Label the thermistor intended for the TEC base `TEC` and label the others 1-5.
The labels must remain attached for the rest of the semester. Place all six
thermistor sensing ends close together in a Styrofoam cup of warm water over the
approximate range \(20^{\circ}\mathrm{C}<T<60^{\circ}\mathrm{C}\). Immerse
only waterproof sensing ends and keep electrical joints dry. Do not allow the
sensors to touch the cup walls or bottom.

**Step 2. Use the experimental measurement chain.** Make sure the corresponding Arduino circuit and thermistor are always used together. Use the same voltage
dividers, Arduino inputs, acquisition code, and sample rate that will be used
for the rod experiment.

**Step 3. Keep the bath uniform.** Stir the water gently and continuously so
that all sensors experience the same temperature.

**Step 4. Record the common cooling history.** Record every channel
simultaneously while the water cools slowly through the temperature range
expected in the rod experiment.

**Step 5. Fit each channel to the reference.** Plot each rod-sensor reading,
$T_i$, against the simultaneous TEC-thermistor reading, $T_{\mathrm{TEC}}$. Do the data fall on a straight line? If so,
 fit

\[
T_{\mathrm{TEC}}=a_i+b_iT_i.
\]

Apply this fitted relation as the correction:

\[
T_{i,\mathrm{corrected}}=a_i+b_iT_i.
\]

**Step 6. Check the corrected differences.** Plot

\[
\Delta T_i
=T_{i,\mathrm{corrected}}-T_{\mathrm{TEC}}
\]

against $T_{\mathrm{TEC}}$. Report the mean difference, scatter, and any
remaining trend with temperature. Choose and record an acceptance criterion
before evaluating the correction. A useful starting criterion is a corrected
mean difference smaller than $0.2^{\circ}\mathrm{C}$ for every channel, with
no residual trend larger than $0.2^{\circ}\mathrm{C}$ across the calibration
range. Revise this criterion if the measured noise and resolution justify a
different value.

**Step 7. Preserve the raw readings.** Store the correction coefficients
separately and apply them during analysis; never overwrite the original data.

No independent reference thermometer is required for this relative
cross-calibration. The corrected channels may share a common absolute bias,
but that bias does not affect temperature differences or the measured spatial
profile.

## Part 2: Choose Sensor Positions, Then Measure The Step Response

1. Install rod thermistor 1 in the first rod hole and use that hole as the
   analysis base \(x=0\). It is neither the physical rod end nor the separate
   thermistor embedded in the TEC. Its measured signal \(T(0,t)\) is the
   boundary condition for the rod model.
2. For a steady placement pilot, begin with the TEC set to
   \(45^{\circ}\mathrm{C}\). A lower temperature generally reaches steady state
   faster but may produce temperature differences that are too small to resolve.
   A higher temperature improves the spatial signal but increases equilibration
   time and heat loss. If you change the pilot temperature, use the lowest
   setpoint that gives a clear profile and **never exceed
   \(55^{\circ}\mathrm{C}\)**.
3. Move the other four thermistors among the available fixed holes and measure
   the resulting steady temperatures. No advance calculation of the positions
   is required. Choose locations for which the steady excess temperature drops
   by at least a factor of \(e\) from rod thermistor 1 to the farthest retained
   sensor:

    \[
    0<\theta_5(x_5,\infty)
    \leq\frac{\theta_1(0,\infty)}{e}.
    \]

    Plot the pilot values as \(\ln\theta\) versus \(x\) while selecting the
    holes. The retained points should be spread across the semilog plot rather
    than clustered near one end. Do not retain a position whose excess
    temperature is indistinguishable from noise or room drift.

4. Once you have identified useful locations, leave the thermistors in those
   holes. Measure and record every selected position and its uncertainty.
5. Set the TEC to \(20^{\circ}\mathrm{C}\) and allow the entire rod to
   equilibrate. Record room temperature and all six thermistor channels. Verify
   that the rod channels agree within the calibration criterion.
6. Apply a non-oscillatory TEC step from \(20^{\circ}\mathrm{C}\) to
   \(45^{\circ}\mathrm{C}\) using PI control. Record continuously until the
   stationary-profile criterion below is satisfied.
7. Plot all temperatures against the same time axis and explain why farther
   sensors respond later and with smaller excursions.
8. Save the commanded TEC temperature, measured TEC temperature, and measured
   rod temperature \(T(0,t)\). The rod thermistor at \(x=0\), rather than the
   TEC command or TEC thermistor, supplies the model boundary condition.

## C5 Checkoff

At S17, demonstrate:

- calibrated or cross-checked rod thermistors,
- documented sensor coordinates and wiring,
- synchronized multichannel logging,
- baseline and initial step-response data,
- files containing timestamps, units, channel labels, and experimental notes,
- individual understanding of the measurement chain and one dominant
  uncertainty.

## Part 3: Stationary-Fin Profile

1. Before the run, record the predicted profile and select a numerical
   steady-state criterion. A useful starting criterion is
   $|dT_i/dt|<0.02^{\circ}\mathrm{C}/\mathrm{min}$ at every sensor for at
   least 10 minutes; justify any different criterion.
2. Use the final steady portion of the \(20^{\circ}\mathrm{C}\) to
   \(45^{\circ}\mathrm{C}\) step-response run. No separate heating run is
   required. Confirm that the steady-state criterion is satisfied.
3. Average each sensor over a justified final interval. Five minutes is a
   reasonable starting interval after the steady-state criterion has been met.
4. Plot $\theta$ versus $x$ with error bars.
5. Fit both the exact finite-length model and the semi-infinite exponential.
6. Plot both sets of residuals and report $m$ in inverse meters with uncertainty.
7. Calculate the characteristic decay length $1/m$ in meters.
8. Report how much the fitted $m$ changes when the finite end is ignored and
   compare that shift with the fit uncertainty.
9. Discuss sensor-position error, room-temperature drift, imperfect contact,
   and the measured evidence for the tip boundary condition.
10. Compare the measured profile and residuals with the prediction record.
    State which assumptions are supported, which model is more adequate, and
    what discrepancy remains unexplained.

## Stationary-Fin Analysis Record

### Evidence To Save During S16-S17

Keep the sensor map, calibration record, geometry, raw baseline, synchronized
step response, commanded and measured TEC temperature, measured rod-base
temperature, steady profile, run
metadata, and exact acquisition code as each item is produced. Use
`docs/module_notes/module_07_rod_instrument.md`, `data/module_07/`, and
`docs/figures/module_07/`. Never overwrite raw rod data with corrected data.

### A4 Submission And Rubric

- **Type:** individual, 10 points
- **Due:** Wednesday, October 28, at **9:05 AM**
- **Moodle file:** `A4_Lastname.pdf`
- **Repository file:** `docs/assessments/a4_finite_length_biot.md`

The four required parts are listed in
[A4: Finite-Rod Model And Validity Checks](#a4-finite-rod-model-and-validity-checks).
Submit all four parts in the single PDF and repository file named above. Put
your name, assignment code, date, repository URL, and the exact Git commit hash
on the first page.

### C5: Rod Instrument And Data-Acquisition Chain

Demonstrate C5 during S17 on Wednesday, October 28. The `C5 Team Checkoff`
Moodle receipt is due by **11:55 AM** and must cite the pushed acquisition-code
and evidence commit.
Prepare the [C5 oral questions](../../assessment.md#c5-rod-instrument-and-data-acquisition-chain).

### Formative Stationary-Fin Analysis

There is no separate Moodle paper for this step. Keep the team note at
`docs/module_notes/module_07_stationary_fin.md` and authoritative analysis code
under `python/analysis/`. The result becomes evidence for C6 and the
final presentation.

Submit one reproducible analysis containing:

- the dimensional governing equation and assumptions,
- the sensor map and calibration result,
- baseline and step-response plots,
- steady $\theta(x)$ data, finite and semi-infinite fits, and both residual sets,
- fitted $m$ and $1/m$ with units and uncertainty,
- the sensor-by-sensor finite-length error and transverse Biot-number check,
- a short explanation of why this result alone cannot separate `k` from `h`.

### A4 Rubric

| Criterion | Points |
| --- | ---: |
| Part 1 correctly applies Fourier's law, units, and physical judgment to Problem 1.3 | 1 |
| Part 2 derives the stationary rod equation and finite insulated-tip solution from the stated laws and boundary conditions | 3 |
| Part 3 obtains the semi-infinite limit and correctly evaluates the tip approximation and sensor-by-sensor finite-length errors | 3 |
| Part 4 correctly calculates the transverse Biot number, gives a separate radius conclusion, and distinguishes convection from radiation | 2 |
| The individual submission is complete, dimensionally checked, clearly organized, and cites the exact Git checkpoint | 1 |

The instructor will give feedback on the stationary-fin record during the rod
work. It is judged by whether the data, both fits, residuals, dimensional
parameters, uncertainty, and interpretation are ready to reuse in C6.
