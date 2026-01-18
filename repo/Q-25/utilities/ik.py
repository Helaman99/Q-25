import sys
import argparse
import math

# Leg segments in inches
prox = 3.75
dist = 9.75
z_offset = 3.25

def inverseKinematics(x, y, z):
    	# converting to inches
    	x_in = x / 2.54
    	y_in = y / 2.54
    	z_in = z / 2.54
    
    	# Calculate hip yaw
    	yaw = math.atan2(y_in, x_in)
    
    	# Horizontal distance from hip yaw axis
    	r = math.sqrt(x_in**2 + y_in**2)
    
    	# Adjust z for the offset between hip and the start of the IK chain
    	z_adjusted = z_in - z_offset
    
    	# Distance between hip pitch joint and foot
    	d = math.sqrt(r**2 + z_adjusted**2)
    
    	# Check if target is reachable
    	if d > (prox + dist) or d < abs(prox - dist):
        	return None  # Target unreachable
    
    	# Knee angle (using law of cosines)
    	knee = math.pi - math.acos((prox**2 + dist**2 - d**2) / (2 * prox * dist))
    
    	# Hip pitch angle
    	hip_pitch = math.atan2(z_adjusted, r) + math.acos((prox**2 + d**2 - dist**2) / (2 * prox * d))
    
    	return {
        	"hip_yaw": math.degrees(yaw),
        	"hip_pitch": math.degrees(hip_pitch),
        	"knee_pitch": math.degrees(knee)
    	}

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Inverse kinematics for quadruped spider leg")
	parser.add_argument("x", type=float, help="Target x coordinate (cm)")
	parser.add_argument("y", type=float, help="Target y coordinate (cm)")
	parser.add_argument("z", type=float, help="Target z coordinate (cm)")
	args = parser.parse_args()

	result = inverseKinematics(args.x, args.y, args.z)
	if result == None:
		print("Target is unreachable.\n")
		sys.exit()
	print(result)
	input("Verify angle validity, then press Enter to continue.\n")

	import time
	from adafruit_servokit import ServoKit

	kit = ServoKit(channels=16)

	kit.servo[0].angle = min(result["hip_yaw"] + 15, 120)
	kit.servo[1].angle = (120 - result["hip_pitch"])
	kit.servo[2].angle = result["knee_pitch"]
