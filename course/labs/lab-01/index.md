# Module 1 Assignment: First Contact With The Instrument

## Introductory Material

### Purpose

In Module 1 you will meet the temperature-control instrument that we will build toward during the semester. It uses an Arduino, a thermistor, a thermoelectric cooler, an H-bridge driver, a power supply, a heat exchanger, an oscilloscope, and laptop software. If you haven't already, read the course<strong> </strong><a href="https://sethfraden.github.io/Phys39F26-course/">Overview</a>.

Before class, your job is to arrive ready to connect to an Arduino, upload a simple program, and think clearly about safety.

### Vocabulary

- **Arduino Uno**: the microcontroller board that reads voltages and sends control signals.
- **Serial Monitor**: the Arduino IDE window that shows text sent from the Arduino to the laptop.
- **Digital output**: a pin that the Arduino can set near 0 V or 5 V.
- **Oscilloscope**: an instrument that displays voltage versus time.
- **Thermistor**: a resistor whose resistance changes with temperature.
- **TEC/Peltier element**: a bidirectional thermal actuator. It can heat one side and cool the other depending on current direction.
- **H-bridge**: an electronic circuit that lets the low-power Arduino control the amount and direction of current from a high-power supply through a load.
- **PWM**: pulse-width modulation, a way to control average power using fast on/off switching.

### Safety Boundary For Module 1

In Module 1, the Arduino is powered by USB. The TEC power supply stays off.

You may inspect the TEC, H-bridge, heat exchanger, thermistor, and safety cutoff, but you will not power the TEC during Module 1. This is deliberate. The course begins by verifying the measurement and communication chain before applying actuator power.

## Pre-Class Assignment

### Before Class

Complete these steps before Module 1.

1. Install the Arduino IDE on the laptop you plan to use in lab, if possible.
2. Read this assignment and write down any question that feels basic or confusing.
3. Skim the vocabulary list below.

If you cannot install software before class, come anyway. We will handle setup in lab.

### Pre-Class Questions

Write short answers before class. These are not meant to be polished.

1. What is the difference between a sensor and an actuator?
2. Why should the TEC power supply remain off while we are only testing Arduino upload and serial communication?
3. What do you expect an Arduino digital output to look like on an oscilloscope?
4. If software says "toggle every 500 ms," what period and frequency would you expect to measure?

### Bring To Class

- Laptop, if you have one.
- Lab notebook or note-taking device.
- Questions.

### Outside-Class Workload Budget For S2

| Work | Planned time |
| --- | ---: |
| Read this module assignment | 20 minutes |
| Read the linked Arduino and hardware introductions | 35 minutes |
| Answer the pre-class questions | 20 minutes |
| Assemble and submit A1 after the in-class evidence is complete | 30 minutes |
| **Total outside class associated with S2** | **1 hour 45 minutes** |

The four-hour course limit is a maximum, not a target. Ask for help rather than
silently exceeding it because of installation or access problems.

## In-Class Assignment

### What You Will Do

You will:

- Identify the instrument's sensor, actuator, controller, power stage, thermal load, and safety cutoff.
- Upload Arduino sketches from the Arduino IDE.
- Open Serial Monitor and read heartbeat messages from the Arduino.
- Probe an Arduino digital output with an oscilloscope.
- Measure voltage levels, timing, and PWM duty cycle.
- Read a potentiometer voltage with `analogRead`.
- Average analog readings and use the averaged value to control LED brightness.
- Compare the measured signals to the code that generated them.

### Programming Task 

- (5-10 mins) Read the introduction to <a href="https://docs.arduino.cc/learn/starting-guide/whats-arduino?queryID=b6c1b642087e54fac19b7471a69050cb&_gl=1*iny9um*_ga*MTQ1Nzk0MDE2MS4xNjg0ODU0NzQ5*_ga_NEXN8H46L5*MTY4NTIxODMyOC40LjAuMTY4NTIxODMyOC4wLjAuMA..">arduino</a>. 

- (5-10 mins) Read the section on <a href="https://sethfraden.github.io/Phys39F26-course/hardware/">Hardware for temperature control</a> (there are no exercises here). It contains a description of the setup with links to details about the components.  

- (120 mins) The bulk of Module 1 is next. Do the <a href="https://sethfraden.github.io/Phys39F26-course/arduino/">intro to arduino assignment</a>. </p> It consists of the following steps:
<ol>
  <li>Run the official Blink sketch using the built-in LED and then an external LED with a current-limiting resistor.</li>
  <li>Modify Blink so the duty cycle is 1:1, 10:1, and 1:10. Measure the digital output with the oscilloscope.</li>
  <li>Run the official AnalogReadSerial sketch with a potentiometer wired as a 0-5 V voltage divider. View the result in Serial Monitor and Serial Plotter.</li>
  <li>Modify the analog-reading sketch so it averages 1000 readings before printing. Compare the averaged readings with the unaveraged readings.</li>
  <li>Modify the averaged analog-reading sketch into an LED-brightness sketch: potentiometer voltage to averaged analog number to PWM output to LED brightness. Measure the PWM output with the oscilloscope.</li>
</ol>

### Collect Your A1 Evidence During Class

The post-class assignment is designed to take no more than **30 minutes**. To
make that possible, collect and save all measurements, code, and images while
you still have the Arduino and oscilloscope in front of you.

Before leaving class, complete this checklist. If an item cannot be completed,
show the instructor what is missing before you leave.

- [ ] Save a labeled photograph or quick sketch of the apparatus.
- [ ] Record the Arduino board model and serial-port name.
- [ ] Save the exact modified Blink, averaged analog-reading, and
  LED-brightness sketches used for the measurements.
