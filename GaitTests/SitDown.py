import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

print("Sitting down.\n")

# Knee pitch when standing straight
#kit.servo[1].angle = 80
#kit.servo[5].angle = 40
#kit.servo[9].angle = 80
#kit.servo[13].angle = 45

for i in range(10):
	kit.servo[1].angle -= 5
	kit.servo[5].angle += 5
	kit.servo[9].angle -= 5
	kit.servo[13].angle += 5
	time.sleep(0.2)
