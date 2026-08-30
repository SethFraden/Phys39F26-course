# Modules And Course Calendar

Use this page to answer two different questions:

- **What are we doing today?** Use the session calendar.
- **Where is the full module handout?** Use the course modules.

The course meets Mondays and Wednesdays from **9:05 AM to 11:55 AM**. Some
modules span several sessions, especially the heat-transport work near the end
of the semester.

!!! note
    This is the complete Fall 2026 course draft. The objectives, graded due
    dates, and completion milestones are fixed planning targets; the instructor
    may revise details after hardware testing or announce a change in class.

## Assessment And Milestones

Consult [**Assessment And Milestones**](../assessment.md) early and throughout
the semester. It explains what must be submitted or demonstrated, when work is
due, how each assignment and milestone will be graded, and what to expect during
oral checks. The calendar below shows the corresponding `A#`, `C#`, `P#`, and
`F1` dates.

## Course Modules

| Module | Focus | Module Pages |
| --- | --- | --- |
| Module 1 | Arduino, signals, oscilloscope, analog input, averaging, and PWM | [Module 1: First Contact](lab-01/index.md) |
| Module 2 | Thermistor temperature measurement, Arduino Serial Plotter output, and H-bridge signal checks with actuator power off | [Module 2: First Real Instrument Pieces](lab-02/index.md) |
| Module 3 | Connect the TEC and thermal switch using prepared high-current wiring; then begin manual controls and first GUI edits | [Module 3: Manual TEC Heat/Cool And First Python GUI](lab-03/index.md) |
| Module 4 | Open-loop TEC calibration and software safety | [Module 4: Open-Loop TEC Calibration And Software Safety](lab-04/index.md) |
| Module 5 | P-only feedback control: droop, gain, and instability | [Module 5: P-Only Temperature Control](lab-05/index.md) |
| Module 6 | Time-domain modeling of P and PI temperature control | [Module 6: Modeling P And PI Temperature Control](lab-06/index.md) |
| Module 7 | TEC process modeling: droop, lag, overshoot, and simulation | [Module 7: Process Model And Python Simulation](lab-07/index.md) |
| Theory Bridge | Fourier's Law, heat equation, dimensional analysis, and Biot number | [Theory Bridge: Fourier's Law, Heat Equation, And Biot Number](theory-bridge-chapter-1/index.md) |
| Fin Theory | Fin geometry, transverse Biot number, and the complete finite-to-infinite derivation | [Fin Design: From A Finite Rod To An Infinite Rod](fin-design-derivation/index.md) |
| Module 8 | Multichannel rod instrument, step response, heat equation, and stationary-fin model | [Module 8: Rod Instrument, Step Response, And Stationary Fin](lab-08/index.md) |
| Module 9 | Periodic boundary control, amplitude decay, phase lag, and Angstrom parameter inference | [Module 9: The Angstrom Method](lab-09/index.md) |
| Module 10 | Aluminum conductivity, side heat loss, uncertainty, reproducibility, and final presentation | [Module 10: Aluminum Conductivity, Side Heat Loss, And Final Synthesis](lab-10/index.md) |

## Graded Completion Milestones

Six completion milestones establish deadlines for the major instrumentation,
hardware, and software capabilities. Completing each milestone by its deadline
is part of the **Module notes, checkoffs, and short assignments** grade. A milestone is complete when
the team can demonstrate a safely functioning system, show current code and
documentation in its repository, and have each student explain the work.

