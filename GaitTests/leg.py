import time
from adafruit_servokit import ServoKit
import threading

kit = ServoKit(channels=16)

class Joint:
	def __init__(self, servoNum):
		self.servoNum = servoNum
		self.curAngle = kit.servo[self.servoNum].angle
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

		jointThreads = []
		match position:
			case 0:  # Standing
				jointThreads += [
					threading.Thread(target=self.hipYaw.MoveToAngle, args=(60,)),
					threading.Thread(target=self.hipPitch.MoveToAngle, args=(abs(self.inversion - 80),)),
					threading.Thread(target=self.kneePitch.MoveToAngle, args=(abs(self.inversion - 110),))
				]
			case 1:  # Lifted
				jointThreads += [
					threading.Thread(target=self.hipPitch.MoveToAngle, args=(abs(self.inversion - 20),)),
					threading.Thread(target=self.kneePitch.MoveToAngle, args=(abs(self.inversion - 110),))
				]
			case 2:  # Stepping out
				jointThreads += [
					threading.Thread(target=self.hipYaw.MoveToAngle, args=(abs(self.inversion - 85),)),
					threading.Thread(target=self.hipPitch.MoveToAngle, args=(abs(self.inversion - 90),)),
					threading.Thread(target=self.kneePitch.MoveToAngle, args=(abs(self.inversion - 81),))
				]
			case 3:  # Pulling in
				jointThreads += [
					threading.Thread(target=self.hipYaw.MoveToAngle, args=(abs(self.inversion - 64),)),
					threading.Thread(target=self.hipPitch.MoveToAngle, args=(abs(self.inversion - 90),)),
					threading.Thread(target=self.kneePitch.MoveToAngle, args=(abs(self.inversion - 90),))
				]
			case 4:  # Pulling in
				jointThreads += [
					threading.Thread(target=self.hipYaw.MoveToAngle, args=(abs(self.inversion - 46),)),
					threading.Thread(target=self.hipPitch.MoveToAngle, args=(abs(self.inversion - 80),)),
					threading.Thread(target=self.kneePitch.MoveToAngle, args=(abs(self.inversion - 105),))
				]
			case 5:  # Pulling in
				jointThreads += [
					threading.Thread(target=self.hipYaw.MoveToAngle, args=(abs(self.inversion - 28),)),
					threading.Thread(target=self.hipPitch.MoveToAngle, args=(abs(self.inversion - 80),)),
					threading.Thread(target=self.kneePitch.MoveToAngle, args=(abs(self.inversion - 105),))
				]
			case 6:  # Fully in
				jointThreads += [
					threading.Thread(target=self.hipYaw.MoveToAngle, args=(abs(self.inversion - 10),)),
					threading.Thread(target=self.hipPitch.MoveToAngle, args=(abs(self.inversion - 80),)),
					threading.Thread(target=self.kneePitch.MoveToAngle, args=(abs(self.inversion - 110),))
			]
			case _:
				print("Invalid phase sent to leg.")

		for thread in jointThreads:
			thread.start()
		for thread in jointThreads:
			thread.join()

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
			self.hipPitch.MoveToAngle(self.hipPitch.curAngle - 20)
		else:
			self.hipPitch.MoveToAngle(self.hipPitch.curAngle + 20)
	def Rebalance(self):
		if self.logging:
			print(f"Rebalancing leg {self.number}")
		if self.inversion == 0:
			self.hipPitch.MoveToAngle(self.hipPitch.curAngle + 20)
		else:
			self.hipPitch.MoveToAngle(self.hipPitch.curAngle - 20)
