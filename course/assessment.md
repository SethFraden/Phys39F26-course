# Assessment And Milestones

## What Is Being Assessed

The course assesses whether you can build, measure, model, explain, and
reproduce a physical experiment. A polished report or AI-generated program is
not sufficient by itself. You must also demonstrate the apparatus, preserve the
evidence, and explain your reasoning individually.

The [course syllabus](syllabus.md) lists the full Course Goals. The
[course calendar](labs/index.md) gives the objective and due work for every
meeting.

## Informal And Formal Assessment

The instructor speaks with each student during all 26 class meetings. Those
conversations, board work, debugging discussions, and progress checks are
formative: they reveal misconceptions early and guide the next explanation or
practice task without generating another paper to grade.

Formal assessment is deliberately limited to five written assessments, six
working-capability checkoffs, and the final presentation. During each C#
checkoff, each student answers one announced primary question and, when useful,
one short follow-up. The individual portion should normally take about **3-5
minutes per student** and occurs while laboratory work is underway.

## Assessment Codes

Every calendar entry uses one of the following labels so that you can tell
whether work is preparation, feedback, or a graded submission.

| Code | Meaning | Graded? |
| --- | --- | --- |
| `Prep` | Required pre-class preparation that will be used or checked in class | No separate score |
| `P1`-`P4` | Scheduled progress check while work is still underway | No separate score |
| `A1`-`A5` | Five key written, data-analysis, or modeling assessments | Yes; A1 is 5 points and A2-A5 are 10 points |
| `C1`-`C6` | Graded completion milestone for a working capability | Yes, 10 points |
| `GC` | Git checkpoint: a meaningful commit and push preserving the submitted state | Evidence within an `A#` or `C#`, not a separate assignment |
| `F1` | Final team presentation and individual oral defense | Yes, 10 points |

## Outside-Class Workload Rule

No class session assigns more than **four hours of outside-class work**. Each
module's workload table includes time to read the assignment itself, read and
work to understand the theory, prepare for class, analyze or code, and package
the submission. Four hours is a maximum, not a target.

Hardware measurements are completed during scheduled or instructor-approved
supervised laboratory time. If a software, access, or hardware problem would
push work beyond the stated budget, preserve the current state, document the
blocker, and bring it to class. Do not hide an unfinished step or substitute an
unverified AI result merely to meet a deadline.

## Where And How To Submit Work

