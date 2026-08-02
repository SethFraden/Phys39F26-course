# Phys 39 / 169 Syllabus 

**Instrumentation and Thermal Physics**  
**Fall 2026 - Brandeis University**  
**Instructor:** Prof. Seth Fraden  
**Email:** fraden@brandeis.edu  
**Office:** 214 Abelson  
**Office hours:** By appointment, and scheduled times to be announced  
**Meeting time:** Monday and Wednesday, 9:05 AM-11:55 AM  
**Classroom/laboratory:** 340 Abelson  
**Course website:** <https://sethfraden.github.io/Phys39F26-course/>

<!-- **Draft status:** This syllabus is a working draft for instructor review. Items
marked TBD should be checked before posting to Brandeis or the public course
website. -->

## Welcome

Welcome to Physics 39/169, Advanced Laboratory. This is a course about building a real instrument, using it to control a physical quantity, and to make measurements from which to extract physical parameters.   While you don't construct from scratch, the project involves some assembly. 

The first part of the course builds toward temperature control with a
thermoelectric cooler (TEC). You will use an Arduino to measure voltages across thermistors,
generate pulse-width modulation (PWM) signals to drive an electronic switch (H-bridge), communicate with a laptop over USB serial, build Python tools for live plotting, and implement Proportional - Integral (PI) feedback control. You will use lumped thermal models for understanding the relationship between heat and temperature and  for elucidating the use of feedback to control temperature.

The second part of the course leverages the same experimental platform to study heat transport in a
long metal cylinder, modeling the flow using the heat equation to connect your data to physical models, and implementing the Angstrom method to measure thermal conductivity.


Feedback and control theory are important ideas that should form part of the
education of a physicist but rarely do. They are important for any experimentalist, but also for theorists as the concept of control is central to dynamical systems. This course aims to give enough of the
formal elements of control theory and practice to satisfy the experimentalist
designing or running a typical physics experiment, and enough modeling to
connect the instrument to thermal physics.

## Course Goals

By the end of the course, you should be able to:

- **G1.** Build and debug simple Arduino-based laboratory instruments.
- **G2.** Measure analog voltages and understand digitization, averaging, noise, and
  calibration.
- **G3.** Address limitations in measurement precision and systematic error.
- **G4.** Convert thermistor voltage-divider measurements into temperature estimates.
- **G5.** Use an oscilloscope to verify timing, digital signals, PWM, and H-bridge
  control signals.
- **G6.** Drive a TEC in heating and cooling directions.
- **G7.** Use Python to read serial data, plot live strip charts, save data, and build
  simple GUI controls.
- **G8.** Implement and interpret manual, proportional, and PI temperature control.
- **G9.** Measure droop, steady-state response, step response, oscillation, and the
  onset of instability.
- **G10.** Develop simple lumped thermal models and compare them with experiment.
- **G11.** Move from lumped models to spatial heat-transport models.
- **G12.** Use Git, GitHub, VS Code, Markdown, and an AI coding assistant to document
  and organize experimental work.
- **G13.** Learn the advantages of dimensional analysis and convert between dimensionless and dimensionfull quantities.
- **G14.** Communicate experimental results in written reports, code repositories, and
  oral presentation.
- **G15.** Use steady and periodically forced rod measurements, including the
  Angstrom method, to determine the thermal conductivity of aluminum and the
  rod's side heat-transfer coefficient with uncertainty.

## Format

The course meets twice per week in a laboratory format. Most meetings will
combine:

- a short discussion or board-work exercise,
- hands-on hardware work,
- software development or modification,
- data collection,
- model-building or interpretation,
- documentation in a Git repository.

You should expect the course to feel iterative. Hardware measurements and
software models will be developed together in small steps.

## Tools And Materials

Bring a Windows or Apple laptop. Let the instructor know if you don't have one. The course will use software for:

