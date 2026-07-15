import time
import threading
from leg import Joint

joints = []
for i in range(16):
	joints.append(Joint(i))

# It is assumed the robot is already in a standing position

joints[5].MoveToAngle(joints[5].curAngle + 20)
joints[13].MoveToAngle(joints[13].curAngle + 20)
joints[12].MoveToAngle(100)
joints[13].MoveToAngle(joints[13].curAngle - 20)
joints[5].MoveToAngle(joints[5].curAngle - 20)

joints[9].MoveToAngle(joints[9].curAngle - 20)
joints[1].MoveToAngle(joints[1].curAngle - 20)
joints[0].MoveToAngle(20)
joints[1].MoveToAngle(joints[1].curAngle + 20)
joints[9].MoveToAngle(joints[9].curAngle + 20)

joints[1].MoveToAngle(joints[1].curAngle - 20)
joints[13].MoveToAngle(joints[13].curAngle + 20)

joints[9].MoveToAngle(joints[9].curAngle - 20)
joints[8].MoveToAngle(115)
joints[10].MoveToAngle(40)
joints[9].MoveToAngle(115)

joints[5].MoveToAngle(joints[5].curAngle + 20)
joints[4].MoveToAngle(5)
joints[6].MoveToAngle(80)
joints[5].MoveToAngle(5)

joints[1].MoveToAngle(joints[1].curAngle + 20)
joints[13].MoveToAngle(joints[13].curAngle - 20)
