# ---------------------------------------------------------------------------- #
#                           Autonomous Functions Template                      #
# ---------------------------------------------------------------------------- #

import vex
from vex import *

# Initialize Brain
brain = Brain()

belt_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)

# ========================= MOTOR SETUP FOR BIG ROBOT =================================
left_front_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
left_rear_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_front_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
right_rear_motor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
rear_lever_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)

# ========================= MOTOR SETUP FOR SMALL ROBOT ===============================
# left_front_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
# right_front_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
# arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)

# ======================== AUTONNOMOUS FUNCTIONS ======================================
# Move the robot forward at a specified speed for a given duration.
def drive_forward(speed, duration):
    """
    Drive the robot forward at a specified speed for a given duration.
    """
    left_front_motor.set_velocity(speed, vex.VelocityUnits.PERCENT)
    left_rear_motor.set_velocity(speed, vex.VelocityUnits.PERCENT)
    right_front_motor.set_velocity(speed, vex.VelocityUnits.PERCENT)
    right_rear_motor.set_velocity(speed, vex.VelocityUnits.PERCENT)

    left_front_motor.spin(vex.DirectionType.FORWARD)
    left_rear_motor.spin(vex.DirectionType.FORWARD)
    right_front_motor.spin(vex.DirectionType.FORWARD)
    right_rear_motor.spin(vex.DirectionType.FORWARD)

    vex.wait(duration, vex.TimeUnits.MSEC)
    stop_motors()

# Rotate the entire robot in a counter-clockwise direction.
def turn_left(speed, duration):
    """
    Turn the robot left by running the left motors in reverse and right motors forward.
    """
    left_front_motor.set_velocity(-speed, vex.VelocityUnits.PERCENT)
    left_rear_motor.set_velocity(-speed, vex.VelocityUnits.PERCENT)
    right_front_motor.set_velocity(speed, vex.VelocityUnits.PERCENT)
    right_rear_motor.set_velocity(speed, vex.VelocityUnits.PERCENT)

    left_front_motor.spin(vex.DirectionType.FORWARD)
    left_rear_motor.spin(vex.DirectionType.FORWARD)
    right_front_motor.spin(vex.DirectionType.FORWARD)
    right_rear_motor.spin(vex.DirectionType.FORWARD)

    vex.wait(duration, vex.TimeUnits.MSEC)
    stop_motors()

# Rotate the entire robot in a clockwise direction.
def turn_right(speed, duration):
    """
    Turn the robot right by running the left motors forward and right motors in reverse.
    """
    left_front_motor.set_velocity(speed, vex.VelocityUnits.PERCENT)
    left_rear_motor.set_velocity(speed, vex.VelocityUnits.PERCENT)
    right_front_motor.set_velocity(-speed, vex.VelocityUnits.PERCENT)
    right_rear_motor.set_velocity(-speed, vex.VelocityUnits.PERCENT)

    left_front_motor.spin(vex.DirectionType.FORWARD)
    left_rear_motor.spin(vex.DirectionType.FORWARD)
    right_front_motor.spin(vex.DirectionType.FORWARD)
    right_rear_motor.spin(vex.DirectionType.FORWARD)

    vex.wait(duration, vex.TimeUnits.MSEC)
    stop_motors()

# Rotate a single motor a specified number of degrees at a given speed, then stop.
def rotate_motor(motor, degrees, speed):
    """
    Rotate a single motor a specified number of degrees at a given speed, then stop.
    
    Parameters:
    motor (Motor): The motor to rotate.
    degrees (float): The number of degrees to rotate the motor.
    speed (int): The speed to rotate the motor (percentage).
    """
    # Set the motor velocity
    motor.set_velocity(speed, vex.VelocityUnits.PERCENT)

    # Rotate the motor for the specified number of degrees
    motor.rotate_for(degrees, vex.RotationUnits.DEG, wait=True)

    # Stop the motor after rotation
    motor.stop()

# Stop all motors immediately.
def stop_motors():
    """
    Stop all movement motors immediately.
    """
    left_front_motor.stop()
    left_rear_motor.stop()
    right_front_motor.stop()
    right_rear_motor.stop()

# Function to rotate a single motor for driving a belt
def run_belt_motor(motor, speed):
    """
    Activates a motor to rotate a belt continuously at a given speed.

    Parameters:
    motor (Motor): The motor to control.
    speed (int): The speed to rotate the motor (percentage).
    """
    # Set the motor velocity
    motor.set_velocity(speed, vex.VelocityUnits.PERCENT)

    # Spin the motor indefinitely in the forward direction
    motor.spin(vex.DirectionType.FORWARD)

# ========================= Autonomous Routine Example ==========================
def autonomous_routine():
    """
    Example of a simple autonomous routine using the movement functions.
    """
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Autonomous Started")

    # Drive forward for 2 seconds at 50% speed
    drive_forward(50, 2000)

    # Turn left for 1 second at 30% speed
    turn_left(30, 1000)

    # Drive forward for 1.5 seconds at 60% speed
    drive_forward(60, 1500)

    # Turn right for 0.5 seconds at 30% speed
    turn_right(30, 500)

    # Stop the motors at the end of the routine
    stop_motors()

    # Rotate left_front_motor 180 degrees at 50% speed
    rotate_motor(left_front_motor, 180, 50)

    # Rotate left_front_motor 90 degrees at 35% speed
    rotate_motor(left_front_motor, 90, 35)

    # Run the belt motor at 50% speed for 5 seconds
    run_belt_motor(belt_motor, 50)
    vex.wait(5, vex.TimeUnits.SEC)
    belt_motor.stop()

# Uncomment this to test the autonomous function
# autonomous_routine()