- Arduino IDE,
- Python,
- VS Code,
- Git and GitHub,
- Markdown,
- AI coding assistants such as GitHub Copilot.

The course website contains setup instructions:

<https://sethfraden.github.io/Phys39F26-course/getting-started/>

## Readings

Readings will be assigned as needed from course notes, web resources, and
selected articles or textbook chapters. Important recurring references include:

- John H. Lienhard IV and John H. Lienhard V, *A Heat Transfer Textbook*.
- John Bechhoefer, "Feedback for physicists: A tutorial essay on control,"
  *Reviews of Modern Physics* 77, 783 (2005).
- John Bechhoefer, *Control Theory for Physicists*.
- Arduino documentation and examples.
- Course website notes on hardware, Arduino, Git/VS Code/AI, and lab safety.

The course will emphasize reading for use: you should be able to connect a
reading to a measurement, circuit, code fragment, or model equation.

## Major Course Units

The  Fall 2026 schedule includes 26 class meetings covering 8 topics.

1. **Arduino primitives and signals**  
   Digital output, analog input, digitization, averaging, noise, PWM,
   oscilloscope verification, and basic Arduino debugging.

2. **First real instrument pieces**  
   Thermistor serial data, temperature conversion and calibration, measurement
   precision and systematic error, Arduino Serial Plotter, and H-bridge
   logic/PWM checks.

3. **Manual TEC heat/cool and Python GUI development**  
   Manual actuator control, live strip charts, saved data, GUI modification,
   serial parsing, and Git/GitHub, VS Code, Markdown, and AI-assisted
   documentation.

4. **Open-loop TEC calibration and software safety**  
   Heating/cooling asymmetry, steady-state response, data logging, and limits.

5. **P-only and PI feedback control**  
   Droop, gain, oscillation, instability, integral action, and windup.

6. **Process modeling**  
   Lumped thermal models, dimensional analysis, time constants, thermal lag,
   Python simulation, and comparison of models with experiment.

7. **Long-cylinder heat transport**  
   Temperature along a rod, heat equation, step and periodic forcing, amplitude
   decay, phase lag, and the Angstrom method.

8. **Final synthesis**  
   Modeling app, measured-versus-predicted comparison, final analysis,
   reproducible code repositories, written reports, and oral presentations.

### How Units, Goals, And Assessments Align

| Major unit | Principal goals | Direct assessment evidence |
| --- | --- | --- |
| 1. Arduino primitives and signals | G1, G2, G5, G12 | Oscilloscope measurements, modified sketches, C1 repository check |
| 2. First real instrument pieces | G1-G5 | Thermistor conversion, calibration evidence, H-bridge signal check, C2 |
| 3. Manual TEC and Python GUI | G6, G7, G12, G14 | Live serial display, saved data, GUI controls, C3 |
| 4. Open-loop TEC calibration | G3, G6, G7, G9 | Signed-PWM calibration, heating/cooling comparison, Lab 4 note |
| 5. P and PI control | G8, G9, G14 | Droop and oscillation data, P/PI comparison, individual explanation |
| 6. Process modeling | G3, G9, G10, G13 | One- and two-lump derivations, model fits, residuals, C4 |
| 7. Long-cylinder heat transport | G2-G4, G7, G11, G13, G15 | Rod calibration, heat-equation derivation, stationary-fin fit, Angstrom data, C5 |
| 8. Final synthesis | G3, G7, G11-G15 | Reproducible model, aluminum `k`, side-loss `H`, C6, final presentation and oral defense |

The current course calendar is maintained on the course website:

<https://sethfraden.github.io/Phys39F26-course/labs/>

## Assignments And Grading

There are no exams. Evaluation will be based on laboratory participation,
documentation, written work, modeling, code, and final presentation.

Draft grading plan:

| Component | Weight |
| --- | ---: |
| Attendance, preparation, and lab participation | 20% |
| Lab notes, checkoffs, and short assignments | 20% |
| Code, GitHub documentation, and reproducibility | 15% |
| Modeling assignments and modeling app | 20% |
| Written reports or project writeups | 15% |
| Final oral presentation | 10% |


