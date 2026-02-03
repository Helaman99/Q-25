import sys
import time
from gpiozero import PWMOutputDevice
from mido import MidiFile

BUZZER = PWMOutputDevice(18)

def midi_to_freq(note):
    return 440.0 * (2 ** ((note - 69) / 12))

def play_midi(filename, volume=0.5):
    mid = MidiFile(filename)

    for msg in mid.play():
        if msg.type == 'note_on' and msg.velocity > 0:
            freq = midi_to_freq(msg.note)
            BUZZER.frequency = freq
            BUZZER.value = volume
        elif msg.type in ('note_off', 'note_on') and msg.velocity == 0:
            BUZZER.value = 0

    BUZZER.value = 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python play_midi.py <file.mid> [volume]")
        sys.exit(1)

    filename = sys.argv[1]
    volume = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    play_midi(filename, volume)

