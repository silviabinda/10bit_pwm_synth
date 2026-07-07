# 10-bit PWM
A project on how to build a 10-bit synthesizer with ESP32, which was developed during studio residency at BEK (https://bek.no/en/) in May / June 2026.

<img width="3213" height="3445" alt="10-bit_pwm_prototype_1" src="https://github.com/user-attachments/assets/f17bf164-35d8-4f2b-9b66-d63433490cbe" />


About the synth:
10-bit PWM is a custom-build open source ESP32-based PWM programmable synthesizer with analog potentiometer controls and software-defined sound engines.

Technical specs:
- Platform: ESP32 
- Programming Environment: MicroPython
- Audio Output: 3.5 mm stereo jack
- Channel Configuration: Dual mono (L = R)
- Controls: Analog potentiometers, Push buttons
- External DAC: not required
- Synthesis: PWM pulse wave / square wave synthesis
- PWM resolution: 10-bit (0 - 1023 duty control)
- Control resolution: 8-bit parameter mapping (0 - 255)
- Sound engines: software-defined, selectable by button

