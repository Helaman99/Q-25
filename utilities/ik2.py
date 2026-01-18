import sys
import argparse
import math

# Leg segment lengths (cm)
proximal_length = 9.0
distal_length = 24.5

# Offsets (cm)
hip_yaw_offset = 2.3  # Lateral offset from hip yaw to proximal pivot
z_offset_from_bottom = 8.1  # Vertical offset from robot bottom to proximal pivot

# Joint limits (degrees)
joint_min = 0
joint_max = 120

def inverseKinematics(x, y, z, hip_x_offset=0, hip_y_offset=0):
    """
    Calculate inverse kinematics for spider leg.
    
    Parameters:
    -----------
    x : float
        Target X position (right) in cm, relative to robot center bottom
    y : float
        Target Y position (forward) in cm, relative to robot center bottom
    z : float
        Target Z position (up) in cm, relative to robot bottom (0 = ground level)
    hip_x_offset : float
        X position of this hip's yaw motor relative to robot center (cm)
    hip_y_offset : float
        Y position of this hip's yaw motor relative to robot center (cm)
        
    Returns:
    --------
    dict : {'hip_yaw': float, 'hip_pitch': float, 'knee_pitch': float}
        Joint angles in degrees, or None if unreachable
    """
    
    # Adjust target position relative to hip yaw motor position
    target_x = x - hip_x_offset
    target_y = y - hip_y_offset
    target_z = z #+ z_offset_from_bottom # Adjust z to be relative to proximal pivot
    
    # Calculate hip yaw angle
    # Account for the lateral offset from yaw axis to proximal pivot
    horizontal_dist = math.sqrt(target_x**2 + target_y**2)
    
    if horizontal_dist < 0.001:
        # Target is directly below, undefined yaw
        print("Error: Target directly below hip")
        return None
    
    # Calculate yaw angle (0° = forward/Y-axis)
    yaw = math.degrees(math.atan2(target_x, target_y))
    
    # Calculate the position of the proximal pivot point after yaw rotation
    # The pivot is offset laterally from the yaw axis
    pivot_to_target_horizontal = horizontal_dist - hip_yaw_offset
    
    if pivot_to_target_horizontal < 0:
        print("Error: Target too close to hip yaw axis")
        return None
    
    # Now solve 2D IK in the plane defined by the yaw rotation
    # Distance from proximal pivot to target in the leg plane
    horizontal_reach = pivot_to_target_horizontal
    vertical_reach = target_z
    
    # Total distance to target
    distance_to_target = math.sqrt(horizontal_reach**2 + vertical_reach**2)
    
    # Check if target is reachable
    max_reach = proximal_length + distal_length
    min_reach = abs(proximal_length - distal_length)
    
    if distance_to_target > max_reach:
        print(f"Error: Target too far: {distance_to_target:.2f}cm > {max_reach:.2f}cm")
        return None
    
    if distance_to_target < min_reach:
        print(f"Error: Target too close: {distance_to_target:.2f}cm < {min_reach:.2f}cm")
        return None
    
    # Use law of cosines to find knee angle
    # Knee angle is the internal angle at the knee joint
    cos_knee = (proximal_length**2 + distal_length**2 - distance_to_target**2) / \
               (2 * proximal_length * distal_length)
    
    # Clamp to valid range to handle floating point errors
    cos_knee = max(-1.0, min(1.0, cos_knee))
    
    # Internal angle at knee
    knee_internal_angle = math.degrees(math.acos(cos_knee))
    
    # Knee pitch servo angle (exterior angle, for spider leg bending upward)
    # For spider leg: knee_pitch = 180 - internal_angle gives upward bend
    knee_pitch = 180 - knee_internal_angle
    
    # Use law of cosines to find angle at proximal pivot
    cos_proximal = (proximal_length**2 + distance_to_target**2 - distal_length**2) / \
                   (2 * proximal_length * distance_to_target)
    
    cos_proximal = max(-1.0, min(1.0, cos_proximal))
    angle_to_target = math.degrees(math.acos(cos_proximal))
    
    # Angle from horizontal to target
    target_angle = math.degrees(math.atan2(vertical_reach, horizontal_reach))
    
    # Hip pitch angle (measured from horizontal, positive = upward)
    hip_pitch = target_angle + angle_to_target
    
    # Check joint limits
    if not (joint_min <= hip_pitch <= joint_max):
        print(f"Error: Hip pitch {hip_pitch:.1f}° out of range [{joint_min}, {joint_max}]")
        return None
    
    if not (joint_min <= knee_pitch <= joint_max):
        print(f"Error: Knee pitch {knee_pitch:.1f}° out of range [{joint_min}, {joint_max}]")
        return None
    
    return {
        'hip_yaw': yaw,
        'hip_pitch': hip_pitch,
        'knee_pitch': knee_pitch
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
    
    print(f"\nCalculated angles:")
    print(f"  Hip Yaw: {result['hip_yaw']:.2f}°")
    print(f"  Hip Pitch: {result['hip_pitch']:.2f}°")
    print(f"  Knee Pitch: {result['knee_pitch']:.2f}°")
    print()
    
    input("Verify angle validity, then press Enter to continue.\n")

    import time
    from adafruit_servokit import ServoKit

    kit = ServoKit(channels=16)

    kit.servo[0].angle = min(result["hip_yaw"] + 15, 120)
    kit.servo[1].angle = (120 - result["hip_pitch"])
    kit.servo[2].angle = result["knee_pitch"]
