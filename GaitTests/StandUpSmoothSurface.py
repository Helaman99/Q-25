import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

hipYawServos = [0, 4, 8, 12]
hipPitchServos = [1, 5, 9, 13]
kneeServos = [2, 6, 10, 14]

for servo in hipYawServos:
	kit.servo[servo].angle = 60

time.sleep(0.18)

print("Assuming default standing position.\n")

# Phase 1 -- tucking legs
## pitch
kit.servo[1].angle = 20
kit.servo[5].angle = 90
kit.servo[9].angle = 20
kit.servo[13].angle = 90
## knee
kit.servo[2].angle = 110
kit.servo[6].angle = 10
kit.servo[10].angle = 110
kit.servo[14].angle = 10
time.sleep(0.18)

# Phase 2 -- pushing into ground
kit.servo[1].angle = 100
kit.servo[5].angle = 20
kit.servo[9].angle = 100
kit.servo[13].angle = 25
time.sleep(0.45)
kit.servo[1].angle = 80
kit.servo[5].angle = 40
kit.servo[9].angle = 80
kit.servo[13].angle = 45
