# Notes for implementing the walking gait

Starting angle: Hip pitch 80, knee pitch 110
Left leg --> just lift hip pitch
Rotate hip yaw to desired angle (not by much)
Bring hip pitch to ~100 degrees and knee pitch to ~30 degrees
Then bring yaw to almost 0 while making hip pitch about 80 degrees again and knee pitch about 75 degrees
-----
Standing positions:

Big angles
Hip pitch: 80
Knee pitch: 110

Small angles:
Hip pitch: 40
Knee pitch: 10

Leg 0 - Big angles
Leg 1 - Small angles
Leg 2 - Big angles
Leg 3 - Small angles
-----
Positions that are looped through for walking:
0 - Standing position using angles above
1 - Lifted position
2 - Foot placed on ground far from body
3 - Foot moves towards body
4 - Foot on ground closest to body

Direction of walking determines hip yaw; hip and knee pitch angles are the same.
Turning mid-walk includes reducing all the angles of the inside legs.

There are 4 phases that each leg goes through for the robot to walk.
Therefor we can have a repeating loop between 0 and 4, where each leg's gait is initiated
by the corrresponding number in the loop.
