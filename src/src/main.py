#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
#ShooterGroup
ShooterGroup_motor_a = Motor(Ports.PORT6, GearSetting.RATIO_36_1, True)
ShooterGroup_motor_b = Motor(Ports.PORT7, GearSetting.RATIO_36_1, True)

ShooterGroup = MotorGroup(ShooterGroup_motor_a, ShooterGroup_motor_b)
Intake = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
expansion = DigitalOut(brain.three_wire_port.h)
controller_1 = Controller(PRIMARY)
spinner = Motor(Ports.PORT2, GearSetting.RATIO_36_1, False)
pusher = DigitalOut(brain.three_wire_port.g)
rear_distance = Distance(Ports.PORT20)
left_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT14, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT17, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain_inertial = Inertial(Ports.PORT1)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)
right_distance = Sonar(brain.three_wire_port.e)
left_distance = Sonar(brain.three_wire_port.c)
# vex-vision-config:begin
front_vision__SIG_1 = Signature(1, -4059, -2931, -3495,13509, 15559, 14534,2.5, 0)
front_vision = Vision(Ports.PORT10, 50, front_vision__SIG_1)
# vex-vision-config:end


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
#SHORT CODE
# ------------------------------------------
# 	Project: Middle School Robotics
#	Author: Ryan Chan-Wu, Alex Savoulides
#	Created: 11/19/22 (after the tragedy of the pdf)
# ------------------------------------------

#Defining Variables;
spinner_for: int = 100

#--------------------Functions Begin--------------------
#Function to print on screen mainly to clear clutter
def cprint(row,text):
    controller_1.screen.clear_row(row)
    controller_1.screen.set_cursor(row, 1)
    controller_1.screen.print(str(text))

#Function to print on brain mainly to clear clutter
def bprint(row,text):
    brain.screen.clear_row(row)
    brain.screen.set_cursor(row, 1)
    brain.screen.print(str(text))

#ShooterGroup Shooting Function
def disk_launch(percent, times):
    Intake.set_velocity(100, PERCENT)
    Intake.spin(FORWARD)
    for i in range(times):
        ShooterGroup.set_velocity(percent,PERCENT)
        ShooterGroup.spin(FORWARD)
        wait(3,SECONDS)
        pusher.set(True)
        wait(200,MSEC)
        pusher.set(False)
    ShooterGroup.stop()
    Intake.stop()

#Update Driver Velocity
def dveloc(percent):
    left_motor_a.set_velocity(percent, PERCENT)
    left_motor_b.set_velocity(percent, PERCENT)
    right_motor_a.set_velocity(percent, PERCENT)
    right_motor_b.set_velocity(percent, PERCENT)


#----------------PID----------------

def pid(expected):

    expected = (expected + drivetrain_inertial.rotation(DEGREES))

    wait(0.25, SECONDS)
    
    error = expected

    while True:
        actual = drivetrain_inertial.rotation(DEGREES)
        error = (expected - actual)
        speed = (error * .5)
        left_motor_a.set_velocity(speed,PERCENT)
        left_motor_b.set_velocity(speed,PERCENT)
        right_motor_a.set_velocity(-speed,PERCENT)
        right_motor_b.set_velocity(-speed,PERCENT)
        
        left_motor_a.spin(FORWARD)
        left_motor_b.spin(FORWARD)
        right_motor_a.spin(FORWARD)
        right_motor_b.spin(FORWARD)
        
        cprint(3,str(error))
        
        wait(0.15,SECONDS)
        
        if abs(error) < 2:
            break
        
    drivetrain.stop()
    left_motor_a.set_velocity(70,PERCENT)
    left_motor_b.set_velocity(70,PERCENT)
    right_motor_a.set_velocity(70,PERCENT)
    right_motor_b.set_velocity(70,PERCENT)
    wait(2,SECONDS)
    cprint(2,'PID Terminated')
    dveloc(100)

#----------------END OF PID----------------

#Logging time of Start:
start_time = None
def log_start_time():
    global start_time
    start_time = brain.timer.time(SECONDS)

