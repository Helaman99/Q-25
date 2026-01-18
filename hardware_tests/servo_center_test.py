import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

# Servo nomenclature
# 0 = Hip yaw servo
# 1 = Hip pitch servo
# 2 = Knee servo
# 3 = Unused

print("Testing servos between 0 and 120 degrees...\n")

for i in range(4):
    print(f"\nTesting leg {i}...")

    servoNum = i * 4

    print("Testing hip yaw servo...")
    kit.servo[servoNum].angle = 0
    time.sleep(0.4)
    kit.servo[servoNum].angle = 120
    time.sleep(0.4)
    kit.servo[servoNum].angle = 60
    time.sleep(0.4)

    print("Testing hip pitch servo...")
    kit.servo[servoNum + 1].angle = 0
    time.sleep(0.4)
    kit.servo[servoNum + 1].angle = 120
    time.sleep(0.4)
    kit.servo[servoNum + 1].angle = 60
    time.sleep(0.4)

    print("Testing knee servo...")
    kit.servo[servoNum + 2].angle = 0
    time.sleep(0.4)
    kit.servo[servoNum + 2].angle = 120
    time.sleep(0.4)
    kit.servo[servoNum + 2].angle = 60
    time.sleep(0.4)

    #print("Testing unknown servo...")
    #kit.servo[servoNum + 3].angle = 0
    #time.sleep(0.4)
    #kit.servo[servoNum + 3].angle = 120
    #time.sleep(0.4)
    #kit.servo[servoNum + 3].angle = 60
    #time.sleep(0.4)
