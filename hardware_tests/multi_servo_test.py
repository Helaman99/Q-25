import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

hip_yaw_servos = [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14]

for servo in hip_yaw_servos:
	kit.servo[servo].angle = 0

time.sleep(0.4)

for servo in hip_yaw_servos:
	kit.servo[servo].angle = 120

time.sleep(0.4)

for servo in hip_yaw_servos:
	kit.servo[servo].angle = 60
