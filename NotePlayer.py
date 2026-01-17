import time

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
    "1/4": 0.25,
    "1/8": 0.125,
    "2": 2.0,
    "3": 3.0,
    "4": 4.0
}

MELODY = [
    ("C4", "1/4"),
    ("E4", "1/4"),
    ("G4", "1/4"),
    ("C5", "1/1"),
    ("", "1/2"),
    ("A3", "1/8")
]

SUSTAIN = 0.75 # How much of the note duration is actually played

BPM = 120

BUZZER = "put the BUZZER here"


# ---------------- BUZZER + MUSIC ---------------- #

def play_tone(frequency, duration_seconds):
    if frequency == 0:
        # Rest
        BUZZER.duty_cycle = 0
        time.sleep(duration_seconds)
        return
    
    duration_played = duration_seconds * SUSTAIN
    
    BUZZER.frequency = frequency
    BUZZER.duty_cycle = 0.5
    time.sleep(duration_played)

    BUZZER.duty_cycle = 0
    time.sleep(duration_seconds - duration_played)

def note_to_frequency(note):
    if note == "" or note is None:
        return 0

    pitch = note[:-1]
    octave = int(note[-1])

    base_freq = BASE_FREQUENCIES[pitch]
    octave_shift = octave - 4
    return base_freq * (2 ** octave_shift)

def play_melody():
    seconds_per_beat = 60.0 / BPM

    for note_name, duration_key in MELODY:
        frequency = note_to_frequency(note_name)
        duration_beats = NOTE_DURATIONS[duration_key]
        duration_seconds = duration_beats * seconds_per_beat

        play_tone(frequency, duration_seconds)

# ---------------- RUN ---------------- #
play_melody()