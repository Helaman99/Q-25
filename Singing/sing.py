import json
import sys
from gpiozero import PWMOutputDevice
from time import sleep

BASE_FREQUENCIES = {
    "C": 261.63,
    "C#": 277.18,
    "D": 293.66,
    "D#": 311.13,
    "E": 329.63,
    "F": 349.23,
    "F#": 369.99,
    "G": 392.00,
    "G#": 415.30,
    "A": 440.00,
    "A#": 466.16,
    "B": 493.88,
}

NOTE_DURATIONS = {
    "1": 1.0,
    "1/2": 0.5,
    "3/4": 0.75,
    "1/4": 0.25,
    "1/8": 0.125,
    "2": 2.0,
    "3": 3.0,
    "4": 4.0
}

SUSTAIN = 0.75  # How much of the note duration is actually played

BUZZER = PWMOutputDevice(18)


# ---------------- BUZZER + MUSIC ---------------- #

def play_tone(frequency, duration_seconds):
    if frequency == 0:
        BUZZER.value = 0
        sleep(duration_seconds)
        return
    
    duration_played = duration_seconds * SUSTAIN
    
    BUZZER.frequency = frequency
    BUZZER.value = 0.5
    sleep(duration_played)

    BUZZER.value = 0
    sleep(duration_seconds - duration_played)


def note_to_frequency(note):
    if not note:
        return 0

    pitch = note[:-1]
    octave = int(note[-1])

    base_freq = BASE_FREQUENCIES[pitch]
    octave_shift = octave - 4
    return base_freq * (2 ** octave_shift)


def play_melody(melody, bpm):
    seconds_per_beat = 60.0 / bpm

    for note_name, duration_key in melody:
        frequency = note_to_frequency(note_name)
        duration_beats = NOTE_DURATIONS[duration_key]
        duration_seconds = duration_beats * seconds_per_beat

        play_tone(frequency, duration_seconds)


# ---------------- MAIN ---------------- #

def load_melody_from_json(path):
    with open(path, "r") as f:
        data = json.load(f)

    # Expecting: { "melody": [ ["A4","1"], ["F4","1/2"], ... ] }
    return data["melody"]

def load_bpm_from_json(path):
    with open(path, "r") as f:
        data = json.load(f)

    return data["bpm"]

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python play.py <song.json> OR python sing.py <song.json> <BPM>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        if len(sys.argv) == 2:
            bpm = load_bpm_from_json(json_path)
        else:
            bpm = int(sys.argv[2])

        melody = load_melody_from_json(json_path)
        print("Singing " + sys.argv[1])
        play_melody(melody, bpm)
    finally:
        BUZZER.close()