#---------------------Autonomous Short ------------------
def autonomous_short():
    calibrate_drivetrain()
    cprint(1, 'Auton. ON (SHORT')
    while rear_distance.object_distance(MM) > 70: 
        drivetrain.drive(REVERSE)
    #Terminating reverse functions
    drivetrain.drive(REVERSE)
    #spinning spinner for 10 degrees
    spinner.spin_for(FORWARD,spinner_for,DEGREES)
    drivetrain.stop()
    drivetrain.turn_for(RIGHT, 75, DEGREES)
    ShooterGroup.set_velocity(85,PERCENT)
    ShooterGroup.spin(FORWARD)
    wait(2,SECONDS)
    pusher.set(False)
    wait(1,SECONDS)
    controller_1.screen.clear_screen()
    
#---------------------Autonomous Long --------------------
def autonomous_long():
    calibrate_drivetrain()
    dveloc(70)
    #Updating status on screen utilizing cprint function
    cprint(1, "Auton. ON (LONG)")
    #Autonomous Program
    #While loop to reverse until distance sensor is roughly 700
    while rear_distance.object_distance(MM) > 830:
        drivetrain.drive(REVERSE)
    #updating status on screen.
    cprint(1,'Turning To Roller')
    #turning right in preperation to get in contact with roller
    drivetrain.turn_for(RIGHT,90,DEGREES)
    #Updating status on screen
    cprint(1, 'Reversing To Roller')
    #Reversing to roller until the switch contact sensor detects contact
    while rear_distance.object_distance(MM) > 70: 
        drivetrain.drive(REVERSE)
    #Terminating reverse functions
    drivetrain.stop()
    drivetrain.drive(REVERSE)
    #updating spinner status
    cprint(1,'Rotating Spinner')
    #spinning spinner for 10 degrees
    spinner.spin_for(FORWARD,spinner_for,DEGREES)
    drivetrain.stop()
    controller_1.screen.clear_screen()
 
      
    
# ----------------------- Autonomous Skills (ALEX) -----------------------
def autonomous_skills():
    calibrate_drivetrain()
    #Updating Velocities
    drivetrain.set_stopping(COAST)
    dveloc(80)
    #Reversing into Spinner #1
    while rear_distance.object_distance(MM) > 70: 
        drivetrain.drive(REVERSE)
    spinner.spin_for(FORWARD,spinner_for,DEGREES)
    drivetrain.stop()
    #Going Forwards; preparing to drivetrain.turn_for into Spinner #2
    while rear_distance.object_distance(MM) < 450:
        drivetrain.drive(FORWARD)
    drivetrain.stop()
    #Reversing into Spinner #2
    pid(90)
    while rear_distance.object_distance(MM) > 70: 
        drivetrain.drive(REVERSE)
    #Spinner Spinning #2
    spinner.spin_for(FORWARD,spinner_for,DEGREES)
    drivetrain.stop()
    wait(1,SECONDS)
    #Going towards Middle
    while rear_distance.object_distance(MM) < 1600:
        drivetrain.drive(FORWARD)
    drivetrain.stop()
    pid(13)
    disk_launch(75,3)
    pid(77)
    #At Middle
    while rear_distance.object_distance(MM) > 600 or not(rear_distance.is_object_detected()):
        drivetrain.drive(REVERSE)
    drivetrain.stop()
    drivetrain.turn_for(RIGHT,90)
    if right_distance.distance(MM) > 635:
        drivetrain.turn_for(LEFT,90)
        while rear_distance.object_distance(MM) > 600:
            drivetrain.drive(REVERSE)
        drivetrain.stop()
        drivetrain.turn_for(RIGHT,90)
    #Going to Spinner #3
    while rear_distance.object_distance(MM) > 65: 
        drivetrain.drive(REVERSE)
    spinner.spin_for(FORWARD,spinner_for,DEGREES)
    drivetrain.stop()
    #Going to Spinner #4
    while rear_distance.object_distance(MM) < 500:
        drivetrain.drive(FORWARD)
    drivetrain.stop()
    pid(-90)
    while rear_distance.object_distance(MM) > 70: 
        drivetrain.drive(REVERSE)
    spinner.spin_for(FORWARD,spinner_for,DEGREES)
    drivetrain.stop()
    expansion.set(True)
    wait(5,SECONDS)
    expansion.set(False)
    controller_1.screen.clear_screen()





