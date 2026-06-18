# Arduino Overview

The Arduino Uno is the small computer at the center of the first part of the
course. It reads voltages from sensors, communicates with the laptop over USB,
and produces digital or PWM control signals.

## What It Does In This Course

- Reads thermistor voltage-divider signals with analog inputs.
- Sends measurements to a laptop through USB serial communication.
- Produces digital timing signals for oscilloscope measurements.
- Produces PWM signals for actuator control.
- Implements safety logic and, later, feedback control.

## Permanent Arduino Examples

The Arduino IDE includes carefully written example sketches. Open them using:

```text
File → Examples → 01.Basics
```

Useful early examples include:

- `Blink`
- `DigitalReadSerial`
- `AnalogReadSerial`
- `ReadAnalogVoltage`
- `Fade`

These examples are valuable because they remain available in the Arduino IDE
after the course ends.

Continue to the [Arduino Uno pinout](pinout.md).

