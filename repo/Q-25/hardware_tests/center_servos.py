import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

hipYawServos = [0, 4, 8, 12]
hipPitchServos = [1, 5, 9, 13]
kneeServos = [2, 6, 10, 14]

print("Centering servos...\n")
for servo in hipYawServos:
	kit.servo[servo].angle = 60
for servo in hipPitchServos:
	kit.servo[servo].angle = 60
for servo in kneeServos:
	kit.servo[servo].angle = 60