#Creating user_control function
def user_control():
    controller_1.screen.clear_screen()
    #setting shooter velocity variable to 75%
    s_velocity = 75
    #updating the shooter velocity after autonomous mode
    cprint(1, 'Shooter: Veloc: '+str(s_velocity)+'%')
    #Log Starting Time for Timer
    dveloc(100)
    while True: 
        #----Print Motor Temperature Status---
        #ShooterGroup
        bprint(1, 'ShooterA Temp: '+str(ShooterGroup_motor_a.temperature(PERCENT))+'%')
        bprint(2, 'ShooterB Temp: '+str(ShooterGroup_motor_b.temperature(PERCENT))+'%')
        #Intake
        bprint(3, 'Intake Temp: '+str(Intake.temperature(PERCENT))+'%')
        #Drivetrain
        bprint(4, 'DrivetrainL1 Temp: '+str(left_motor_a.temperature(PERCENT))+'%') 
        bprint(5, 'DrivetrainL2 Temp: '+str(left_motor_b.temperature(PERCENT))+'%') 
        bprint(6, 'DrivetrainR1 Temp: '+str(right_motor_a.temperature(PERCENT))+'%')
        bprint(7, 'DrivetrainR2 Temp: '+str(right_motor_b.temperature(PERCENT))+'%') 
        #Spinner
        bprint(8, 'Spinner Temp: '+ str(spinner.temperature(PERCENT))+'%')
        #Print Distance Sensor (For Debbuging)
        bprint(9, 'RearDistance:' + str(rear_distance.object_distance(MM))+ 'mm')
        bprint(10, 'LeftDistance: ' +str(left_distance.distance(MM))+'mm')
        bprint(11, 'RightDistance: '+ str(right_distance.distance(MM))+'mm' )        
        #Updating ShooterGroup Velocity
        ShooterGroup.set_velocity(int(s_velocity), PERCENT)
        #Defining Variables
        #Setting Buttons
        if controller_1.buttonL1.pressing():
            #Displaying the ShooterGroup Velocity on Screen
            cprint(2, 'Shooter: '+str(round((((ShooterGroup_motor_a.velocity(PERCENT)*ShooterGroup_motor_b.velocity(PERCENT))/2)/s_velocity*100)))+'%')
            ShooterGroup.spin(FORWARD)
        else:
            controller_1.screen.clear_row(2)
            ShooterGroup.stop()
            #ShooterGroup: -10
        if controller_1.buttonA.pressing() and (int(s_velocity) >= 70):
            s_velocity -= 10
            #update status with text/vibration
            cprint(1, 'Shooter: Veloc: '+str(s_velocity)+'%')
            controller_1.rumble(".")
            #ShooterGroup: +5
        if controller_1.buttonX.pressing() and (int(s_velocity) <= 95):
            s_velocity += 5
            #update status with text/vibration
            cprint(1, 'Shooter: Veloc: '+ str(s_velocity) +'%')
            controller_1.rumble(".") 
            #ShooterGroup + 10
        if controller_1.buttonY.pressing() and (int(s_velocity) <= 90):
            s_velocity += 10
            #update status with text/vibration
            cprint(1, 'Shooter: Veloc: '+str(s_velocity)+ '%')
            controller_1.rumble(".")
        if controller_1.buttonR1.pressing():
            Intake.set_velocity(100, PERCENT)
            Intake.spin(FORWARD)
        elif controller_1.buttonR2.pressing():
            Intake.set_velocity(100, PERCENT)
            Intake.spin(REVERSE)
        else:
            Intake.set_velocity(0, PERCENT)
        if controller_1.buttonB.pressing():
            expansion.set(True)
            controller_1.rumble("-")
            wait(5,SECONDS)
            expansion.set(False)
        if controller_1.buttonDown.pressing():
            pusher.set(False)
            controller_1.rumble("-")
        else:
            pusher.set(True)
        if controller_1.buttonLeft.pressing():
            spinner.set_velocity(100, PERCENT)
            spinner.spin(FORWARD)
        elif controller_1.buttonRight.pressing():
            spinner.spin(REVERSE)
        else:
            spinner.stop()
        #Temporary for debugging purposes 
        if controller_1.buttonL2.pressing():
            autonomous_skills()
#     Competition Format (Do Not Modify)
# ------------------------------------------

def vex_auton():
    auton_control_0 = Thread(autonomous_long)

    while(competition.is_autonomous() and competition.is_enabled() ):
        wait(10, MSEC)
    
    auton_control_0.stop()

def vex_driver():
    driver_control_0 = Thread(user_control)

    while(competition.is_driver_control() and competition.is_enabled()):
        wait(10, MSEC)
    driver_control_0.stop()

competition = Competition(vex_driver, vex_auton)


