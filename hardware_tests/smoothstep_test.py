import sys
import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
servo = int(sys.argv[1])
start = int(sys.argv[2])
cur_angle = start
end = int(sys.argv[3])
step_count = int(sys.argv[4])

def get_steps():
    steps = []
    for i in range (step_count + 1):
        t = i / step_count
        steps.append(int(start + (end - start) * (6*t**5 - 15*t**4 + 10*t**3))) #quintic
	#steps.append(int(start + (end - start) * (3 * t**2 - 2 * t**3))) #cubic
    return steps

steps = get_steps()

for step in steps:
    kit.servo[servo].angle = step
    #print("Step angle: " + str(step))
    #time.sleep(round(abs(cur_angle - step)/60 * 0.17, 4))
    #print("Sleep time: " + str(round(abs(cur_angle - step)/60 * 0.17, 4)) + " \n")
    cur_angle = step