The [Phys 39/169 Brandeis Moodle course](https://moodle.brandeis.edu/course/view.php?id=6589)
is the official submission and grade-record location. GitHub holds the working
code, data, figures, and documentation. Except when the instructor announces a
hardware emergency or accommodation, email is not a submission method.

### A# Written, Data, And Modeling Assignments

- Every student submits one PDF to the Moodle activity bearing the same code.
- For the team assignments `A1`, `A2`, and `A3`, both partners may upload the
  same team PDF, named `A#_Lastname_Lastname.pdf`, but each student must make a
  separate Moodle submission.
- For the individual assignments `A4` and `A5`, submit independently written
  work named `A#_Lastname.pdf`.
- Put student names, assignment code, date, repository URL, and exact Git commit
  hash on the first page.
- Include the requested reasoning, equations, tables, and figures in the PDF.
  Do not make the grader hunt through the repository to discover the answer.
- Keep code, data, and full-resolution figures in GitHub. In the PDF, give the
  exact repository paths needed to locate them.
- Submit the Moodle file and push the cited `GC` by the stated deadline.

The following assignments are **individual**: `A4` and `A5`. They assess each
student's understanding of the finite-rod/Biot and Angstrom derivations.
Assignments `A1`, `A2`, and `A3` are team assignments, so partners may submit
identical PDFs; however, each student must upload the PDF separately. Both
partners remain responsible for every part and answer individual oral questions
during the associated checkoffs.

### C# Completion Milestones

A milestone has two required pieces:

1. Demonstrate the working capability to the instructor during the scheduled
   meeting and answer the individual oral question.
2. Before the deadline, one team member submits a Moodle text response named
   `C# Team Checkoff` containing the team names, repository URL, exact commit
   hash, and paths to the README, principal code, data, and requested evidence.
   **C1 is the exception:** every student submits the text response individually,
   although teammates may submit identical text documenting their shared work.

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
- files have descriptive names and are organized by module or assignment,
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

| Check | Session and date | Show during the check |
| --- | --- | --- |
| `P1` | S6, Wed. Sept. 16 | Python reads real serial data, displays temperature and PWM, and saves a labeled data file. |
| `P2` | S14, Mon. Oct. 19 | The modeling program runs, imports an experimental trace, produces at least one fitted curve, and displays residuals. |
| `P3` | S20, Mon. Nov. 9 | Completed Angstrom reading questions, a proposed drive period, and a prediction for amplitude decay and phase lag. |
| `P4` | S22, Mon. Nov. 16 | A periodic dataset containing at least five settled cycles, sensor positions and units, acquisition metadata, and a base-temperature tracking check. |

## How Milestones Are Graded

Each completion milestone is worth 10 points. Team members normally share the
working-system, evidence, and repository points. The two oral-explanation
points are individual. Late work remains required and can recover all but the
deadline point.

### Oral Check Format

Each `C#` section below, or its linked module section, includes the questions
students should prepare. The instructor asks each student one primary question
from that milestone's list and may ask one short follow-up. A complete answer
identifies the physical or computational principle, points to relevant
hardware, code, or data when appropriate, and uses correct signs and units.
These are brief checks of understanding, not surprise examinations.

The oral check is not a separate appointment or a long examination. It is a
brief formal sample of understanding embedded in the scheduled laboratory
meeting. Informal questions during other meetings are used for feedback rather
than points.

## C1: Development Environment And Repository

**Due:** Demonstration during Session S4, Wednesday, September 9; each student
must submit a Moodle `C1 Team Checkoff` text response by **5:00 PM**. Teammates
may submit identical text, but each student must submit it separately.

The complete C1 rubric and the single authoritative set of announced questions
are in [Module 1: C1 In-Class Assessment](labs/lab-01/index.md#c1-in-class-assessment).

## C2: Measurement And Actuator Electronics

**Due:** Demonstration during Session S6, Wednesday, September 16; Moodle
`C2 Team Checkoff` receipt due by **5:00 PM**

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

**Due:** Demonstration during Session S7, Wednesday, September 23; Moodle
`C3 Team Checkoff` receipt due by **11:55 AM**

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

**Due:** Demonstration during Session S15, Wednesday, October 21; Moodle
`C4 Team Checkoff` receipt due by **11:55 AM**

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

**Due:** Demonstration during Session S18, Monday, November 2; Moodle
`C5 Team Checkoff` receipt due by **11:55 AM**

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
6. Starting from a thin rod slice, how do conservation of energy, Fourier's
   law, and Newton's law of cooling produce the stationary fin equation?
7. Write or explain the finite insulated-tip and semi-infinite analytical
   temperature profiles. Which boundary condition is lost in the
   semi-infinite limit?

## C6: Final Thermal-Transport Package

**Due:** Demonstration during Session S25, Monday, November 30; Moodle
`C6 Team Checkoff` receipt due by **11:55 AM**

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

The course uses five written assessments rather than a paper after every
module. `A1` is a 5-point introductory evidence note. `A2`-`A5` are 10-point
assessments with specific rubrics on their module pages. Intermediate notes,
plots, code, and Git checkpoints receive feedback and support the oral
checkoffs; they are not separate papers to grade.

The 5-point table below is the A1 rubric; the A2-A5 pages use expanded 10-point
rubrics.

| Criterion | Points |
| --- | ---: |
| Required calculation, analysis, or documentation is complete and technically credible | 2 |
| Requested data, figure, derivation, or other evidence is included | 1 |
| Physical interpretation, units, and uncertainty or limitations are addressed where applicable | 1 |
| Work is clear, reproducible from the linked `GC`, and submitted by the deadline | 1 |

## Fixed Graded Due Dates And Definitions

| Code | Due | What must be submitted: definition of done |
| --- | --- | --- |
| `C1` | Sept. 9, during S4; individual text response by 5:00 PM | Development environment, repository, and Module 1 measurement milestone, demonstrated using the [Module 1 C1 rubric and oral questions](labs/lab-01/index.md#c1-in-class-assessment). Every student submits the Moodle text response; teammates may use identical text. This is separate from `A1`, although both may cite the same pushed commit. |
| `A1` | Sept. 14, 5:00 PM | **Module 1 evidence note (team):** complete the [Module 1 A1 instructions](labs/lab-01/index.md#a1-module-1-evidence-note). Each student submits `A1_Lastname_Lastname.pdf` to Moodle; teammates may upload the same PDF. Keep the Markdown note, exact code, serial/averaging evidence, oscilloscope evidence, and dimensional measurements in the repository; cite the pushed `GC`. Use feedback from the earlier `C1` checkoff when completing the note. |
| `C2` | Sept. 16, during S6; receipt by 5:00 PM | [Measurement and actuator-electronics milestone](labs/lab-02/index.md#collect-your-c2-evidence-during-class), demonstrated using the C2 rubric above. |
| `C3` | Sept. 23, during S7; receipt by 11:55 AM | [TEC instrument and first-Python-GUI milestone](labs/lab-03/index.md#collect-your-c3-evidence-during-class), demonstrated using the C3 rubric above. |
| `A2` | Sept. 28, 6:00 PM | [**Open-loop TEC instrument note**](labs/lab-04/index.md#a2-open-loop-tec-instrument-note) (team): each student uploads the team PDF; teammates may upload the same file. Include the signed-PWM table, heating/cooling traces, dimensional calibration graph, asymmetry and limits, safety evidence, code/data links, and `GC`. |
| `A3` | Oct. 14, 6:00 PM | [**Feedback data and lumped-model memo**](labs/lab-06/index.md#a3-feedback-data-and-lumped-model-memo) (team): each student uploads the team PDF; teammates may upload the same file. Include selected open-loop and P/PI evidence, droop and instability, dimensional one-lump derivation, comparable P/PI metrics, anti-windup, model limits, code/data links, and `GC`. |
| `C4` | Oct. 21, during S15; receipt by 11:55 AM | [Feedback-controller and TEC-process-model milestone](labs/lab-07/index.md#c4-feedback-controller-and-tec-process-model), demonstrated using the C4 rubric above. |
| `A4` | Oct. 28, 9:05 AM | [**Finite-length and small-Biot guided study**](labs/lab-08/index.md#a4-finite-length-and-small-biot-guided-study) (individual): governing-equation derivation, Lienhard Problems 4.12 and 4.20, finite and semi-infinite solutions, sensor errors, and transverse Biot number. |
| `C5` | Nov. 2, during S18; receipt by 11:55 AM | [Rod instrument and data-acquisition milestone](labs/lab-08/index.md#c5-rod-instrument-and-data-acquisition-chain), demonstrated using the C5 rubric above. |
| `A5` | Nov. 11, 9:05 AM | [**Angstrom derivation and model-validity plan**](labs/lab-09/index.md#a5-angstrom-derivation-and-model-validity-plan) (individual): periodic relations, `kappa` and `nu`, acquisition plan, and radial-model comparison. |
| `C6` | Nov. 30, during S25; receipt by 11:55 AM | [Final thermal-transport package](labs/lab-10/index.md#c6-submission), including finite-length and finite-radius checks, demonstrated using the C6 rubric above. |
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
| Arduino primitives and signals | G1, G2, G5, G12 | A1 oscilloscope measurements and modified sketches; C1 repository check |
| First real instrument pieces | G1-G5 | Thermistor conversion, calibration evidence, H-bridge signal check, C2 |
| Manual TEC and Python GUI | G6, G7, G12, G14 | Live serial display, saved data, GUI controls, C3 |
| Open-loop TEC calibration | G3, G6, G7, G9 | Signed-PWM calibration, heating/cooling comparison, Module 4 note |
| P and PI control | G8, G9, G14 | Droop and oscillation data, P/PI comparison, oral explanation |
| Process modeling | G3, G9, G10, G13 | Lumped-model derivations, fits, residuals, C4 |
| Long-cylinder heat transport | G2-G4, G7, G11, G13, G15 | Rod calibration, finite-length solution, transverse-Biot check, stationary-fin fit, Angstrom data, C5 |
| Final synthesis | G3, G7, G11-G15 | Reproducible model, aluminum conductivity `k`, side-loss `H`, C6, presentation |
