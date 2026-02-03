import sys
import time
from gpiozero import PWMOutputDevice
from mido import MidiFile

BUZZER = PWMOutputDevice(18)

def midi_to_freq(note):
    return 440.0 * (2 ** ((note - 69) / 12))

def play_midi(filename):
    mid = MidiFile(filename)

    # Mido handles tempo and timing internally when using .play()
    for msg in mid.play():
        if msg.type == 'note_on' and msg.velocity > 0:
            freq = midi_to_freq(msg.note)
            BUZZER.frequency = freq
            BUZZER.value = 0.5
        elif msg.type in ('note_off', 'note_on') and msg.velocity == 0:
            BUZZER.value = 0

    BUZZER.value = 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python play_midi.py <file.mid>")
        sys.exit(1)

    play_midi(sys.argv[1])
