# Labs And Course Calendar

Use this page to answer two different questions:

- **What are we doing today?** Use the meeting calendar.
- **Where is the full lab handout?** Use the lab modules.

The course meets Mondays and Wednesdays from **9:05 AM to 11:55 AM**. Some lab
modules span several meetings, especially the heat-transport work near the end
of the semester.

!!! note
    This is the complete Fall 2026 course draft. The objectives, graded due
    dates, and completion milestones are fixed planning targets; the instructor
    may revise details after hardware testing or announce a change in class.

## Lab Modules

| Module | Focus | Lab Pages |
| --- | --- | --- |
| Module 1 | Arduino, signals, oscilloscope, analog input, averaging, and PWM | [Lab 1: First Contact](lab-01/index.md) |
| Module 2 | Thermistor temperature measurement, Arduino Serial Plotter output, and H-bridge signal checks with actuator power off | [Lab 2: First Real Instrument Pieces](lab-02/index.md) |
| Module 3 | Connect the TEC and thermal switch using prepared high-current wiring; then begin manual controls and first GUI edits | [Lab 3: Manual TEC Heat/Cool And First Python GUI](lab-03/index.md) |
| Module 4 | Open-loop TEC calibration and software safety | [Lab 4: Open-Loop TEC Calibration And Software Safety](lab-04/index.md) |
| Module 5 | P-only feedback control: droop, gain, and instability | [Lab 5: P-Only Temperature Control](lab-05/index.md) |
| Module 6 | Time-domain modeling of P and PI temperature control | [Lab 6: Modeling P And PI Temperature Control](lab-06/index.md) |
| Module 7 | TEC process modeling: droop, lag, overshoot, and simulation | [Lab 7: Process Model And Python Simulation](lab-07/index.md) |
| Theory Bridge | Fourier's Law, heat equation, dimensional analysis, and Biot number | [Theory Bridge: Fourier's Law, Heat Equation, And Biot Number](theory-bridge-chapter-1/index.md) |
| Fin Theory | Fin geometry, transverse Biot number, and the complete finite-to-infinite derivation | [Fin Design: From A Finite Rod To An Infinite Rod](fin-design-derivation/index.md) |
| Module 8 | Multichannel rod instrument, step response, heat equation, and stationary-fin model | [Lab 8: Rod Instrument, Step Response, And Stationary Fin](lab-08/index.md) |
| Module 9 | Periodic boundary control, amplitude decay, phase lag, and Angstrom parameter inference | [Lab 9: The Angstrom Method](lab-09/index.md) |
| Module 10 | Aluminum conductivity, side heat loss, uncertainty, reproducibility, and final presentation | [Lab 10: Aluminum Conductivity, Side Heat Loss, And Final Synthesis](lab-10/index.md) |

## Graded Completion Milestones

Six completion milestones establish deadlines for the major instrumentation,
hardware, and software capabilities. Meeting each deadline is part of the **Lab
notes, checkoffs, and short assignments** grade. A milestone is complete when
the team can demonstrate a safely functioning system, show current code and
documentation in its repository, and have each student explain the work.

