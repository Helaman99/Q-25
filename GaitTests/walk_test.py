import time
from adafruit_servokit import ServoKit
import threading

kit = ServoKit(channels=16)

class Joint:
	def __init__(self, servoNum):
		self.servoNum = servoNum
		self.curAngle = 60
		kit.servo[self.servoNum].angle = 60
		self.logging = False

	def MoveToAngle(self, newAngle, steps=30, delay=0.03):
		if self.logging:
			print(f"Moving servo {self.servoNum} from {self.curAngle} degrees to {newAngle} degrees")

		startAngle = self.curAngle

		for i in range(1, steps + 1):
			t = i / steps

			t_eased = 2 * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 2 / 2

			intermediateAngle = startAngle + (newAngle - startAngle) * t_eased
			if intermediateAngle < 0 or intermediateAngle > 120:
				print(f"Incorrect angle given to servo {self.servoNum}: {intermediateAngle}")
				Exit()

			kit.servo[self.servoNum].angle = intermediateAngle
			self.curAngle = intermediateAngle
			time.sleep(delay)

			if self.logging:
				print(f"Step {i}: {intermediateAngle}")

		# Ensure we land exactly on the target
		kit.servo[self.servoNum].angle = newAngle
		self.curAngle = newAngle

class Leg:
	def __init__(self, number):
		self.number = number
		self.hipYaw = Joint(number * 4)
		self.hipPitch = Joint(self.hipYaw.servoNum + 1)
		self.kneePitch = Joint(self.hipYaw.servoNum + 2)
		self.inversion = 0
		self.inFront = False
		self.curPosition = None
		self.logging = True

		if number % 2 != 0:
			self.inversion = 120
		if number == 0 or number == 3:
			self.inFront = True

	def MoveToPosition(self, position):
		if self.logging:
			print(f"Moving leg {self.number} to position {position}")
		match position:
			case 0: # Standing
				self.hipYaw.MoveToAngle(60)
				self.hipPitch.MoveToAngle(abs(self.inversion - 80))
				self.kneePitch.MoveToAngle(abs(self.inversion - 110))
			case 1: # Lifted
				self.hipPitch.MoveToAngle(abs(self.inversion - 20))
				#self.kneePitch.MoveToAngle(abs(self.inversion - 110))
			case 2: # Stepping out
				self.hipYaw.MoveToAngle(abs(self.inversion - 85))
				self.hipPitch.MoveToAngle(abs(self.inversion - 80))
				#self.kneePitch.MoveToAngle(abs(self.inversion - 110))
			case 3: # Pulling in
				self.hipYaw.MoveToAngle(abs(self.inversion - 64))
				self.hipPitch.MoveToAngle(abs(self.inversion - 80))
				#self.kneePitch.MoveToAngle(abs(self.inversion - 110))
			case 4: # Pulling in
				self.hipYaw.MoveToAngle(abs(self.inversion - 46))
				self.hipPitch.MoveToAngle(abs(self.inversion - 80))
				#self.kneePitch.MoveToAngle(abs(self.inversion - 110))
			case 5: # Pulling in
				self.hipYaw.MoveToAngle(abs(self.inversion - 28))
				self.hipPitch.MoveToAngle(abs(self.inversion - 80))
				#self.kneePitch.MoveToAngle(abs(self.inversion - 110))
			case 6: # Fully in
				self.hipYaw.MoveToAngle(abs(self.inversion - 10))
				self.hipPitch.MoveToAngle(abs(self.inversion - 80))
				#self.kneePitch.MoveToAngle(abs(self.inversion - 110))
			case _:
				print("Invalid phase sent to leg.")
		self.curPosition = position

	def MoveToNextPosition(self):
		if self.curPosition == 0:
			print("No next position from the default standing position.")
		elif self.curPosition == 6 and self.inFront:
			self.MoveToPosition(1)
		elif self.curPosition == 1 and not self.inFront:
			self.MoveToPosition(6)
		else:
			if self.inFront: self.MoveToPosition(self.curPosition + 1)
			else: self.MoveToPosition(self.curPosition - 1)

	def CounterBalance(self):
		if self.logging:
			print(f"Counterbalancing with leg {self.number}")
		if self.inversion == 0:
			kit.servo[self.hipPitch.servoNum].angle -= 10
		else:
			kit.servo[self.hipPitch.servoNum].angle += 10
	def Rebalance(self):
		if self.logging:
			print(f"Rebalancing leg {self.number}")
		if self.inversion == 0:
			kit.servo[self.hipPitch.servoNum].angle += 10
		else:
			kit.servo[self.hipPitch.servoNum].angle -= 10

legOrder = [Leg(0), Leg(2), Leg(3), Leg(1)]
prevLegOpposite = False # Every other iteration, the leg that needs to be counterbalanced is the one before the current leg

for leg in legOrder:
	leg.MoveToPosition(0)

while (True):
	for curLeg in range(4):
		input("Press any key to continue.\n");
		if prevLegOpposite:
			nextLeg = (curLeg + 3) % 4
			prevLegOpposite = False
			lastLeg = (curLeg + 1) % 4
		else:
			nextLeg = (curLeg + 1) % 4
			prevLegOpposite = True
			lastLeg = (curLeg + 3) % 4
		secondNextLeg = (curLeg + 2) % 4
		print(f"prevLegOpposite = {prevLegOpposite}")

		legOrder[nextLeg].CounterBalance()
		time.sleep(0.2)
		legOrder[curLeg].MoveToPosition(1)
		time.sleep(0.18)

		legOrder[curLeg].MoveToNextPosition()
		legOrder[nextLeg].Rebalance()

		threads = []

		for leg in [curLeg, nextLeg, secondNextLeg, lastLeg]:
			t = threading.Thread(
				target=legOrder[leg].MoveToNextPosition
			)
			t.start()
			threads.append(t)

		for t in threads:
			t.join()

