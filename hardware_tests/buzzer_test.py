from gpiozero import PWMOutputDevice
from time import sleep

buzzer = PWMOutputDevice(18)

tonesHz = [200, 300, 400, 500, 600, 700, 800]

for tone in tonesHz:
	buzzer.frequency = tone
	buzzer.value = 0.5  # duty cycle
	sleep(0.2)

for i in range(50):
	buzzer.frequency = 300
	buzzer.value = 0.5
	sleep(0.01)
	buzzer.frequency = 200
	buzzer.value = 0.5
	sleep(0.01)

for i in range(50):
	buzzer.frequency = 200
	buzzer.value = 0.5
	sleep(0.01)
	buzzer.frequency = 100
	buzzer.value = 0.5
	sleep(0.01)

for i in range(50):
	buzzer.frequency = 400
	buzzer.value = 0.5
	sleep(0.01)
	buzzer.frequency = 300
	buzzer.value = 0.5
	sleep(0.01)


buzzer.off()
