import time
from adafruit_servokit import ServoKit
import threading

kit = ServoKit(channels=16)
INTERVAL = 10

class Servo:
	def __init__(self, number):
		self.number = number
		self.curAngle = 60

	def moveToAngle(self, newAngle):
		print(f"Moving servo {self.number} to angle {newAngle}")
		while self.curAngle != newAngle:
			print(f"Current angle: {self.curAngle}")
			if self.curAngle < newAngle:
				self.curAngle = min(self.curAngle + INTERVAL, newAngle)
			else:
				self.curAngle = max(self.curAngle - INTERVAL, newAngle)
			kit.servo[self.number].angle = self.curAngle
			time.sleep(0.1)

	def moveToAngleAsync(self, newAngle):
		thread = threading.Thread(
			target = self.moveToAngle,
			args=(newAngle)
		)
		thread.start()
		return thread

servo1 = Servo(1)
servo2 = Servo(2)
servo5 = Servo(5)
servo6 = Servo(6)
servo9 = Servo(9)
servo10 = Servo(10)
servo13 = Servo(13)
servo14 = Servo(14)

print("Centering legs...")
hipYawServos = [0, 4, 8, 12]
for servo in hipYawServos:
	kit.servo[servo].angle = 60

kit.servo[1].angle = 60
kit.servo[2].angle = 60
kit.servo[5].angle = 60
kit.servo[6].angle = 60
kit.servo[9].angle = 60
kit.servo[10].angle = 60
kit.servo[13].angle = 60
kit.servo[14].angle = 60

time.sleep(0.18)

print("Assuming default standing position.")

print("Phase 1 -- tucking legs")
## pitch
servo1.moveToAngle(20)
servo5.moveToAngle(90)
servo9.moveToAngle(20)
servo13.moveToAngle(90)
## knee
servo2.moveToAngle(110)
servo6.moveToAngle(10)
servo10.moveToAngle(110)
servo14.moveToAngle(10)

print("Phase 2 -- pushing into ground")
## pitch
servo1.moveToAngle(100)
servo5.moveToAngle(20)
servo9.moveToAngle(100)
servo13.moveToAngle(25)
## knee -- lifting as high as possible
servo2.moveToAngle(60)
servo6.moveToAngle(70)
servo10.moveToAngle(60)
servo14.moveToAngle(70)

servo1.moveToAngle(110)
servo5.moveToAngle(15)
servo9.moveToAngle(110)
servo13.moveToAngle(20)

input("Awaiting input to continue")

print("Phase 3 -- retucking and putting foot down")

servo9.moveToAngle(80)
servo1.moveToAngle(20)
servo2.moveToAngle(110)
servo1.moveToAngle(80)
servo9.moveToAngle(110)

servo1.moveToAngle(50)
servo9.moveToAngle(20)
servo10.moveToAngle(110)
servo9.moveToAngle(80)
servo1.moveToAngle(80)

servo13.moveToAngle(50)
servo5.moveToAngle(85)
servo6.moveToAngle(20)
servo5.moveToAngle(20)
servo13.moveToAngle(20)

servo5.moveToAngle(50)
servo13.moveToAngle(80)
servo14.moveToAngle(20)
servo13.moveToAngle(20)
servo5.moveToAngle(20)

#input()


## knee -- lifting as high as possible
#for i in range(9):
	#kit.servo[2].angle = 110 - (i * 5)
	#kit.servo[6].angle = 10 + (i * 5)
	#kit.servo[10].angle = 110 - (i * 5)
	#kit.servo[14].angle = 10 + (i * 5)
	#time.sleep(0.1)
#time.sleep(0.18)

# Final standing position
### pitch
#kit.servo[1].angle = 80
#kit.servo[5].angle = 40
#kit.servo[9].angle = 80
#kit.servo[13].angle = 45
### knee
#kit.servo[2].angle = 110
#kit.servo[6].angle = 10
#kit.servo[10].angle = 110
#kit.servo[14].angle = 10
