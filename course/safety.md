# Laboratory Safety

## General Boundary

Measurement circuits powered only through Arduino USB are introduced before
the TEC power stage. Do not connect or energize the H-bridge, TEC, or external
power supply unless the assignment and instructor explicitly call for it.

## Before Applying TEC Power

- Verify Arduino PWM signals with an oscilloscope.
- Begin with PWM set to zero.
- Confirm common grounding and H-bridge wiring.
- Use a current-limited power supply.
- Confirm the hardware thermal cutoff is present.
- Increase PWM gradually while watching temperature.