| Milestone | Due | Completion standard |
| --- | --- | --- |
| [**C1. Development environment and repository ready**](../assessment.md#c1-development-environment-and-repository) | Demonstration during S3, Wed. Sept. 2; receipt by 11:55 AM | Arduino IDE, GitHub Desktop, and VS Code are working; the course repository is organized; an Arduino sketch runs; and a meaningful commit has been pushed. |
| [**C2. Measurement and actuator electronics complete**](../assessment.md#c2-measurement-and-actuator-electronics) | Demonstration during S5, Mon. Sept. 14; receipt by 11:55 AM | The thermistor reports a plausible calibrated temperature; the H-bridge PWM and direction inputs have been verified with the oscilloscope; and the prepared actuator wiring is complete. |
| [**C3. TEC instrument and first Python GUI complete**](../assessment.md#c3-tec-instrument-and-first-python-gui) | Demonstration during S7, Wed. Sept. 23; receipt by 11:55 AM | The TEC and thermal switch are wired safely; manual heat/cool and PWM work; Python displays and saves the serial data; and an open-loop temperature record has been made. |
| [**C4. Feedback controller and TEC process model complete**](../assessment.md#c4-feedback-controller-and-tec-process-model) | Demonstration during S15, Wed. Oct. 21; receipt by 11:55 AM | P and PI control run safely; droop and oscillation data have been collected; the process model runs; and at least one model trace has been compared with experiment. |
| [**C5. Rod instrument and data-acquisition chain complete**](../assessment.md#c5-rod-instrument-and-data-acquisition-chain) | Demonstration during S18, Mon. Nov. 2; receipt by 11:55 AM | Rod thermistors are calibrated; sensor positions and wiring are documented; multichannel logging works; and baseline plus initial step-response data have been saved. |
| [**C6. Final thermal-transport package complete**](../assessment.md#c6-final-thermal-transport-package) | Demonstration during S25, Mon. Nov. 30; receipt by 11:55 AM | Periodic rod data and reproducible analysis report `q`, `q_prime`, diffusivity `kappa`, aluminum conductivity `k`, loss rate `nu`, and side heat-transfer coefficient `H`, with units and uncertainty. |

For every milestone, late work must still be completed. Timely completion is
one part of the milestone score because later experiments depend on the system
being ready.

See [Assessment And Milestones](../assessment.md) for exactly what is due, the
rubrics for each `A#`, `C#`, and `F1`, the scheduled `P#` progress checks, and
the mapping from assessments to Course Goals.

## Semester At A Glance

`S#` identifies a class session. `A#` identifies a graded assignment, `C#`
identifies a graded completion milestone, `P#` identifies an ungraded progress
check, and `F1` identifies the final presentation and oral defense. `Prep`
means required preparation with no separate grade.

### August 2026

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | --- | --- | --- | --- | --- | --- |
| 24 | 25 | **26**<br>[S1](#session-1)<br>[Module 1](lab-01/index.md) | 27 | 28 | 29 | 30 |
| **31**<br>[S2](#session-2)<br>[Module 1](lab-01/index.md)<br>Collect A1 evidence |  |  |  |  |  |  |

### September 2026

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | --- | --- | --- | --- | --- | --- |
| 31 Aug<br>[S2](#session-2)<br>[Module 1](lab-01/index.md)<br>Collect A1 evidence | 1 | **2**<br>[S3](#session-3)<br>[Module 2](lab-02/index.md)<br>[**C1 checkoff**](../assessment.md#c1-development-environment-and-repository) | 3 | 4 | 5 | 6 |
| **7**<br>No class<br>[**A1 due 5:00 PM**](lab-01/index.md#a1-module-1-evidence-note) | 8 | **9**<br>[S4](#session-4)<br>[Module 2](lab-02/index.md) | 10 | 11 | 12 | 13 |
| **14**<br>[S5](#session-5)<br>[Module 3](lab-03/index.md)<br>**C2 checkoff** | 15 | **16**<br>[S6](#session-6)<br>[Module 3](lab-03/index.md)<br>**P1** | 17 | 18 | 19 | 20 |
| **21**<br>No class | 22 | **23**<br>[S7](#session-7)<br>[Module 3](lab-03/index.md) / [Module 4](lab-04/index.md)<br>**C3 checkoff** | 24 | 25 | 26 | 27 |
| **28**<br>[S8](#session-8)<br>[Module 4](lab-04/index.md)<br>**A2 due** | 29 | **30**<br>[S9](#session-9)<br>[Module 5](lab-05/index.md)<br>**Prep** |  |  |  |  |

### October 2026

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | --- | --- | --- | --- | --- | --- |
| 28 Sep<br>[S8](#session-8)<br>[Module 4](lab-04/index.md) | 29 Sep | 30 Sep<br>[S9](#session-9)<br>[Module 5](lab-05/index.md) | 1 | 2 | 3 | 4 |
| **5**<br>[S10](#session-10)<br>[Module 5](lab-05/index.md)<br>P-control record | 6 | **7**<br>[S11](#session-11)<br>[Module 6](lab-06/index.md)<br>Guided derivation | 8 | 9 | 10 | 11 |
| **12**<br>No class | **13**<br>[S12](#session-12)<br>[Module 6](lab-06/index.md)<br>Brandeis Monday<br>**Prep** | **14**<br>[S13](#session-13)<br>[Module 6](lab-06/index.md)<br>**A3 due** | 15 | 16 | 17 | 18 |
| **19**<br>[S14](#session-14)<br>[Module 7](lab-07/index.md)<br>**P2** | 20 | **21**<br>[S15](#session-15)<br>[Module 7](lab-07/index.md)<br>**C4 checkoff** | 22 | 23 | 24 | 25 |
| **26**<br>[S16](#session-16)<br>[Theory Bridge](theory-bridge-chapter-1/index.md) / [Module 8](lab-08/index.md)<br>**Prep** | 27 | **28**<br>[S17](#session-17)<br>[Module 8](lab-08/index.md)<br>**A4 due** | 29 | 30 | 31 |  |

### November 2026

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | --- | --- | --- | --- | --- | --- |
| **2**<br>[S18](#session-18)<br>[Module 8](lab-08/index.md)<br>**C5 checkoff** | 3 | **4**<br>[S19](#session-19)<br>[Module 8](lab-08/index.md)<br>Stationary analysis | 5 | 6 | 7 | 8 |
| **9**<br>[S20](#session-20)<br>[Module 9](lab-09/index.md)<br>**P3** | 10 | **11**<br>[S21](#session-21)<br>[Module 9](lab-09/index.md)<br>**A5 due** | 12 | 13 | 14 | 15 |
| **16**<br>[S22](#session-22)<br>[Module 9](lab-09/index.md)<br>**P4** | 17 | **18**<br>[S23](#session-23)<br>[Module 9](lab-09/index.md)<br>Modeling-app check | 19 | 20 | 21 | 22 |
| **23**<br>[S24](#session-24)<br>[Module 10](lab-10/index.md)<br>A5 draft | 24 | **25**<br>No class | 26 | 27 | 28 | 29 |
| **30**<br>[S25](#session-25)<br>[Module 10](lab-10/index.md)<br>**C6 checkoff** |  |  |  |  |  |  |

### December 2026

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | --- | --- | --- | --- | --- | --- |
| 30 Nov<br>[S25](#session-25)<br>[Module 10](lab-10/index.md) | 1 | **2**<br>[S26](#session-26)<br>[Module 10](lab-10/index.md)<br>**F1 due** | 3 | 4 | 5 | 6 |

## Outside-Class Workload At A Glance

The figures below include reading the module assignment, theory reading and
comprehension, preparation, analysis or coding, and submission work. See each
module for the itemized budget. Four hours is the maximum, not the expected
time for every session.

| Sessions | Planned outside-class time per session |
| --- | --- |
| S1, S2, S3, S4 | 1 h 30 min; 1 h 45 min; 2 h 30 min; 2 h |
| S5, S6, S7, S8 | 2 h; 2 h 30 min; 3 h; 3 h 15 min |
| S9, S10, S11, S12 | 3 h 15 min; 2 h 45 min; 3 h 30 min; 2 h 45 min |
| S13, S14, S15, S16 | 3 h 30 min; 3 h 15 min; 3 h 30 min; 3 h 45 min |
| S17, S18, S19, S20 | 3 h 45 min; 1 h 45 min; 2 h 45 min; 3 h 30 min |
| S21, S22, S23, S24 | 3 h 45 min; 1 h; 3 h; 3 h 45 min |
| S25, S26 | 4 h; 4 h |

If a technical blocker would require exceeding a session's budget, save and
document the current state and bring the problem to class.

## Session Calendar

| Session | Date | Day | By the end of this session, students can... | Module/Assignment | Due | Goals |
| --- | --- | --- | --- | --- | --- | --- |
| <span id="meeting-1"></span><span id="session-1">S1</span> | 2026-08-26 | Wed | Upload and modify an Arduino sketch; identify the instrument and safety boundaries; create and commit to the course repository. | [GitHub Desktop, GitHub, VS Code, And AI](../git-vscode-ai-workflow.md) | `Prep`: setup completed in class | G1, G5, G12 |
| <span id="meeting-2"></span><span id="session-2">S2</span> | 2026-08-31 | Mon | Relate digital output, ADC input, averaging, PWM, and oscilloscope traces to physical voltage and time. | [Module 1: First Contact](lab-01/index.md) | In class: collect all `A1` evidence | G1, G2, G5 |
| <span id="meeting-3"></span><span id="session-3">S3</span> | 2026-09-02 | Wed | Build a thermistor divider; convert ADC readings to resistance and temperature; state calibration assumptions. | [Module 2: First Real Instrument Pieces](lab-02/index.md) | [**C1**](../assessment.md#c1-development-environment-and-repository) demonstrated during class, receipt by 11:55 AM; [**A1**](lab-01/index.md#a1-module-1-evidence-note) due online Sept. 7 at 5:00 PM | G1-G4, G12, G14 |
| <span id="meeting-4"></span><span id="session-4">S4</span> | 2026-09-09 | Wed | Predict and verify H-bridge PWM and direction waveforms before applying TEC power. | [Module 2](lab-02/index.md) | `Prep`: H-bridge prediction table | G1, G2, G5, G6 |
| <span id="meeting-5"></span><span id="session-5">S5</span> | 2026-09-14 | Mon | Produce safe low-power TEC heating and cooling; distinguish measurement, actuation, and feedback. | [Module 3: Manual TEC Heat/Cool And First Python GUI](lab-03/index.md) | [**C2**](../assessment.md#c2-measurement-and-actuator-electronics) demonstration; receipt 11:55 AM | G1, G3-G6 |
| <span id="meeting-6"></span><span id="session-6">S6</span> | 2026-09-16 | Wed | Parse real serial data; display and save temperature and PWM; set update interval, window, and axes. | [Module 3](lab-03/index.md) | `P1` | G2, G7, G12 |
| <span id="meeting-7"></span><span id="session-7">S7</span> | 2026-09-23 | Wed | Command heat/cool and PWM from Python; test software and hardware limits; save open-loop records. | [Module 3](lab-03/index.md) and [Module 4](lab-04/index.md) | [**C3**](../assessment.md#c3-tec-instrument-and-first-python-gui) demonstration; receipt 11:55 AM | G3, G6, G7, G12, G14 |
| <span id="meeting-8"></span><span id="session-8">S8</span> | 2026-09-28 | Mon | Measure steady temperature versus signed PWM and identify asymmetry, limits, and a steady-state criterion. | [Module 4: Open-Loop TEC Calibration And Software Safety](lab-04/index.md) | [**A2**](lab-04/index.md#a2-open-loop-tec-instrument-note) due 6:00 PM | G2, G3, G6, G7, G9 |
| <span id="meeting-9"></span><span id="session-9">S9</span> | 2026-09-30 | Wed | Implement P control and explain why nonzero actuator power produces droop. | [Module 5: P-Only Temperature Control](lab-05/index.md) | `Prep`: P-control prediction | G7-G10 |
| <span id="meeting-10"></span><span id="session-10">S10</span> | 2026-10-05 | Mon | Measure droop versus gain and characterize oscillation amplitude and frequency near instability. | [Module 5](lab-05/index.md) | Formative P-control record for A3/C4 | G3, G8, G9, G14 |
| <span id="meeting-11"></span><span id="session-11">S11</span> | 2026-10-07 | Wed | Derive and fit a one-lump energy balance; interpret heat capacity, conductance, and time constant dimensionally. | [Module 6: Modeling P And PI Temperature Control](lab-06/index.md) | Guided A2 derivation work | G9, G10, G13 |
| <span id="meeting-12"></span><span id="session-12">S12</span> | 2026-10-13 | Tue | Explain how integral action removes droop; implement anti-windup; compare P and PI responses. | [Module 6](lab-06/index.md) | `Prep`: PI-control preparation | G8-G10, G13 |
| <span id="meeting-13"></span><span id="session-13">S13</span> | 2026-10-14 | Wed | Use a two-lump model to explain thermal lag, overshoot, and gain-dependent oscillation. | [Module 6](lab-06/index.md) | [**A3**](lab-06/index.md#a3-feedback-data-and-lumped-model-memo) due 6:00 PM | G9, G10, G13, G14 |
| <span id="meeting-14"></span><span id="session-14">S14</span> | 2026-10-19 | Mon | Fit one- and two-lump models and judge whether added complexity is supported by residuals. | [Module 7: Process Model And Python Simulation](lab-07/index.md) | `P2` | G3, G7, G10, G12-G14 |
| <span id="meeting-15"></span><span id="session-15">S15</span> | 2026-10-21 | Wed | Defend the TEC controller and model; explain why a rod requires `T(x,t)` rather than a lumped temperature. | [Module 7](lab-07/index.md) | [**C4**](../assessment.md#c4-feedback-controller-and-tec-process-model) demonstration; receipt 11:55 AM | G8-G14 |
| <span id="meeting-16"></span><span id="session-16">S16</span> | 2026-10-26 | Mon | Lecture: solve the finite-length one-dimensional rod, obtain the semi-infinite limit, and introduce the transverse Biot number. | [Theory Bridge](theory-bridge-chapter-1/index.md) and [Module 8](lab-08/index.md) | `Prep`: Lienhard Chapter 1 and Section 4.5 | G11, G13, G14 |
| <span id="meeting-17"></span><span id="session-17">S17</span> | 2026-10-28 | Wed | Quantify finite-length error and transverse Biot number; calibrate and map rod thermistors for `T(x,t)`. | [Module 8: Rod Instrument, Step Response, And Stationary Fin](lab-08/index.md) | [**A4**](lab-08/index.md#a4-finite-length-and-small-biot-guided-study) due 9:05 AM | G2-G4, G11-G14 |
| <span id="meeting-18"></span><span id="session-18">S18</span> | 2026-11-02 | Mon | Acquire baseline and step-response data; lecture on the axisymmetric radial model while the experiment runs. | [Module 8](lab-08/index.md) | [**C5**](../assessment.md#c5-rod-instrument-and-data-acquisition-chain) demonstration; receipt 11:55 AM | G3, G7, G9, G11-G13 |
| <span id="meeting-19"></span><span id="session-19">S19</span> | 2026-11-04 | Wed | Fit finite-length and semi-infinite stationary profiles; compare residuals and approximation error. | [Module 8](lab-08/index.md) | Formative stationary analysis for C6/F1 | G3, G11, G13-G15 |
| <span id="meeting-20"></span><span id="session-20">S20</span> | 2026-11-09 | Mon | Complete the guided radial-model study, then tune a sinusoidal base boundary and collect an Angstrom pilot run. | [Module 9: The Angstrom Method](lab-09/index.md) | `P3` | G6-G9, G11-G13 |
| <span id="meeting-21"></span><span id="session-21">S21</span> | 2026-11-11 | Wed | Fit sensor mean, amplitude, and phase; explain exponential amplitude decay and linear phase lag. | [Module 9](lab-09/index.md) | [**A5**](lab-09/index.md#a5-angstrom-derivation-and-model-validity-plan) due 9:05 AM | G3, G7, G11, G13-G15 |
| <span id="meeting-22"></span><span id="session-22">S22</span> | 2026-11-16 | Mon | Acquire at least five settled periods and document whether the measured boundary and rod data are usable. | [Module 9](lab-09/index.md) | `P4` | G2, G3, G7, G11, G12 |
| <span id="meeting-23"></span><span id="session-23">S23</span> | 2026-11-18 | Wed | Determine spatial amplitude and phase coefficients and infer diffusivity `kappa` and loss rate `nu`. | [Module 9](lab-09/index.md) | Formative modeling-app check for C6/F1 | G3, G7, G11-G15 |
| <span id="meeting-24"></span><span id="session-24">S24</span> | 2026-11-23 | Mon | Calculate aluminum `k` and side-loss `H`; update finite-length and transverse-Biot checks using measured parameters. | [Module 10: Aluminum Conductivity, Side Heat Loss, And Final Synthesis](lab-10/index.md) | Formative A5 draft-results check | G3, G11, G13-G15 |
| <span id="meeting-25"></span><span id="session-25">S25</span> | 2026-11-30 | Mon | Compare measured and modeled `T(x,t)`; defend finite-length and finite-radius validity checks; reproduce final results. | [Module 10](lab-10/index.md) | [**C6**](../assessment.md#c6-final-thermal-transport-package) demonstration and receipt 11:55 AM | G3, G7, G11-G15 |
| <span id="meeting-26"></span><span id="session-26">S26</span> | 2026-12-02 | Wed | Present the instrument-to-model chain and individually defend hardware, software, control, and thermal-physics decisions. | [Module 10](lab-10/index.md) | `F1` | G1-G15 |

## Calendar Notes

- No class is scheduled on Monday, September 7; Monday, September 21; Monday,
  October 12; or Wednesday, November 25.
- Tuesday, October 13 is included as a Brandeis Monday make-up meeting.
- The TEC-only sequence is planned to finish by Session S15 so the second half of
  the course can focus on thermal transport in the long metal cylinder.
