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

LED_TRIGGER = "/sys/class/leds/led0/trigger"
LED_BRIGHTNESS = "/sys/class/leds/led0/brightness"


# ---------------- LED CONTROL ---------------- #

def save_and_disable_led_trigger():
    """Save current LED trigger and disable automatic control."""
    with open(LED_TRIGGER, "r") as f:
        current = f.read().strip()
    # Save it globally so we can restore later
    global ORIGINAL_TRIGGER
    ORIGINAL_TRIGGER = current

    # Disable automatic LED behavior
    with open(LED_TRIGGER, "w") as f:
        f.write("none")

def restore_led_trigger():
    """Restore the LED trigger to its original behavior."""
    with open(LED_TRIGGER, "w") as f:
        f.write(ORIGINAL_TRIGGER)

def led_on():
    with open(LED_BRIGHTNESS, "w") as f:
        f.write("1")

def led_off():
    with open(LED_BRIGHTNESS, "w") as f:
        f.write("0")


# ---------------- BUZZER + MUSIC ---------------- #

def play_tone(frequency, duration_seconds):
    if frequency == 0:
        # Rest
        BUZZER.duty_cycle = 0
        time.sleep(duration_seconds)
        return
    
    duration_played = duration_seconds * SUSTAIN

    led_on()
    
    BUZZER.frequency = frequency
    BUZZER.duty_cycle = 0.5
    time.sleep(duration_played)

    BUZZER.duty_cycle = 0
    led_off()
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

    save_and_disable_led_trigger()

    try:
        for note_name, duration_key in MELODY:
            frequency = note_to_frequency(note_name)
            duration_beats = NOTE_DURATIONS[duration_key]
            duration_seconds = duration_beats * seconds_per_beat

            play_tone(frequency, duration_seconds)
    finally:
        led_off()
        restore_led_trigger()

# ---------------- RUN ---------------- #
play_melody()