- [ ] Copy three representative labeled lines from Serial Monitor.
- [ ] Save evidence comparing the unaveraged and 1000-reading averaged analog
  signal, such as a Serial Plotter screenshot or a short numerical record.
- [ ] Save an oscilloscope screenshot or clear hand sketch of a Blink waveform.
- [ ] Save an oscilloscope screenshot or clear hand sketch of the LED PWM
  waveform.
- [ ] Fill in the measurement table below using oscilloscope measurements, not
  ideal values copied from the code.
- [ ] Write two or three bullet points about what the oscilloscope revealed that
  the serial displays did not.

| Signal measured | Arduino setting | Expected duty cycle | $V_{\mathrm{low}}$ | $V_{\mathrm{high}}$ | Measured period $T$ | Frequency $f$ | Measured duty cycle |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Blink | HIGH:LOW = 1:1 | 50.0% |  |  |  |  |  |
| Blink | HIGH:LOW = 10:1 | 90.9% |  |  |  |  |  |
| Blink | HIGH:LOW = 1:10 | 9.1% |  |  |  |  |  |
| LED PWM | `analogWrite = ___` |  |  |  |  |  |  |

Include units with every measured quantity. Calculate

$$
f=\frac{1}{T},
\qquad
D=100\%\frac{t_{\mathrm{HIGH}}}{T}.
$$

For Arduino PWM, the expected duty cycle is approximately

$$
D_{\mathrm{expected}}=100\%\frac{\texttt{analogWrite value}}{255}.
$$

The H-bridge and TEC remain inspection-only today. We will use the H-bridge in
a later actuator module after everyone has measured PWM directly and can explain
what `analogWrite` is doing.

 <!-- In class,

- Launch Arduino IDE
- From the examples section, run Blink.ino

<img src="figures/ArduinoExample.png" alt="Arduino examples" width="400">

- Change the duty cycle from the default 1:1 to 10:1 and to 1:10. Did it work?
- Now run another example, AnalogReadSerial.ino
- Wire up the trim pot as instructed. View the results on the Serial Monitor and Serial Plotter. Slow down the time intervals between measurements to something sensible. Rotate the trim pot and see if the graphical plot makes sense. What range of voltage do you input into the analog pin from the trim pot? What range of numbers does the Arduino analog read report back to you as you vary voltage?
- Add averaging to the analog-reading sketch.
- Use the averaged analog reading to set PWM on an LED.
- Measure the PWM output with the oscilloscope and compare the waveform to the LED brightness.

You should expect to revise the sketch after the first upload. Debugging board selection, port selection, baud rate, and timing is part of the lab. -->


## Post-Class Assignment

### A1: Module 1 Evidence Note

- **Assessment code:** `A1`, graded team assignment, 5 points
- **Due:** before Session S3, Wednesday, September 2, at **9:05 AM**
- **Repository file:** `docs/module_notes/module_01_evidence.md`
- **Moodle submission:** `A1_Lastname_Lastname.pdf`
- **Expected post-class time:** no more than **30 minutes**, provided the
  in-class evidence checklist is complete

`A1` assesses the scientific and technical evidence from Module 1. It is
separate from [`C1`, the development-environment and repository
milestone](../../assessment.md#c1-development-environment-and-repository),
which you will demonstrate during S3.

### Assemble And Submit The Note

After class:

1. Put the evidence gathered in class into
   `docs/module_notes/module_01_evidence.md`.
2. Add links to the exact repository files for the modified Blink, averaged
   analog-reading, and LED-brightness sketches. Do not paste pages of Arduino
   code into the note.
3. Complete the table above and write a three-to-five-sentence answer to the
   comparison question below.
4. Commit the note, sketches, and evidence; push the Git checkpoint (`GC`) to
   GitHub.
5. Export the note as `A1_Lastname_Lastname.pdf`. Put the team members,
   repository URL, and full commit hash on the first page, then submit the PDF
   to the [`A1` Moodle activity](https://moodle.brandeis.edu/course/view.php?id=6589)
   before the deadline.

Your note must contain:

- the labeled apparatus photograph or sketch,
- the Arduino board and serial port,
- links to the three exact Arduino sketches used,
- three representative labeled Serial Monitor lines,
- the brief unaveraged-versus-averaged comparison,
- the Blink and LED-PWM oscilloscope images or hand sketches,
- the completed measurement table, with units, and
- a three-to-five-sentence answer to: **What did the oscilloscope show that the
  Serial Monitor and Serial Plotter did not?**

Your answer should distinguish a direct electrical measurement from values
chosen and printed by software. Discuss the actual high and low voltages,
individual pulses, period, frequency, and duty cycle. The Serial Monitor shows
printed numbers, while the Serial Plotter graphs those samples against serial
sample order; neither display shows the individual fast PWM pulses when the
program prints only a summary value.

### Thirty-Minute Time Budget

| Task | Target time |
| --- | ---: |
| Organize the in-class evidence and add code links | 5 minutes |
| Finish the measurement table | 10 minutes |
| Write the comparison answer | 5 minutes |
| Check the note, commit, push, export, and submit | 10 minutes |

### A1 Rubric

| Criterion | Points |
| --- | ---: |
| Exact code links and labeled serial/averaging evidence are complete | 1 |
| Oscilloscope evidence and measurement table are complete, dimensional, and credible | 2 |
| The comparison correctly distinguishes the measured waveform from serial output | 1 |
| The PDF is clear, cites the pushed `GC`, and is submitted by the deadline | 1 |
