# Lab 1 Assignment: First Contact With The Instrument

## Introductory Material

### Purpose

In the first class you will meet the temperature-control instrument that we will build toward during the semester. It uses an Arduino, a thermistor, a thermoelectric cooler, an H-bridge driver, a power supply, a heat exchanger, an oscilloscope, and laptop software.

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

### Safety Boundary For Lab 1

In Lab 1, the Arduino is powered by USB. The TEC power supply stays off.

You may inspect the TEC, H-bridge, heat exchanger, thermistor, and safety cutoff, but you will not power the TEC during the first lab. This is deliberate. The course begins by verifying the measurement and communication chain before applying actuator power.

## Pre-Class Assignment

### Before Class

Complete these steps before the first meeting.

1. Install the Arduino IDE on the laptop you plan to use in lab, if possible.
2. Bring a USB cable or adapter that can connect your laptop to an Arduino Uno.
3. Read this assignment and write down any question that feels basic or confusing.
4. Skim the vocabulary list below.

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

## In-Class Assignment

### What You Will Do

You will:

- Identify the instrument's sensor, actuator, controller, power stage, thermal load, and safety cutoff.
- Upload Arduino sketches from the Arduino IDE.
- Open Serial Monitor and read heartbeat messages from the Arduino.
- Probe an Arduino digital output with an oscilloscope.
- Measure voltage levels and timing.
- Compare the measured signal to the code that generated it.

### Programming Task

In class, 

- Launch Arduino IDE
- From the examples section, run Blink.ino

<img src="figures/ArduinoExample.png" alt="Arduino examples" width="400">

- Change the duty cycle from the default 1:1 to 10:1 and to 1:10. Did it work?
- Now run another example, AnalogReadSerial.ino
- Wire up the trim-pot as instructed. View the results on the Serial Monitor and Serial Plotter. Slow down the time intervals between measurements to something sensible. Rotate the trim plot and see if the graphical plot makes sense. What range of voltage do you input into the analog pin from the trim-pot? What range of numbers does the Arduino analog read report back to you as you vary voltage? 

- sets one digital output pin as an output,
- turns that pin HIGH and LOW repeatedly,
- also drives the built-in LED,
- prints a heartbeat message to Serial Monitor at `9600` baud,
- lets you predict the period and frequency of the signal before measuring it.

You should expect to revise the sketch after the first upload. Debugging board selection, port selection, baud rate, and timing is part of the lab.

## Post-Class Assignment

### What To Submit

Submit a short lab note containing:

- A labeled photo or sketch of the apparatus.
- The Arduino board and serial port you used.
- The Arduino sketch you wrote.
- Three lines copied from Serial Monitor.
- An oscilloscope screenshot or hand sketch of the waveform.
- A small table with `V_low`, `V_high`, period, and frequency.
- A paragraph answering: What did the oscilloscope show that the Serial Monitor did not?
