#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
#Left Drivetrain
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_motor_c = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
#Left Group
left_drive_smart = MotorGroup(left_motor_a, left_motor_b, left_motor_c)
#Right Drivetrain
right_motor_a = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
right_motor_c = Motor(Ports.PORT6, GearSetting.RATIO_18_1, True)
#Right Group
right_drive_smart = MotorGroup(right_motor_a, right_motor_b,right_motor_c)
#Inertial
drivetrain_inertial = Inertial(Ports.PORT5)
#Drivetrain Declaration
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)
controller_1 = Controller(PRIMARY)
spinner = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)

def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # stop the motors if the brain is calibrating
            if drivetrain_inertial.is_calibrating():
                left_drive_smart.stop()
                right_drive_smart.stop()
                while drivetrain_inertial.is_calibrating():
                    sleep(25, MSEC)
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3
            # right = axis2
            drivetrain_left_side_speed = controller_1.axis3.position()
            drivetrain_right_side_speed = controller_1.axis2.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code

def cprint(row,text):
    controller_1.screen.clear_row(row)
    controller_1.screen.set_cursor(row, 1)
    controller_1.screen.print(str(text))

def rumble(patern):
    patern = str(patern)
    controller_1.rumble(patern)

#Function to print on brain mainly to clear clutter
def bprint(row,text,column=1):
    brain.screen.clear_row(row)
    brain.screen.set_cursor(row, column)
    brain.screen.print(str(text))

#ShooterGroup Shooting Function
def disk_launch(percent, times):
    intake.set_velocity(100, PERCENT)
    intake.spin(FORWARD)
    for i in range(times):
        ShooterGroup.set_velocity(percent,PERCENT)
        ShooterGroup.spin(FORWARD)
        wait(3,SECONDS)
        pusher.set(False)
        wait(200,MSEC)
        pusher.set(True)
    ShooterGroup.stop()
    intake.stop()

def preAutonomous():
    pass

def autonomous_short():
    pass

def autonomous_long():
    pass

def autonomous_skills():
    pass

#----------------PID----------------

def pid(expected,d_velocity=100):
    expected = (expected + drivetrain_inertial.rotation(DEGREES))

    wait(0.25, SECONDS)
    
    error = expected

    while True:
        actual = drivetrain_inertial.rotation(DEGREES)
        error = (expected - actual)
        speed = (error * 0.5)
        left_motor_a.set_velocity(speed,PERCENT)
        left_motor_b.set_velocity(speed,PERCENT)
        right_motor_a.set_velocity(-speed,PERCENT)
        right_motor_b.set_velocity(-speed,PERCENT)
        
        left_motor_a.spin(FORWARD)
        left_motor_b.spin(FORWARD)
        right_motor_a.spin(FORWARD)
        right_motor_b.spin(FORWARD)
        
        cprint(2,str(error))

        if abs(error) < 2:
            break

        wait(0.15,SECONDS)
            
    drivetrain.stop()
    left_motor_a.set_velocity(d_velocity,PERCENT)
    left_motor_b.set_velocity(d_velocity,PERCENT)
    right_motor_a.set_velocity(d_velocity,PERCENT)
    right_motor_b.set_velocity(d_velocity,PERCENT)
    cprint(2,'PID Completed') 


def driverControl():
    userFeedbackThread = Thread(userFeedback) #Creating Threads to maximize efficency
    while True:
        pass


def userFeedback():
    while True:
        pass



my_thread1 = Thread(driverControl)

        

comp = Competition(driverControl, autonomous_short)
preAutonomous()