import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

class Leg:
	def __init__(self, number):
		self.number = number
		self.hipYaw = number * 4
		self.hipPitch = self.hipYaw + 1
		self.kneePitch = self.hipYaw + 2
		self.inversion = 0
		self.inFront = False

		if number % 2 != 0:
			self.inversion = 120
		if number == 0 or number == 3:
			self.inFront = True

	def MoveToPosition(self, position):
		match position:
			case 0: # Standing
				kit.servo[self.hipYaw].angle = 60
				kit.servo[self.hipPitch].angle = abs(self.inversion - 80)
				kit.servo[self.kneePitch].angle = abs(self.inversion - 110)
			case 1: # Lifted
				kit.servo[self.hipYaw].angle = 60
				kit.servo[self.hipPitch].angle = abs(self.inversion - 10)
				kit.servo[self.kneePitch].angle = abs(self.inversion - 110)
			case 2: # Stepping out
				kit.servo[self.hipYaw].angle = abs(self.inversion - 85)
				kit.servo[self.hipPitch].angle = abs(self.inversion - 110)
				kit.servo[self.kneePitch].angle = abs(self.inversion - 45)
			case 3: # Pulling in
				kit.servo[self.hipYaw].angle = abs(self.inversion - 56)
				kit.servo[self.hipPitch].angle = abs(self.inversion - 96)
				kit.servo[self.kneePitch].angle = abs(self.inversion - 66)
			case 4: # Pulling in
				kit.servo[self.hipYaw].angle = abs(self.inversion - 38)
				kit.servo[self.hipPitch].angle = abs(self.inversion - 83)
				kit.servo[self.kneePitch].angle = abs(self.inversion - 87)
			case 5: # Fully in
				kit.servo[self.hipYaw].angle = abs(self.inversion - 10)
				kit.servo[self.hipPitch].angle = abs(self.inversion - 70)
				kit.servo[self.kneePitch].angle = abs(self.inversion - 110)
			case _:
				print("Invalid phase sent to leg.")

	def CounterBalance(self):
		if self.inversion == 0:
			kit.servo[self.hipPitch].angle -= 20
		else:
			kit.servo[self.hipPitch].angle += 20
	def Rebalance(self):
		if self.inversion == 0:
			kit.servo[self.hipPitch].angle += 20
		else:
			kit.servo[self.hipPitch].angle -= 20

legOrder = [Leg(0), Leg(2), Leg(3), Leg(1)]

while (True):
	for curLeg in range(4):
		nextLeg = (curLeg + 1) % 4
		secondNextLeg = (curLeg + 2) % 4
		lastLeg = (curLeg + 3) % 4
		legOrder[nextLeg].CounterBalance()
		time.sleep(0.2)
		legOrder[curLeg].MoveToPosition(1)
		time.sleep(0.18)

		if legOrder[curLeg].inFront:
			legOrder[curLeg].MoveToPosition(2)
			legOrder[nextLeg].Rebalance()
		else:
			legOrder[curLeg].MoveToPosition(5)
			legOrder[nextLeg].Rebalance()

		if legOrder[nextLeg].inFront:
			legOrder[nextLeg].MoveToPosition(5)
		else:
			legOrder[nextLeg].MoveToPosition(2)

		if legOrder[secondNextLeg].inFront:
			legOrder[secondNextLeg].MoveToPosition(4)
		else:
			legOrder[secondNextLeg].MoveToPosition(3)

		if legOrder[lastLeg].inFront:
			legOrder[lastLeg].MoveToPosition(3)
		else:
			legOrder[lastLeg].MoveToPosition(4)
