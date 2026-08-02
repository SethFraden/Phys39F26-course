# Assessment And Milestones

## What Is Being Assessed

The course assesses whether you can build, measure, model, explain, and
reproduce a physical experiment. A polished report or AI-generated program is
not sufficient by itself. You must also demonstrate the apparatus, preserve the
evidence, and explain your reasoning individually.

The [course syllabus](syllabus.md) lists the full Course Goals. The
[course calendar](labs/index.md) gives the objective and due work for every
meeting.

## Progress Checks, Milestones, And Git Checkpoints

- A **progress check** is an informal review used to identify problems while
  work is still underway. It is not a separate graded submission.
- A **completion milestone**, labeled `C1` through `C6`, is a graded deadline
  for a working hardware, software, or modeling capability.
- A **Git checkpoint** is a meaningful commit that preserves a recoverable
  stage of the work. It is evidence within an assignment, not a separate
  assignment.

## How Milestones Are Graded

Each completion milestone is worth 10 points. Team members normally share the
working-system, evidence, and repository points. The two oral-explanation
points are individual. Late work remains required and can recover all but the
deadline point.

## C1: Development Environment And Repository

**Due:** Meeting 3, Wednesday, September 2

| Criterion | Points |
| --- | ---: |
| Arduino IDE, VS Code, and GitHub workflow operate; a modified sketch uploads and runs | 4 |
| Organized folder and short README identify what was tested | 2 |
| Meaningful commit is pushed and can be located | 1 |
| Individual explains files, upload, commit, and push | 2 |
| Complete by the deadline | 1 |

## C2: Measurement And Actuator Electronics

**Due:** Meeting 5, Monday, September 14

| Criterion | Points |
| --- | ---: |
| Thermistor reports plausible calibrated temperature; H-bridge PWM and direction signals are correct and safely verified | 4 |
| Wiring evidence and oscilloscope/measurement table are present | 2 |
| Current Arduino code and documentation are pushed | 1 |
| Individual explains divider conversion, PWM, and expected H-bridge inputs | 2 |
| Complete by the deadline | 1 |

## C3: TEC Instrument And First Python GUI

**Due:** Meeting 7, Wednesday, September 23

| Criterion | Points |
| --- | ---: |
| Protected TEC heats and cools under GUI command; Python displays and saves real serial data | 4 |
| Open-loop heat and cool records include labels, units, and operating limits | 2 |
| Arduino and Python versions used for the demonstration are pushed | 1 |
| Individual explains serial parsing, GUI controls, and safety behavior | 2 |
| Complete by the deadline | 1 |

## C4: Feedback Controller And TEC Process Model

**Due:** Meeting 15, Wednesday, October 21

| Criterion | Points |
| --- | ---: |
| P and PI control operate safely; one- or two-lump model runs and is compared with data | 4 |
| Droop, oscillation, and model-residual evidence support the conclusions | 2 |
| Reproducible controller/model code and parameter record are pushed | 1 |
| Individual explains droop, integral action, lag, and one model limitation | 2 |
| Complete by the deadline | 1 |

## C5: Rod Instrument And Data-Acquisition Chain

**Due:** Meeting 18, Monday, November 2

| Criterion | Points |
| --- | ---: |
| Mapped thermistors and synchronized multichannel logging acquire credible `T(x,t)` data | 4 |
| Calibration, baseline, initial step response, coordinates, units, and metadata are present | 2 |
| Acquisition code and data organization are reproducible | 1 |
| Individual explains the measurement chain and a dominant uncertainty | 2 |
| Complete by the deadline | 1 |

## C6: Final Thermal-Transport Package

**Due:** Meeting 25, Monday, November 30

| Criterion | Points |
| --- | ---: |
| Angstrom analysis reports `q`, `q_prime`, `kappa`, aluminum `k`, `nu`, and side-loss `H` with dimensional equations | 4 |
| Uncertainties, residuals, accepted-value comparison, and frequency/model checks are present | 2 |
| A fresh run from the documented repository reproduces the principal values and figures | 1 |
| Individual explains how amplitude decay and phase lag separate conductivity from side loss | 2 |
| Complete by the deadline | 1 |

## Fixed Graded Due Dates

| Due | Work |
| --- | --- |
| Sept. 2 | C1; Lab 1 note |
| Sept. 14 | C2 |
| Sept. 23 | C3 |
| Sept. 28 | Lab 4 open-loop note |
| Oct. 5 | P-control data package |
| Oct. 7 | One-lump derivation |
| Oct. 14 | P/PI analysis memo |
| Oct. 21 | C4; heat-transfer reading memo |
| Oct. 28 | Heat-equation and dimensional-analysis derivation |
| Nov. 2 | C5 |
| Nov. 4 | Stationary-fin analysis |
| Nov. 11 | Angstrom derivation and experiment plan |
| Nov. 18 | Modeling-app draft |
| Nov. 23 | Draft conductivity and heat-loss results |
| Nov. 30 | C6; final analysis packet |
| Dec. 2 | Final presentation and individual oral defense |

## Course Goal Coverage

| Major course unit | Goals assessed | Principal evidence |
| --- | --- | --- |
| Arduino primitives and signals | G1, G2, G5, G12 | Oscilloscope measurements, modified sketches, C1 |
| First real instrument pieces | G1-G5 | Thermistor conversion, calibration evidence, H-bridge signal check, C2 |
| Manual TEC and Python GUI | G6, G7, G12, G14 | Live serial display, saved data, GUI controls, C3 |
| Open-loop TEC calibration | G3, G6, G7, G9 | Signed-PWM calibration, heating/cooling comparison, Lab 4 note |
| P and PI control | G8, G9, G14 | Droop and oscillation data, P/PI comparison, oral explanation |
| Process modeling | G3, G9, G10, G13 | Lumped-model derivations, fits, residuals, C4 |
| Long-cylinder heat transport | G2-G4, G7, G11, G13, G15 | Rod calibration, heat equation, stationary-fin fit, Angstrom data, C5 |
| Final synthesis | G3, G7, G11-G15 | Reproducible model, aluminum conductivity `k`, side-loss `H`, C6, presentation |

## Individual Understanding

Short oral questions are embedded in milestone checkoffs and the final
presentation. They are not intended as surprise examinations. Typical prompts
ask you to:

- trace one measured value from voltage to a plotted temperature,
- predict the H-bridge inputs for heating or cooling,
- explain why P control has droop or why integral action can wind up,
- identify each term and unit in a thermal model,
- explain one residual or systematic error,
- explain why both amplitude decay and phase lag are needed to determine
  conductivity and side loss.

This structure makes individual understanding visible without requiring a
separate long oral examination.
