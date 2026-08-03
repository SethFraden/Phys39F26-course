# Assessment And Milestones

## What Is Being Assessed

The course assesses whether you can build, measure, model, explain, and
reproduce a physical experiment. A polished report or AI-generated program is
not sufficient by itself. You must also demonstrate the apparatus, preserve the
evidence, and explain your reasoning individually.

The [course syllabus](syllabus.md) lists the full Course Goals. The
[course calendar](labs/index.md) gives the objective and due work for every
meeting.

## Assessment Codes

Every calendar entry uses one of the following labels so that you can tell
whether work is preparation, feedback, or a graded submission.

| Code | Meaning | Graded? |
| --- | --- | --- |
| `Prep` | Required pre-class preparation that will be used or checked in class | No separate score |
| `P1`-`P4` | Scheduled progress check while work is still underway | No separate score |
| `A1`-`A11` | Graded written, data-analysis, or modeling assignment | Yes, normally 5 points |
| `C1`-`C6` | Graded completion milestone for a working capability | Yes, 10 points |
| `GC` | Git checkpoint: a meaningful commit and push preserving the submitted state | Evidence within an `A#` or `C#`, not a separate assignment |
| `F1` | Final team presentation and individual oral defense | Yes, 10 points |

## Where And How To Submit Work

The [Phys 39/169 Brandeis Moodle course](https://moodle.brandeis.edu/course/view.php?id=6589)
is the official submission and grade-record location. GitHub holds the working
code, data, figures, and documentation. Except when the instructor announces a
hardware emergency or accommodation, email is not a submission method.

### A# Written, Data, And Modeling Assignments

- Submit one PDF to the Moodle activity bearing the same code, such as `A8`.
- Name a team file `A8_Lastname_Lastname.pdf`; name an individual file
  `A7_Lastname.pdf`.
- Put student names, assignment code, date, repository URL, and exact Git commit
  hash on the first page.
- Include the requested reasoning, equations, tables, and figures in the PDF.
  Do not make the grader hunt through the repository to discover the answer.
- Keep code, data, and full-resolution figures in GitHub. In the PDF, give the
  exact repository paths needed to locate them.
- Submit the Moodle file and push the cited `GC` by the stated deadline.

The following assignments are **individual**: `A4`, `A6`, `A7`, and `A9`.
They assess each student's understanding of the thermal-model derivations and
reading. Assignments `A1`-`A3`, `A5`, `A8`, `A10`, and `A11` are normally one
submission per laboratory team; both partners remain responsible for every
part.

### C# Completion Milestones

A milestone has two required pieces:

1. Demonstrate the working capability to the instructor during the scheduled
   meeting and answer the individual oral question.
2. Before the deadline, one team member submits a Moodle text response named
   `C# Team Checkoff` containing the team names, repository URL, exact commit
   hash, and paths to the README, principal code, data, and requested evidence.

The instructor records the shared system/evidence/repository points and the
individual oral points in Moodle. A demonstration without the Moodle receipt
and cited commit is not a complete milestone.

### P#, Prep, And F1

- `Prep` and `P#` work is brought to class and shown when requested; there is no
  separate Moodle upload unless the instructor announces one.
- For `F1`, one team member uploads `F1_Lastname_Lastname_slides.pdf` to Moodle
  and cites the final repository commit. Each student completes the individual
  oral defense during the presentation.

## What Counts As A Git Checkpoint

For every required `GC`, the grader will look for all of the following:

- the cited commit exists on GitHub and was pushed by the deadline,
- the Moodle submission gives the repository URL and full commit hash,
- the commit contains the exact Arduino, Python, analysis, or documentation
  version used for the submitted result,
- a README identifies the hardware assumptions, data format, dependencies, and
  exact command needed to run or reproduce the work,
- data and figures named in the submission are present at the cited paths,
- files have descriptive names and are organized by lab or assignment,
- the commit message says what capability or analysis was completed,
- another person can follow the README from a fresh checkout without guessing
  which of several similarly named files is authoritative.

<!-- Generated data too large for GitHub may be stored in an instructor-approved
location, but the repository must contain a small example plus a README link
and description. Secrets, passwords, and private tokens must never be committed. -->

Use this Moodle receipt template for an `A#` or `C#` submission:

```text
Assignment or milestone:
Student name(s):
Repository URL:
Branch:
Full commit hash:
README path:
Principal code path(s):
Data and figure path(s):
Command used to reproduce the result:
```

## Progress Checks

Progress checks are brief demonstrations or reviews. They identify problems
early and do not create another document to grade. Bring the current apparatus,
code, plots, and repository state.

| Check | Meeting and date | Show during the check |
| --- | --- | --- |
| `P1` | M6, Wed. Sept. 16 | Python reads real serial data, displays temperature and PWM, and saves a labeled data file. |
| `P2` | M14, Mon. Oct. 19 | The modeling program runs, imports an experimental trace, produces at least one fitted curve, and displays residuals. |
| `P3` | M20, Mon. Nov. 9 | Completed Angstrom reading questions, a proposed drive period, and a prediction for amplitude decay and phase lag. |
| `P4` | M22, Mon. Nov. 16 | A periodic dataset containing at least five settled cycles, sensor positions and units, acquisition metadata, and a base-temperature tracking check. |

## How Milestones Are Graded

Each completion milestone is worth 10 points. Team members normally share the
working-system, evidence, and repository points. The two oral-explanation
points are individual. Late work remains required and can recover all but the
deadline point.

### Oral Check Format

Each `C#` section below includes the questions students should prepare. The
instructor asks each student one primary question from that milestone's list
and may ask one short follow-up. A complete answer identifies the physical or
computational principle, points to relevant hardware, code, or data when
appropriate, and uses correct signs and units. These are brief checks of
understanding, not surprise examinations.

## C1: Development Environment And Repository

**Due:** Meeting 3, Wednesday, September 2

| Criterion | Points |
| --- | ---: |
| Arduino IDE, VS Code, and GitHub workflow operate; a modified sketch uploads and runs | 4 |
| Organized folder and short README identify what was tested | 2 |
| Meaningful commit is pushed and can be located | 1 |
| Individual explains files, upload, commit, and push | 2 |
| Complete by the deadline | 1 |

### C1 Oral Questions

1. Show where the Arduino sketch is stored. What did you change, and how can
   you tell the uploaded board is running that version?
2. What is the difference between saving a file, committing it, and pushing it?
3. Starting from the cited commit, show how you would inspect or recover the
   preceding version of one file.

## C2: Measurement And Actuator Electronics

**Due:** Meeting 5, Monday, September 14

| Criterion | Points |
| --- | ---: |
| Thermistor reports plausible calibrated temperature; H-bridge PWM and direction signals are correct and safely verified | 4 |
| Wiring evidence and oscilloscope/measurement table are present | 2 |
| Current Arduino code and documentation are pushed | 1 |
| Individual explains divider conversion, PWM, and expected H-bridge inputs | 2 |
| Complete by the deadline | 1 |

### C2 Oral Questions

1. Starting from the divider circuit, derive the equation used to convert the
   measured voltage into thermistor resistance.
2. For heating, cooling, and zero output, what signals should appear on the two
   H-bridge PWM inputs?
3. Point to an oscilloscope trace. What are its frequency, duty cycle, high and
   low voltages, and physical meaning?

## C3: TEC Instrument And First Python GUI

**Due:** Meeting 7, Wednesday, September 23

| Criterion | Points |
| --- | ---: |
| Protected TEC heats and cools under GUI command; Python displays and saves real serial data | 4 |
| Open-loop heat and cool records include labels, units, and operating limits | 2 |
| Arduino and Python versions used for the demonstration are pushed | 1 |
| Individual explains serial parsing, GUI controls, and safety behavior | 2 |
| Complete by the deadline | 1 |

### C3 Oral Questions

1. Trace one temperature value from Arduino `analogRead()` through the serial
   line to the Python plot.
2. How do the PWM slider and text entry stay synchronized, and what value is
   actually sent to the Arduino?
3. What should the software and hardware do after an invalid temperature,
   broken serial connection, or over-temperature condition?

## C4: Feedback Controller And TEC Process Model

**Due:** Meeting 15, Wednesday, October 21

| Criterion | Points |
| --- | ---: |
| P and PI control operate safely; one- or two-lump model runs and is compared with data | 4 |
| Droop, oscillation, and model-residual evidence support the conclusions | 2 |
| Reproducible controller/model code and parameter record are pushed | 1 |
| Individual explains droop, integral action, lag, and one model limitation | 2 |
| Complete by the deadline | 1 |

### C4 Oral Questions

1. Why does P-only control have droop? Use the steady-state controller and
   thermal-balance equations in your explanation.
2. Why can integral action remove droop, and what is integral windup?
3. Which physical lag in the apparatus can produce overshoot or oscillation as
   gain increases?
4. Identify one fitted model parameter, give its units, and explain how the
   data constrain it.

## C5: Rod Instrument And Data-Acquisition Chain

**Due:** Meeting 18, Monday, November 2

| Criterion | Points |
| --- | ---: |
| Mapped thermistors and synchronized multichannel logging acquire credible `T(x,t)` data | 4 |
| Calibration, baseline, initial step response, coordinates, units, and metadata are present | 2 |
| Acquisition code and data organization are reproducible | 1 |
| Individual explains the measurement chain and a dominant uncertainty | 2 |
| Complete by the deadline | 1 |

### C5 Oral Questions

1. Choose one rod sensor and trace its channel number, physical position,
   calibration, serial field, and saved-data column.
2. Why must the sensor streams and base temperature share a time reference?
3. What metadata are required to interpret `T(x,t)` six months later?
4. Identify the largest measurement uncertainty at this stage and describe how
   it affects the later conductivity result.
5. What two different approximations are meant by calling the rod "long and
   thin"? Which calculation tests each approximation?

## C6: Final Thermal-Transport Package

**Due:** Meeting 25, Monday, November 30

| Criterion | Points |
| --- | ---: |
| Angstrom analysis reports `q`, `q_prime`, `kappa`, aluminum `k`, `nu`, and side-loss `H` with dimensional equations | 4 |
| Uncertainties, residuals, accepted-value comparison, and finite-length, finite-radius, and frequency/model checks are present | 2 |
| A fresh run from the documented repository reproduces the principal values and figures | 1 |
| Individual explains how amplitude decay and phase lag separate conductivity from side loss | 2 |
| Complete by the deadline | 1 |

### C6 Oral Questions

These questions are also the announced question bank for the individual part
of `F1`.

1. How are `q` and `q_prime` obtained from the measured amplitudes and phases?
2. Why are both amplitude decay and phase lag needed to separate diffusivity
   from side heat loss?
3. Derive or explain `kappa = omega/(2*q*q_prime)` and
   `nu = kappa*(q^2 - q_prime^2)`, including units.
4. How are `kappa` and `nu` converted into aluminum conductivity `k` and
   side heat-transfer coefficient `H`?
5. Point to one residual plot or frequency-consistency check. What model failure
   would it reveal?
6. Which systematic uncertainty most limits your reported `k` or `H`, and why?
7. How did you quantify the error caused by treating the finite rod as
   semi-infinite? Why can the answer depend on sensor position?
8. Define the transverse Biot number for the circular rod. What physical
   approximation does a small value justify?
9. In the guided radial calculation, why did the surface, centerline, and
   cross-sectional mean temperatures differ? Which one does a surface
   thermistor measure most directly?

## Graded Assignment Rubric

Assignments `A1` through `A11` are normally worth 5 points. Unless an
assignment page specifies otherwise, use this rubric:

| Criterion | Points |
| --- | ---: |
| Required calculation, analysis, or documentation is complete and technically credible | 2 |
| Requested data, figure, derivation, or other evidence is included | 1 |
| Physical interpretation, units, and uncertainty or limitations are addressed where applicable | 1 |
| Work is clear, reproducible from the linked `GC`, and submitted by the deadline | 1 |

## Fixed Graded Due Dates And Definitions

| Code | Due | What must be submitted: definition of done |
| --- | --- | --- |
| `A1` | Sept. 2 | **Lab 1 evidence note:** a Markdown record naming the Arduino examples tested, the modifications made, and oscilloscope or measured evidence for digital timing, analog input, averaging, and PWM. Link the relevant sketches and `GC`. |
| `C1` | Sept. 2 | Development environment and repository milestone, demonstrated using the rubric above. |
| `C2` | Sept. 14 | Measurement and actuator-electronics milestone, demonstrated using the rubric above. |
| `C3` | Sept. 23 | TEC instrument and first-Python-GUI milestone, demonstrated using the rubric above. |
| `A2` | Sept. 28 | **Open-loop TEC note:** signed-PWM settings, labeled heating and cooling records, the criterion used to call a temperature steady, observed asymmetry or saturation, and the operating limits used. |
| `A3` | Oct. 5 | **P-control data package:** setpoint and gain table, measured droop versus gain, time traces near instability, oscillation amplitude and frequency versus gain, safety limit, interpretation, data, code, and `GC`. |
| `A4` | Oct. 7 | **One-lump derivation:** dimensional energy-balance equation, equilibrium temperature, time constant, definition and units of every parameter, and a comparison with one measured transient or stated testable prediction. |
| `A5` | Oct. 14 | **P/PI analysis memo:** P and PI responses under comparable conditions, quantitative droop and transient metrics, actuator saturation evidence, and an explanation of integral action and anti-windup. |
| `A6` | Oct. 21 | **Heat-transfer reading memo:** one page connecting Fourier conduction, side heat loss, boundary conditions, and measurable quantities to the aluminum-rod experiment. |
| `C4` | Oct. 21 | Feedback-controller and TEC-process-model milestone, demonstrated using the rubric above. |
| `A7` | Oct. 28 | **Finite-length and small-Biot guided study (individual):** using Lienhard Section 4.5, complete Problems 4.12 and 4.20; derive the finite insulated-tip profile and its semi-infinite limit; calculate `mL`, finite-versus-infinite error at each sensor, and the transverse Biot number; state separately when length and radius may be ignored. |
| `C5` | Nov. 2 | Rod instrument and data-acquisition milestone, demonstrated using the rubric above. |
| `A8` | Nov. 4 | **Stationary-fin analysis:** plot steady excess temperature `theta(x) = T(x) - T_room` versus position with units; fit both finite-length and semi-infinite models; compare residuals and the shift in `m`; report the decay coefficient in `1/m` with uncertainty; explain `m^2 = HP/(kA)` and why this steady fit alone cannot separate `H` from `k`. Include data, fit code, and `GC`. |
| `A9` | Nov. 11 | **Angstrom derivation and model-validity plan (individual):** derive or explain the periodic amplitude and phase relations; show how `q` and `q_prime` determine `kappa` and `nu`; choose and justify the drive period, sampling interval, settled-cycle count, and sensor range; include the guided numerical comparison for transverse Biot numbers `0.01`, `0.1`, and `1`, and state whether the course rod supports one-dimensional analysis. |
| `A10` | Nov. 18 | **Modeling-app draft:** runnable code loads rod data, fits a sinusoid at every sensor, plots amplitude and unwrapped phase versus position, fits `q` and `q_prime`, estimates `kappa` and `nu`, shows intermediate plots and residuals, and includes run instructions plus `GC`. |
| `A11` | Nov. 23 | **Draft conductivity and heat-loss results:** preliminary `k = kappa*rho*c` and `H = nu*rho*c*A/P`, with units, uncertainty, accepted-value comparison, frequency/model check, and dominant systematic limitations. |
| `C6` | Nov. 30 | Final thermal-transport package, including the finite-length check and guided numerical finite-radius comparison, demonstrated using the rubric above. |
| `F1` | Dec. 2 | Final team presentation and individual oral defense, using the rubric below. |

## F1: Final Presentation And Individual Oral Defense

The individual `F1` oral defense uses the announced questions in the
[C6 Oral Questions](#c6-oral-questions) section above.

| Criterion | Points |
| --- | ---: |
| Team clearly explains the instrument, control system, rod experiment, and analysis chain | 3 |
| Results for aluminum `k` and side-loss `H` include units, uncertainty, evidence, and limitations | 2 |
| Figures are readable and the repository can reproduce the principal results | 1 |
| Individual accurately answers questions about hardware, software, control, and thermal physics | 3 |
| Presentation is complete and delivered on the scheduled final meeting | 1 |

## Course Goal Coverage

| Major course unit | Goals assessed | Principal evidence |
| --- | --- | --- |
| Arduino primitives and signals | G1, G2, G5, G12 | Oscilloscope measurements, modified sketches, C1 |
| First real instrument pieces | G1-G5 | Thermistor conversion, calibration evidence, H-bridge signal check, C2 |
| Manual TEC and Python GUI | G6, G7, G12, G14 | Live serial display, saved data, GUI controls, C3 |
| Open-loop TEC calibration | G3, G6, G7, G9 | Signed-PWM calibration, heating/cooling comparison, Lab 4 note |
| P and PI control | G8, G9, G14 | Droop and oscillation data, P/PI comparison, oral explanation |
| Process modeling | G3, G9, G10, G13 | Lumped-model derivations, fits, residuals, C4 |
| Long-cylinder heat transport | G2-G4, G7, G11, G13, G15 | Rod calibration, finite-length solution, transverse-Biot check, stationary-fin fit, Angstrom data, C5 |
| Final synthesis | G3, G7, G11-G15 | Reproducible model, aluminum conductivity `k`, side-loss `H`, C6, presentation |