| Milestone | Due | Completion standard |
| --- | --- | --- |
| [**C1. Development environment and repository ready**](../assessment.md#c1-development-environment-and-repository) | Meeting 3, Wed. Sept. 2 | Arduino IDE, GitHub Desktop, and VS Code are working; the course repository is organized; an Arduino sketch runs; and a meaningful commit has been pushed. |
| [**C2. Measurement and actuator electronics complete**](../assessment.md#c2-measurement-and-actuator-electronics) | Meeting 5, Mon. Sept. 14 | The thermistor reports a plausible calibrated temperature; the H-bridge PWM and direction inputs have been verified with the oscilloscope; and the prepared actuator wiring is complete. |
| [**C3. TEC instrument and first Python GUI complete**](../assessment.md#c3-tec-instrument-and-first-python-gui) | Meeting 7, Wed. Sept. 23 | The TEC and thermal switch are wired safely; manual heat/cool and PWM work; Python displays and saves the serial data; and an open-loop temperature record has been made. |
| [**C4. Feedback controller and TEC process model complete**](../assessment.md#c4-feedback-controller-and-tec-process-model) | Meeting 15, Wed. Oct. 21 | P and PI control run safely; droop and oscillation data have been collected; the process model runs; and at least one model trace has been compared with experiment. |
| [**C5. Rod instrument and data-acquisition chain complete**](../assessment.md#c5-rod-instrument-and-data-acquisition-chain) | Meeting 18, Mon. Nov. 2 | Rod thermistors are calibrated; sensor positions and wiring are documented; multichannel logging works; and baseline plus initial step-response data have been saved. |
| [**C6. Final thermal-transport package complete**](../assessment.md#c6-final-thermal-transport-package) | Meeting 25, Mon. Nov. 30 | Periodic rod data and reproducible analysis report `q`, `q_prime`, diffusivity `kappa`, aluminum conductivity `k`, loss rate `nu`, and side heat-transfer coefficient `H`, with units and uncertainty. |

For every milestone, late work must still be completed. Timely completion is
one part of the milestone score because later experiments depend on the system
being ready.

See [Assessment And Milestones](../assessment.md) for exactly what is due, the
rubrics for each `A#`, `C#`, and `F1`, the scheduled `P#` progress checks, and
the mapping from assessments to Course Goals.

## Semester At A Glance

`M#` identifies the class meeting. `A#` identifies a graded assignment, `C#`
identifies a graded completion milestone, `P#` identifies an ungraded progress
check, and `F1` identifies the final presentation and oral defense. `Prep`
means required preparation with no separate grade.

### August 2026

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | --- | --- | --- | --- | --- | --- |
| 24 | 25 | **26**<br>[M1](#meeting-1) | 27 | 28 | 29 | 30 |
| **31**<br>[M2](#meeting-2)<br>**Prep** |  |  |  |  |  |  |

### September 2026

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | --- | --- | --- | --- | --- | --- |
| 31 Aug<br>[M2](#meeting-2)<br>**Prep** | 1 | **2**<br>[M3](#meeting-3)<br>**C1 due**<br>**A1 due** | 3 | 4 | 5 | 6 |
| **7**<br>No class | 8 | **9**<br>[M4](#meeting-4) | 10 | 11 | 12 | 13 |
| **14**<br>[M5](#meeting-5)<br>**C2 due** | 15 | **16**<br>[M6](#meeting-6)<br>**P1** | 17 | 18 | 19 | 20 |
| **21**<br>No class | 22 | **23**<br>[M7](#meeting-7)<br>**C3 due** | 24 | 25 | 26 | 27 |
| **28**<br>[M8](#meeting-8)<br>**A2 due** | 29 | **30**<br>[M9](#meeting-9)<br>**Prep** |  |  |  |  |

### October 2026

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | --- | --- | --- | --- | --- | --- |
| 28 Sep<br>[M8](#meeting-8) | 29 Sep | 30 Sep<br>[M9](#meeting-9) | 1 | 2 | 3 | 4 |
| **5**<br>[M10](#meeting-10)<br>**A3 due** | 6 | **7**<br>[M11](#meeting-11)<br>**A4 due** | 8 | 9 | 10 | 11 |
| **12**<br>No class | **13**<br>[M12](#meeting-12)<br>Brandeis Monday<br>**Prep** | **14**<br>[M13](#meeting-13)<br>**A5 due** | 15 | 16 | 17 | 18 |
| **19**<br>[M14](#meeting-14)<br>**P2** | 20 | **21**<br>[M15](#meeting-15)<br>**C4 due**<br>**A6 due** | 22 | 23 | 24 | 25 |
| **26**<br>[M16](#meeting-16)<br>**Prep** | 27 | **28**<br>[M17](#meeting-17)<br>**A7 due** | 29 | 30 | 31 |  |

### November 2026

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | --- | --- | --- | --- | --- | --- |
| **2**<br>[M18](#meeting-18)<br>**C5 due** | 3 | **4**<br>[M19](#meeting-19)<br>**A8 due** | 5 | 6 | 7 | 8 |
| **9**<br>[M20](#meeting-20)<br>**P3** | 10 | **11**<br>[M21](#meeting-21)<br>**A9 due** | 12 | 13 | 14 | 15 |
| **16**<br>[M22](#meeting-22)<br>**P4** | 17 | **18**<br>[M23](#meeting-23)<br>**A10 due** | 19 | 20 | 21 | 22 |
| **23**<br>[M24](#meeting-24)<br>**A11 due** | 24 | **25**<br>No class | 26 | 27 | 28 | 29 |
| **30**<br>[M25](#meeting-25)<br>**C6 due** |  |  |  |  |  |  |

### December 2026

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | --- | --- | --- | --- | --- | --- |
| 30 Nov<br>[M25](#meeting-25) | 1 | **2**<br>[M26](#meeting-26)<br>**F1 due** | 3 | 4 | 5 | 6 |

## Meeting Calendar

| Meeting | Date | Day | By the end of this meeting, students can... | Lab/Assignment | Due | Goals |
| --- | --- | --- | --- | --- | --- | --- |
| <span id="meeting-1">1</span> | 2026-08-26 | Wed | Upload and modify an Arduino sketch; identify the instrument and safety boundaries; create and commit to the course repository. | [GitHub Desktop, GitHub, VS Code, And AI](../git-vscode-ai-workflow.md) | `Prep`: setup completed in class | G1, G5, G12 |
| <span id="meeting-2">2</span> | 2026-08-31 | Mon | Relate digital output, ADC input, averaging, PWM, and oscilloscope traces to physical voltage and time. | [Lab 1: First Contact](lab-01/index.md) | `Prep`: Arduino examples | G1, G2, G5 |
| <span id="meeting-3">3</span> | 2026-09-02 | Wed | Build a thermistor divider; convert ADC readings to resistance and temperature; state calibration assumptions. | [Lab 2: First Real Instrument Pieces](lab-02/index.md) | [**C1**](../assessment.md#c1-development-environment-and-repository); `A1` | G1-G4, G12, G14 |
| <span id="meeting-4">4</span> | 2026-09-09 | Wed | Predict and verify H-bridge PWM and direction waveforms before applying TEC power. | [Lab 2](lab-02/index.md) | `Prep`: H-bridge prediction table | G1, G2, G5, G6 |
| <span id="meeting-5">5</span> | 2026-09-14 | Mon | Produce safe low-power TEC heating and cooling; distinguish measurement, actuation, and feedback. | [Lab 3: Manual TEC Heat/Cool And First Python GUI](lab-03/index.md) | [**C2**](../assessment.md#c2-measurement-and-actuator-electronics) | G1, G3-G6 |
| <span id="meeting-6">6</span> | 2026-09-16 | Wed | Parse real serial data; display and save temperature and PWM; set update interval, window, and axes. | [Lab 3](lab-03/index.md) | `P1` | G2, G7, G12 |
| <span id="meeting-7">7</span> | 2026-09-23 | Wed | Command heat/cool and PWM from Python; test software and hardware limits; save open-loop records. | [Lab 3](lab-03/index.md) and [Lab 4](lab-04/index.md) | [**C3**](../assessment.md#c3-tec-instrument-and-first-python-gui) | G3, G6, G7, G12, G14 |
| <span id="meeting-8">8</span> | 2026-09-28 | Mon | Measure steady temperature versus signed PWM and identify asymmetry, limits, and a steady-state criterion. | [Lab 4: Open-Loop TEC Calibration And Software Safety](lab-04/index.md) | `A2` | G2, G3, G6, G7, G9 |
| <span id="meeting-9">9</span> | 2026-09-30 | Wed | Implement P control and explain why nonzero actuator power produces droop. | [Lab 5: P-Only Temperature Control](lab-05/index.md) | `Prep`: P-control prediction | G7-G10 |
| <span id="meeting-10">10</span> | 2026-10-05 | Mon | Measure droop versus gain and characterize oscillation amplitude and frequency near instability. | [Lab 5](lab-05/index.md) | `A3` | G3, G8, G9, G14 |
| <span id="meeting-11">11</span> | 2026-10-07 | Wed | Derive and fit a one-lump energy balance; interpret heat capacity, conductance, and time constant dimensionally. | [Lab 6: Modeling P And PI Temperature Control](lab-06/index.md) | `A4` | G9, G10, G13 |
| <span id="meeting-12">12</span> | 2026-10-13 | Tue | Explain how integral action removes droop; implement anti-windup; compare P and PI responses. | [Lab 6](lab-06/index.md) | `Prep`: PI-control preparation | G8-G10, G13 |
| <span id="meeting-13">13</span> | 2026-10-14 | Wed | Use a two-lump model to explain thermal lag, overshoot, and gain-dependent oscillation. | [Lab 6](lab-06/index.md) | `A5` | G9, G10, G13, G14 |
| <span id="meeting-14">14</span> | 2026-10-19 | Mon | Fit one- and two-lump models and judge whether added complexity is supported by residuals. | [Lab 7: Process Model And Python Simulation](lab-07/index.md) | `P2` | G3, G7, G10, G12-G14 |
| <span id="meeting-15">15</span> | 2026-10-21 | Wed | Defend the TEC controller and model; explain why a rod requires `T(x,t)` rather than a lumped temperature. | [Lab 7](lab-07/index.md) | [**C4**](../assessment.md#c4-feedback-controller-and-tec-process-model); `A6` | G8-G14 |
| <span id="meeting-16">16</span> | 2026-10-26 | Mon | Lecture: solve the finite-length one-dimensional rod, obtain the semi-infinite limit, and introduce the transverse Biot number. | [Theory Bridge](theory-bridge-chapter-1/index.md) and [Lab 8](lab-08/index.md) | `Prep`: Lienhard Chapter 1 and Section 4.5 | G11, G13, G14 |
| <span id="meeting-17">17</span> | 2026-10-28 | Wed | Quantify finite-length error and transverse Biot number; calibrate and map rod thermistors for `T(x,t)`. | [Lab 8: Rod Instrument, Step Response, And Stationary Fin](lab-08/index.md) | `A7` | G2-G4, G11-G14 |
| <span id="meeting-18">18</span> | 2026-11-02 | Mon | Acquire baseline and step-response data; lecture on the axisymmetric radial model while the experiment runs. | [Lab 8](lab-08/index.md) | [**C5**](../assessment.md#c5-rod-instrument-and-data-acquisition-chain) | G3, G7, G9, G11-G13 |
| <span id="meeting-19">19</span> | 2026-11-04 | Wed | Fit finite-length and semi-infinite stationary profiles; compare residuals and approximation error. | [Lab 8](lab-08/index.md) | `A8` | G3, G11, G13-G15 |
| <span id="meeting-20">20</span> | 2026-11-09 | Mon | Complete the guided radial-model study, then tune a sinusoidal base boundary and collect an Angstrom pilot run. | [Lab 9: The Angstrom Method](lab-09/index.md) | `P3` | G6-G9, G11-G13 |
| <span id="meeting-21">21</span> | 2026-11-11 | Wed | Fit sensor mean, amplitude, and phase; explain exponential amplitude decay and linear phase lag. | [Lab 9](lab-09/index.md) | `A9` | G3, G7, G11, G13-G15 |
| <span id="meeting-22">22</span> | 2026-11-16 | Mon | Acquire at least five settled periods and document whether the measured boundary and rod data are usable. | [Lab 9](lab-09/index.md) | `P4` | G2, G3, G7, G11, G12 |
| <span id="meeting-23">23</span> | 2026-11-18 | Wed | Determine spatial amplitude and phase coefficients and infer diffusivity `kappa` and loss rate `nu`. | [Lab 9](lab-09/index.md) | `A10` | G3, G7, G11-G15 |
| <span id="meeting-24">24</span> | 2026-11-23 | Mon | Calculate aluminum `k` and side-loss `H`; update finite-length and transverse-Biot checks using measured parameters. | [Lab 10: Aluminum Conductivity, Side Heat Loss, And Final Synthesis](lab-10/index.md) | `A11` | G3, G11, G13-G15 |
| <span id="meeting-25">25</span> | 2026-11-30 | Mon | Compare measured and modeled `T(x,t)`; defend finite-length and finite-radius validity checks; reproduce final results. | [Lab 10](lab-10/index.md) | [**C6**](../assessment.md#c6-final-thermal-transport-package) | G3, G7, G11-G15 |
| <span id="meeting-26">26</span> | 2026-12-02 | Wed | Present the instrument-to-model chain and individually defend hardware, software, control, and thermal-physics decisions. | [Lab 10](lab-10/index.md) | `F1` | G1-G15 |

## Calendar Notes

- No class is scheduled on Monday, September 7; Monday, September 21; Monday,
  October 12; or Wednesday, November 25.
- Tuesday, October 13 is included as a Brandeis Monday make-up meeting.
- The TEC-only sequence is planned to finish by Meeting 15 so the second half of
  the course can focus on thermal transport in the long metal cylinder.
