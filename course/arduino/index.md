# Arduino Reference

The hands-on Arduino exercises are part of the [Module 1
assignment](../labs/lab-01/index.md). This page is a compact reference to the
Arduino material used throughout the course.

The Arduino IDE includes permanent example sketches that are worth learning
because students can find them again after the course. Open them from:

```text
File -> Examples
```

Arduino also publishes [worked built-in
examples](https://docs.arduino.cc/built-in-examples/). Module 1 begins with
`Blink` and `AnalogReadSerial`.

## What The Arduino Does In This Course

The Arduino Uno is the small computer at the center of the first part of the
course. It reads voltages from sensors, communicates with the laptop over USB,
and produces digital or PWM control signals.

- Reads thermistor voltage-divider signals with analog inputs.
- Sends measurements to a laptop through USB serial communication.
- Produces digital timing signals for oscilloscope measurements.
- Produces PWM signals for actuator control.
- Implements safety logic and, later, feedback control.

## Course References

- [Analog, ADC, And PWM](analog-digital.md)
- [Arduino Uno pinout](pinout.md)
- [Module 1 assignment](../labs/lab-01/index.md)
- [Official Blink example](https://docs.arduino.cc/built-in-examples/basics/Blink/)
- [Official AnalogReadSerial example](https://docs.arduino.cc/built-in-examples/basics/AnalogReadSerial/)
- [Official Arduino Uno Rev3 page](https://docs.arduino.cc/hardware/uno-rev3/)
- [Pulse-width modulation background](https://en.wikipedia.org/wiki/Pulse-width_modulation)
