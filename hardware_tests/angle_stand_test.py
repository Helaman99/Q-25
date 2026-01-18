import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

# Servo nomenclature
# 0 = Hip yaw servo
# 1 = Hip pitch servo
# 2 = Knee servo
# 3 = Unused

hipYawServos = [0, 4, 8, 12]
hipPitchServos = [1, 5, 9, 13]
kneeServos = [2, 6, 10, 14]

print("Testing leg angles to stand tall!\n")

print("Centering hip yaw...\n")
for servo in hipYawServos:
	kit.servo[servo].angle = 60

time.sleep(0.18)

print("Standing Up!\n")

# Phase one -- getting off the ground
## tucking legs
### pitch
kit.servo[1].angle = 20
kit.servo[5].angle = 90
kit.servo[9].angle = 20
kit.servo[13].angle = 90
### knee
kit.servo[2].angle = 110
kit.servo[6].angle = 10
kit.servo[10].angle = 110
kit.servo[14].angle = 10
time.sleep(0.18)

## pushing into ground
### pitch
kit.servo[1].angle = 100
kit.servo[5].angle = 20
kit.servo[9].angle = 100
kit.servo[13].angle = 25
### knee -- Without the knee also pushing, robot won't stand without max torque
kit.servo[2].angle = 70
kit.servo[6].angle = 50
kit.servo[10].angle = 70
kit.servo[14].angle = 50
#time.sleep(1)

# Second phase to stand all the way up
# Only really works with max torque
#kit.servo[1].angle = 20
#kit.servo[2].angle = 110
#time.sleep(0.18)
#kit.servo[1].angle = 80
#time.sleep(0.18)

#kit.servo[9].angle = 20
#kit.servo[10].angle = 110
#time.sleep(0.18)
#kit.servo[9].angle = 80
#time.sleep(0.18)

#kit.servo[5].angle = 90
#kit.servo[6].angle = 10
#time.sleep(0.18)
#kit.servo[5].angle = 40
#time.sleep(0.18)

#kit.servo[13].angle = 90
#kit.servo[14].angle = 10
#time.sleep(0.18)
#kit.servo[13].angle = 45
#time.sleep(0.18)
