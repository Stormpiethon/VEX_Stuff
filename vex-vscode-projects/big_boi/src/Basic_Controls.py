# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       alebritt                                                     #
# 	Created:      2/4/2025, 1:59:40 PM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

import vex
from vex import *

# Initialize Brain and Controller
brain = Brain()
brain.screen.clear_screen()
brain.screen.print("Program Started")
vex.wait(1000, vex.TimeUnits.MSEC)

controller = Controller()

# Initialize the motors
left_front_motor = Motor(Ports.PORT15, GearSetting.RATIO_18_1, True)
left_rear_motor = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
right_front_motor = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
right_rear_motor = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)

left_motors = MotorGroup(left_front_motor, left_rear_motor)
right_motors = MotorGroup(right_front_motor, right_rear_motor)

belt_motor = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)
roller_motor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
lever_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)

# Set up a drivetrain object for use in autonomous movement
# WheelTravel (circumference) = 326.17 mm => Wheel Diameter = 103.8 mm
# TrackWidth = 431.8
# WheelBase (distance between wheels) = 282.58 mm
# Units = MM or vex.DistanceUnits.MM
# External Gear Ratio = 2.67
drivetrain = DriveTrain(
    lm = left_motors, 
    rm = right_motors,
    wheelTravel = 326.17,  
    trackWidth = 431.8, 
    wheelBase = 282.58,
    units = MM,
    externalGearRatio = 2.67
    )


# ======================================= FUNCTIONS =====================================
def scale_input(value):
    """
    Function to scale the first portion of the joystick input for more precision
    """

    if abs(value) <= 20:
        # Cubic scaling should output to 1 at the threshold of 20
        return (value * value * value) / 8000.0

    else:
        # Linear scaling for the rest of the joystick input
        return value * 0.8

# ========================== FUNCTIONS FOR AUTONOMOUS ===================================
def autonomous():
    """
    Basic autonomous function to move forward, turn, and stop.
    """
    brain.screen.clear_screen()
    brain.screen.print("Autonomous Mode")
    
    # Move forward for 1000 mm at 50% speed
    # drivetrain.drive_for(vex.DirectionType.FORWARD, 1000, vex.DistanceUnits.MM, 50, vex.VelocityUnits.PERCENT)
    
    drivetrain.turn_for(vex.TurnType.RIGHT, 45.0, vex.RotationUnits.DEG, 10, vex.VelocityUnits.PERCENT)
    drivetrain.turn_for(vex.TurnType.LEFT, 45.0, vex.RotationUnits.DEG, 10, vex.VelocityUnits.PERCENT)
    
    # Move backward for 500 mm
    # drivetrain.drive_for(DirectionType.REVERSE, 500.0, DistanceUnits.MM, 50, VelocityUnits.PERCENT)
    
    brain.screen.clear_screen()
    brain.screen.print("Autonomous Complete")

# ===================== MAIN PROGRAM LOOP FOR DRIVER CONTROL ============================
# Driver Control Function
def driver_control():
    """
    Main driver control loop that allows for commands from the controller to be sent to the motors
    """
    # Print to Brain screen to indicate that driver control is active
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Driver Control Active")
    vex.wait(3000, vex.TimeUnits.MSEC)

    """
    # Apply deadzone for joystick inputs
    deadzone = 5
    if abs(left_speed) < deadzone:
        left_speed = 0
    if abs(right_speed) < deadzone:
        right_speed = 0
    """

    # Belt running state --- 0=off, 1=forward, -1=reverse
    belt_running = 0
    belt_speed = 75

    # Roller toggle state
    roller_running = False
    roller_speed = 60
    roller_motor.set_velocity(roller_speed, vex.VelocityUnits.PERCENT)

    # Lever toggle state --- 0=up, 1=down
    lever_position = 1
    lever_speed = 80
    lever_motor.set_velocity(lever_speed, vex.VelocityUnits.PERCENT)
    
    while True:
        # Get input values for the motors from the controller joysticks
        left_speed = scale_input(controller.axis3.position())
        right_speed = scale_input(controller.axis2.position())

        """        
        brain.screen.clear_screen()
        brain.screen.print("L: " + str(left_speed))
        brain.screen.new_line()
        brain.screen.print("R: " + str(turn_speed))
        """

        # Set the motor speeds based on the controller input
        left_motors.set_velocity(left_speed, vex.VelocityUnits.PERCENT)
        right_motors.set_velocity(right_speed, vex.VelocityUnits.PERCENT)

        # Move the wheels based on the controller input
        left_motors.spin(vex.DirectionType.FORWARD)
        right_motors.spin(vex.DirectionType.FORWARD)

        """
        # Drivetrain style controls (didn't work well), but here for reference
        # Determine direction based on forward_speed
        if forward_speed >= 0:
            direction = vex.DirectionType.FORWARD
        else:
            direction = vex.DirectionType.REVERSE

        # Drive the robot using the drivetrain object
        drivetrain.drive(direction, abs(forward_speed), turn_speed)
        """

        # Belt toggle with L1 and L2
        if controller.buttonL1.pressing():
            if belt_running != 1:
                belt_motor.spin(vex.DirectionType.FORWARD, belt_speed, vex.VelocityUnits.PERCENT)
                belt_running = 1
            else:
                belt_motor.stop()
                belt_running = 0
            vex.wait(300, vex.TimeUnits.MSEC)

        elif controller.buttonL2.pressing():
            if belt_running != -1:
                belt_motor.spin(vex.DirectionType.REVERSE, belt_speed, vex.VelocityUnits.PERCENT)
                belt_running = -1
            else:
                belt_motor.stop()
                belt_running = 0
            vex.wait(300, vex.TimeUnits.MSEC)

        # Forward Roller control toggling using the A button
        if controller.buttonA.pressing():
            if not roller_running:
                roller_motor.spin(vex.DirectionType.FORWARD, roller_speed, vex.VelocityUnits.PERCENT)
                roller_running = True
            else:
                roller_motor.stop()
                roller_running = False
            vex.wait(300, vex.TimeUnits.MSEC)

        # Reverse Roller control toggling using the X button
        if controller.buttonX.pressing():
            if not roller_running:
                roller_motor.spin(vex.DirectionType.REVERSE, roller_speed, vex.VelocityUnits.PERCENT)
                roller_running = True
            else:
                roller_motor.stop()
                roller_running = False
            vex.wait(300, vex.TimeUnits.MSEC)

        # Lever control using the right bumper buttons
        # Change the stop position status for solid holding
        if controller.buttonR1.pressing() and lever_position == 0:
            lever_motor.spin_for(50, vex.RotationUnits.DEG, True)
            lever_motor.stop(vex.BrakeType.HOLD)
            lever_position = 1
            vex.wait(300, vex.TimeUnits.MSEC)

        if controller.buttonR2.pressing() and lever_position == 1:
            lever_motor.spin_for(-50, vex.RotationUnits.DEG, True)
            lever_motor.stop(vex.BrakeType.HOLD)
            lever_position = 0
            vex.wait(300, vex.TimeUnits.MSEC)

        # Check if the down button is pressed and end the program if it is
        if controller.buttonDown.pressing():
            break

        # Allow the program to continuously update motor speeds
        vex.wait(20, vex.TimeUnits.MSEC)
        

# ======================================= MAIN PROGRAM ======================================
# Run the autonomous program
autonomous()

# Run the driver control program
driver_control()