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

# Competition Object (Handles Autonomous & Driver Control)
# competition = vex.Competition()

# Initialize the devices that will be used
brain = Brain()
brain.screen.clear_screen()
brain.screen.print("Program Started")
vex.wait(1000, vex.TimeUnits.MSEC)

controller = Controller()

# ========================= MOTOR SETUP FOR SMALL ROBOT =================================
left_rear_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
right_rear_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)

belt_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)

arm_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)

# ========================== FUNCTIONS FOR MECHANICALS ==================================


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
    vex.wait(5000, vex.TimeUnits.MSEC)
    
    while True:
        # Set the motor speeds based on the joystick input
        left_speed = controller.axis3.position() * 0.8
        right_speed = controller.axis2.position() * 0.8

        # Set default motor speeds
        belt_speed = 40
        arm_speed = 10

        # Apply deadzone for joystick inputs
        deadzone = 5
        if abs(left_speed) < deadzone:
            left_speed = 0
        if abs(right_speed) < deadzone:
            right_speed = 0

        # Print values to Brain screen for debugging
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("L:", left_speed, " R:", right_speed)

        # Left side motors
        left_rear_motor.set_velocity(left_speed, vex.VelocityUnits.PERCENT)

        # Right side motors
        right_rear_motor.set_velocity(right_speed, vex.VelocityUnits.PERCENT)

        # Spin motors based on joystick input
        left_rear_motor.spin(vex.DirectionType.FORWARD)
        right_rear_motor.spin(vex.DirectionType.FORWARD)

        # Belt control using the left bumper buttons for forward and reverse
        if controller.buttonL1.pressing():
            belt_motor.spin(vex.DirectionType.FORWARD, belt_speed, vex.VelocityUnits.PERCENT)
        elif controller.buttonL2.pressing():
            belt_motor.spin(vex.DirectionType.REVERSE, belt_speed, vex.VelocityUnits.PERCENT)
        else:
            belt_motor.stop(vex.BrakeType.HOLD)

        # Arm control using the left bumper buttons for forward and reverse
        if controller.buttonR1.pressing():
            arm_motor.spin(vex.DirectionType.FORWARD, arm_speed, vex.VelocityUnits.PERCENT)
        elif controller.buttonR2.pressing():
            arm_motor.spin(vex.DirectionType.REVERSE, arm_speed, vex.VelocityUnits.PERCENT)
        else:
            arm_motor.stop(vex.BrakeType.HOLD)

        # Allow the program to continuously update motor speeds
        vex.wait(20, vex.TimeUnits.MSEC)
        

# ============================== MAIN PROGRAM =====================================
driver_control()