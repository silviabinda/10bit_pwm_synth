# ESP32-based sound instrument protoype
# made by Silvia Binda Heiserova during her studio residency at BEK May/June 2026

from machine import ADC, Pin, PWM
import time
import math
time.sleep(1)

SPEAKER_PIN = 25

POT_SPEED_PIN = 35
POT_DUTY_PIN = 34
POT_THIRD_PIN = 32

MODE_SWITCH_PIN = 33
BOOT_BUTTON_PIN = 0

speaker = PWM(Pin(SPEAKER_PIN))

pot_speed = ADC(Pin(POT_SPEED_PIN))
pot_speed.atten(ADC.ATTN_11DB)
pot_speed.width(ADC.WIDTH_12BIT)

pot_duty = ADC(Pin(POT_DUTY_PIN))
pot_duty.atten(ADC.ATTN_11DB)
pot_duty.width(ADC.WIDTH_12BIT)

pot_third = ADC(Pin(POT_THIRD_PIN))
pot_third.atten(ADC.ATTN_11DB)
pot_third.width(ADC.WIDTH_12BIT)

mode_switch = Pin(MODE_SWITCH_PIN, Pin.IN, Pin.PULL_UP)
boot_button = Pin(BOOT_BUTTON_PIN, Pin.IN, Pin.PULL_UP)

mode = 0
last_switch = 1
sound_enabled = False
last_boot = 1

phase_engine = 0.0
phase_heli = 0.0
melody_step = 0
sid_step = 0
broken_step = 0
false_step = 0

BASE_FREQ = 60

sid_patterns = [
    [1, 1, 1, 1],
    [1, 2, 1, 2],
    [1, 2, 4, 2],
    [0.5, 1, 2, 4],
]

broken_intervals = [
    [1.0, 1.06, 1.33],
    [1.0, 1.17, 1.41],
    [1.0, 1.25, 1.48],
    [1.0, 1.11, 1.37, 1.72],
]

false_melody = [
    220, 247, 262, 294,
    277, 247, 220, 196,
    208, 233, 247, 220,
    185, 196, 220, 247
]

C3=131; D3=147; E3=165; F3=175; G3=196; A3=220; B3=247
C4=262; D4=294; E4=330; F4=349; G4=392; A4=440; B4=494
C5=523

melodies = [
    [C4,E4,G4,E4,D4,F4,A4,F4],
    [E4,D4,C4,D4,E4,G4,E4,C4],
    [G3,C4,E4,G4,E4,C4,D4,G3],
    [A3,C4,E4,C4,G3,B3,D4,B3],
    [C4,D4,E4,G4,E4,D4,C4,G3],
    [G4,E4,D4,C4,D4,E4,C4,G3],
    [C4,G3,A3,C4,D4,F4,E4,C4],
    [E4,G4,A4,G4,E4,D4,C4,D4],
    [D4,F4,A4,F4,E4,G4,B4,G4],
    [C4,E4,D4,F4,E4,G4,F4,A4],

    [A3,E4,C4,E4,G3,D4,B3,D4],
    [C4,C4,G3,C4,E4,E4,D4,C4],
    [G3,B3,D4,G4,F4,D4,B3,G3],
    [F3,A3,C4,F4,E4,C4,A3,F3],
    [E3,G3,B3,E4,D4,B3,G3,E3],
    [C4,D4,F4,E4,C4,A3,G3,C4],
    [D4,E4,G4,A4,G4,E4,D4,C4],
    [G4,A4,G4,E4,C4,D4,E4,G4],
    [C4,E4,G4,C5,B4,G4,E4,C4],
    [A3,C4,D4,F4,E4,C4,A3,G3],

    [E4,F4,G4,E4,D4,E4,C4,D4],
    [C4,D4,E4,C4,G3,A3,C4,E4],
    [G3,A3,C4,D4,E4,D4,C4,A3],
    [F4,E4,D4,C4,D4,F4,A4,F4],
    [C4,E4,F4,G4,A4,G4,E4,C4],
    [D4,F4,E4,G4,F4,A4,G4,D4],
    [E4,G4,F4,A4,G4,B4,A4,E4],
    [C4,G4,E4,G4,D4,A4,F4,A4],
    [A3,C4,E4,G4,A4,G4,E4,C4],
    [B3,D4,F4,A4,G4,E4,D4,B3],

    [C4,E4,G4,A4,G4,E4,D4,C4],
    [D4,F4,A4,B4,A4,F4,E4,D4],
    [E4,G4,B4,C5,B4,G4,F4,E4],
    [G3,D4,G4,D4,E4,C4,D4,G3],
    [C4,A3,C4,E4,D4,G3,D4,F4],
    [F3,C4,F4,C4,G3,D4,G4,D4],
    [E3,B3,E4,B3,F3,C4,F4,C4],
    [C4,D4,G3,A3,C4,E4,D4,G3],
    [A3,B3,C4,E4,D4,C4,B3,A3],
    [G3,C4,D4,E4,G4,E4,D4,C4],

    [C4,E4,G4,E4,A4,G4,E4,C4],
    [D4,F4,A4,F4,B4,A4,F4,D4],
    [E4,G4,C5,G4,B4,G4,E4,C4],
    [C4,D4,E4,G4,A4,C5,A4,G4],
    [G3,C4,E4,D4,G3,B3,D4,C4],
    [A3,D4,F4,E4,A3,C4,E4,D4],
    [F3,A3,C4,E4,F4,E4,C4,A3],
    [C4,G3,C4,D4,E4,G4,E4,D4],
    [E4,C4,D4,G3,C4,E4,G4,C5],
    [C4,E4,D4,G4,E4,A4,G4,C5],
    [C4,G4,E4,C5,G4,E4,D4,C4],
]


