import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

hipYawServos = [0, 4, 8, 12]
hipPitchServos = [1, 5, 9, 13]
kneeServos = [2, 6, 10, 14]

print("Assuming standing position...\n")
for servo in hipYawServos:
	kit.servo[servo].angle = 60
print("Walking.\n")

# pitch back opposite leg, lift current leg
kit.servo[9].angle -= 20
time.sleep(0.2)
kit.servo[1].angle = 10
kit.servo[0].angle = 100
time.sleep(0.18)
kit.servo[1].angle = 80
kit.servo[9].angle += 20
