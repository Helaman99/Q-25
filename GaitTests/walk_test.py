import time
import threading
from leg import Leg

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
		time.sleep(0.2)

		threads = []

		for leg in [curLeg, nextLeg, secondNextLeg, lastLeg]:
			t = threading.Thread(
				target=legOrder[leg].MoveToNextPosition
			)
			t.start()
			threads.append(t)

		for t in threads:
			t.join()