def check_mode_switch():
    global mode, last_switch

    current_switch = mode_switch.value()

    if last_switch == 1 and current_switch == 0:
        mode = (mode + 1) % 6
        speaker.duty(0)
        time.sleep_ms(200)
        print("MODE:", mode)
        last_switch = current_switch
        return True

    last_switch = current_switch
    return False


def wait_ms_with_switch_check(duration):
    elapsed = 0

    while elapsed < duration:
        if check_mode_switch():
            return True

        time.sleep_ms(5)
        elapsed += 5

    return False


try:
    while True:

        check_mode_switch()

        current_boot = boot_button.value()

        if last_boot == 1 and current_boot == 0:
            sound_enabled = not sound_enabled
            speaker.duty(0)
            time.sleep_ms(250)
            print("SOUND:", sound_enabled)

        last_boot = current_boot

        if not sound_enabled:
            speaker.duty(0)
            time.sleep_ms(20)
            continue

        speed_val = pot_speed.read() >> 4
        duty_val = pot_duty.read() >> 4
        third_val = pot_third.read() >> 4

        if mode == 0:
        
            base_freq = 80 + int((speed_val / 255) * 420)
            duty = int(120 + (duty_val / 255) * 800)
            turbulence = int((third_val / 255) * 80)

            vibration = (
                math.sin(phase_engine * 11) * turbulence +
                math.sin(phase_engine * 17) * (turbulence * 0.4) +
                math.sin(phase_engine * 23) * (turbulence * 0.2)
            )

            frequency = base_freq + int(vibration)
            frequency = max(20, min(5000, frequency))

            speaker.freq(frequency)
            speaker.duty(duty)

            phase_engine += 0.05 + (speed_val / 255) * 0.25
            time.sleep_ms(8)

        elif mode == 1:
       
            speed = 0.08 + (speed_val / 255) * 0.8
            base_duty = int(120 + (duty_val / 255) * 700)
            intensity = third_val / 255

            rotor_fast = (math.sin(phase_heli) + 1) / 2
            rotor_slow = (math.sin(phase_heli * 0.23) + 1) / 2
            rotor = (rotor_fast * 0.75) + (rotor_slow * 0.25)

            moving_duty = int(base_duty * (1 - intensity + rotor * intensity))
            moving_duty = max(20, min(1023, moving_duty))

            wobble = int(math.sin(phase_heli * 0.5) * 3 * intensity)
            freq = BASE_FREQ + wobble

            speaker.freq(freq)
            speaker.duty(moving_duty)

            phase_heli += speed
            time.sleep_ms(10)

        elif mode == 2:
         
            melody_index = speed_val // 5
            if melody_index > 50:
                melody_index = 50

            melody = melodies[melody_index]

            pitch_mult = 0.5 + (duty_val / 255) * 1.5
            poly_amount = third_val / 255

            note = int(melody[melody_step] * pitch_mult)

            if third_val < 85:
                interval = 1.0
            elif third_val < 170:
                interval = 1.5
            else:
                interval = 2.0

            second_note = int(note * interval)

            if poly_amount < 0.1:
                speaker.freq(note)
                speaker.duty(512)
                time.sleep_ms(130)

            else:
                repeats = int(4 + poly_amount * 12)

                for i in range(repeats):
                    if check_mode_switch():
                        break

                    speaker.freq(note)
                    speaker.duty(512)
                    time.sleep_ms(6)

                    speaker.freq(second_note)
                    speaker.duty(512)
                    time.sleep_ms(6)

            speaker.duty(0)
            time.sleep_ms(35)

            melody_step += 1
            if melody_step >= 8:
                melody_step = 0

        elif mode == 3:

            base_freq = 220
            duty = 600

            step_delay = int(20 + (1.0 - speed_val / 255) * 180)

            pattern_index = duty_val // 64
            if pattern_index > 3:
                pattern_index = 3

            sid_pattern = sid_patterns[pattern_index]

            pulse_count = 1 + int((third_val / 255) * 3)

            octave = sid_pattern[sid_step % len(sid_pattern)]
            freq = int(base_freq * octave)

            for p in range(pulse_count):
                if check_mode_switch():
                    break

                speaker.freq(freq)
                speaker.duty(duty)
                time.sleep_ms(12)

                speaker.duty(0)
                time.sleep_ms(4)

            sid_step += 1

            if wait_ms_with_switch_check(step_delay):
                continue

        elif mode == 4:
            
            base_freq = int(70 + (speed_val / 255) * 260)

            chord_index = duty_val // 64
            if chord_index > 3:
                chord_index = 3

            chord = broken_intervals[chord_index]

            density = 1 + int((third_val / 255) * 5)
            note_gap = int(8 + (1.0 - third_val / 255) * 45)

            for i in range(density):
                if check_mode_switch():
                    break

                interval = chord[(broken_step + i) % len(chord)]
                detune = ((broken_step * 7 + i * 13) % 23) - 11

                freq = int(base_freq * interval) + detune
                freq = max(30, min(3000, freq))

                speaker.freq(freq)
                speaker.duty(520)

                time.sleep_ms(note_gap)

                speaker.duty(0)
                time.sleep_ms(6)

            broken_step += 1

            if broken_step > 9999:
                broken_step = 0

        else:
      
            base_index = false_step % len(false_melody)

            transpose = 0.75 + (speed_val / 255) * 1.5
            drift = int((duty_val / 255) * 18) - 9
            instability = third_val / 255

            note = int(false_melody[base_index] * transpose)

            false_offset = int(math.sin(false_step * 0.7) * 22 * instability)
            note = note + false_offset + drift
            note = max(60, min(2000, note))

            repeats = 1 + int(instability * 4)
            note_length = int(90 - instability * 55)

            for i in range(repeats):
                if check_mode_switch():
                    break

                shadow = int(note * (1.005 + instability * 0.025))

                speaker.freq(note)
                speaker.duty(460)
                time.sleep_ms(note_length)

                speaker.freq(shadow)
                speaker.duty(360)
                time.sleep_ms(8)

                speaker.duty(0)
                time.sleep_ms(18)

            false_step += 1

            if false_step > 9999:
                false_step = 0

except KeyboardInterrupt:
    speaker.duty(0)
    speaker.deinit()
    print("Synth stopped")