### Lab Notes And Documentation

Six graded completion milestones establish deadlines for major instrumentation,
hardware, and software capabilities. Meeting each deadline is part of the lab
notes, checkoffs, and short assignments grade. At each milestone, the team must
demonstrate a safely functioning system, current code and documentation in its
repository, and enough individual understanding for each student to explain the
work. The milestone dates and definitions are listed in the
[course calendar](https://sethfraden.github.io/Phys39F26-course/labs/).

Each milestone is worth 10 points. The standard structure is 4 points for the
required working capability, 2 points for experimental or analytical evidence,
1 point for current reproducible repository documentation, 2 points for an
individual oral explanation, and 1 point for completion by the deadline.
Milestone-specific rubrics are published with the course calendar. Late work
must still be completed and can recover every point except the deadline point.

You will keep a record of what you built, measured, changed, and learned. Your
documentation should include:

- wiring diagrams or clear photos when useful,
- Arduino sketches and Python code,
- data files or links to data files,
- plots,
- model equations,
- short explanations of what worked and what failed,
- notes on how AI assistance was used.

The goal is not polished perfection every week. The goal is a recoverable,
understandable record of experimental progress.

### Fixed Assignment Dates

| Due | Graded work |
| --- | --- |
| Sept. 2 | C1 and Lab 1 note |
| Sept. 14 | C2 |
| Sept. 23 | C3 |
| Sept. 28 | Lab 4 open-loop note |
| Oct. 5 | P-control data package |
| Oct. 7 | One-lump derivation |
| Oct. 14 | P/PI analysis memo |
| Oct. 21 | C4 and heat-transfer reading memo |
| Oct. 28 | Heat-equation and dimensional-analysis derivation |
| Nov. 2 | C5 |
| Nov. 4 | Stationary-fin analysis |
| Nov. 11 | Angstrom derivation and experiment plan |
| Nov. 18 | Modeling-app draft |
| Nov. 23 | Draft conductivity and heat-loss results |
| Nov. 30 | C6 and final analysis packet |
| Dec. 2 | Final presentation and individual oral defense |

### Written Reports

The course will include substantial written work distributed across the fixed
dates above. The principal pieces include:

- a mid-course temperature-control report or project checkpoint,
- a modeling-app checkpoint,
- thermal-transport theory/modeling assignments,
- final analysis and presentation material.

### Presentations

Final presentations will occur on the last class meeting. Each team will explain
what they measured, what model they used, how well the model worked, and what
they would improve next.

## Teams

You will usually work in teams of two. Teamwork is part of the course. Both
partners should understand the hardware, the code, the data, and the model. It
is acceptable for partners to have different strengths, but it is not acceptable
for one partner to be the only person who understands an essential part of the
project.

## Use Of AI Coding Assistants

AI coding assistants are allowed and encouraged in this course, but they must be
used thoughtfully. You may use AI to:

- explain code,
- write Arduino sketches,
- write Python,
- generate draft plots or GUIs,
- improve documentation,
- propose model equations,
- help organize Git commits and Markdown notes.

You remain responsible for understanding and testing anything you submit. You
should be able to explain what your code does, what data it expects, what output
it produces, and what assumptions it makes. If AI substantially helps with an
assignment, briefly note how it was used.

Do not submit code or text that you cannot explain. Do not use AI to fabricate
data, conceal errors, or misrepresent what happened in the lab.

## Git, GitHub, And VS Code

You will use Git and GitHub to organize course work. The minimum expectation is
that you can:

- keep course files in a clear folder structure,
- edit Markdown and code in VS Code,
- commit meaningful checkpoints,
- push to GitHub,
- recover earlier versions when needed,
- document what changed and why.

Early in the course we will practice only the minimum workflow needed to be
productive. More advanced Git use will be introduced only as needed.

## Attendance And Laboratory Work

Lab attendance is expected. Each meeting depends on hands-on work, shared
equipment, and collaboration with your partner, so it cannot be fully replaced
by work done later on your own.

This course expects 180 hours of work, divided between 26 in-class meetings and
out-of-class activities. The 26 scheduled meetings of 2 hours 50 minutes total
73 hours 40 minutes in class. This leaves 106 hours 20 minutes outside class,
or an average of approximately 4 hours 5 minutes preparing for and following up
on each lab meeting. This outside work includes readings, code development,
data analysis, model derivations, GitHub documentation, and report or
presentation preparation. The amount will vary from week to week.

Attendance matters because this is a laboratory course. Many assignments depend
on hardware measurements that are difficult to reproduce outside scheduled lab
time. If you must miss class, contact the instructor as soon as possible and
make a plan to catch up.

Because students work in teams, an absence affects other people. Communicate
early and clearly with your partner and the instructor.

## Safety

This course uses electrical power supplies, soldering irons, hot/cold TEC
assemblies, tools, and laboratory hardware. You are expected to follow all
safety instructions given in class and on the course website. In particular:

- Do not power a circuit until the wiring has been checked when requested.
- Do not leave powered heating/cooling hardware unattended unless the instructor
  has explicitly approved the setup.
- Use current limits and software limits when instructed.
- Treat unexpected heating, smell, smoke, unstable behavior, or repeated serial
  failures as reasons to stop and ask for help.

Safety boundaries may override any assignment instruction.

## Academic Integrity

You are expected to follow Brandeis policies on academic integrity. Your data,
code, plots, reports, and presentations should honestly represent your own work
and your team's work. Collaboration is expected; misrepresentation is not.

You are expected to be familiar with, and to follow, the University's policies
on academic integrity. You are expected to be honest in all of your academic
work. Please consult [Brandeis University Rights and
Responsibilities](https://www.brandeis.edu/student-rights-community-standards/rights-responsibilities/current/section-4.html)
for all policies and procedures related to academic integrity. Allegations of
academic dishonesty will be forwarded to Student Rights and Community Standards.
Sanctions for academic dishonesty can include failing grades and/or suspension
from the University. Citation and research assistance can be found through the
[Brandeis Library](https://library.brandeis.edu/).

## Accessibility And Accommodations

Brandeis seeks to create a learning environment that is welcoming and inclusive.
Students who may need disability-related academic accommodations should work
with Student Accessibility Support (SAS). SAS can be reached at
access@brandeis.edu and 781-736-3537.

Student Accessibility Support information:

<https://www.brandeis.edu/accessibility/>

If you already have an accommodation letter, please share it with the instructor
as early as possible so that accommodations can be implemented effectively in
the laboratory setting.

<!-- TBD: before posting, check whether Brandeis requires exact current SAS syllabus
language for Fall 2026. -->

## Classroom Climate

Laboratory work involves uncertainty, mistakes, and revision. A useful lab
culture is one in which people can ask naive questions, report confusing data,
admit that code does not work, and help each other reason through problems.
Everyone is expected to contribute to a respectful, serious, and generous
working environment.


## Graduate Students In Phys 169

Students enrolled in Phys 169 will participate in the same laboratory sequence.
Graduate-level expectations may include deeper modeling, stronger leadership in
documentation, or a more advanced final analysis. Specific expectations will be
set by arrangement with the instructor.

<!-- TBD: clarify whether Phys 169 has any formal additional written requirement. -->

<!-- ## Historical Note

Earlier versions of this course used LabVIEW and MATLAB for thermal-control
instrumentation. The Fall 2026 version shifts the software center of gravity to
Python, Arduino, Git/GitHub, VS Code, and AI-assisted development while keeping
the same experimental spirit: build the instrument, understand the signal, close
the loop, and compare the behavior to a physical model. -->
