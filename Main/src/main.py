#region VEXcode Generated Robot Configuration
#Importing Vex
from vex import *
#Used Tan-Cos-Etc
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
#---ShooterGroup---
ShooterGroup_motor_a = Motor(Ports.PORT6, GearSetting.RATIO_36_1, True)
ShooterGroup_motor_b = Motor(Ports.PORT7, GearSetting.RATIO_36_1, True)
#Grouped
ShooterGroup = MotorGroup(ShooterGroup_motor_a, ShooterGroup_motor_b)
#---Intake---
Intake = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
#---Expansion---
expansion = DigitalOut(brain.three_wire_port.h)
#---Controller---
controller_1 = Controller(PRIMARY)
#---Spinner---
spinner = Motor(Ports.PORT2, GearSetting.RATIO_36_1, False)
#---Pusher---
pusher = DigitalOut(brain.three_wire_port.g)
#---Contact/Distance Sensors---
rear_distance = Distance(Ports.PORT20)
right_distance = Sonar(brain.three_wire_port.e)
left_distance = Sonar(brain.three_wire_port.c)
spinner_switch = Limit(brain.three_wire_port.b)
#---Drivetrain---
#Left
left_motor_a = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
#Left Group
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
#Right
right_motor_a = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)
#Right Group
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
#Drivetrain Inertial (Gyro)
drivetrain_inertial = Inertial(Ports.PORT1)
#Combination
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)



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
#endregion VEXcode Generated Robot Configuration
#SHORT CODE
# ------------------------------------------
# 	Project: Middle School Robotics
#	Author: Ryan Chan-Wu, Alex Savoulides
#	Created: 11/19/22 (after the tragedy of the pdf)
# ------------------------------------------

#Velocity Function
def cprint(row,text):
    controller_1.screen.clear_row(row)
    controller_1.screen.set_cursor(row, 1)
    controller_1.screen.print(str(text))

def bprint(row,text):
    brain.screen.clear_row(row)
    brain.screen.set_cursor(row, 1)
    brain.screen.print(str(text))

def shooter(percent):
    ShooterGroup.set_velocity(percent,PERCENT)
    ShooterGroup.spin(FORWARD)
    wait(6,SECONDS)
    pusher.set(True)
    wait(1,SECONDS)
    pusher.set(False)
def driveveloc(percent):
    left_motor_a.set_velocity(percent,PERCENT)
    left_motor_b.set_velocity(percent,PERCENT)
    right_motor_a.set_velocity(percent,PERCENT)
    right_motor_b.set_velocity(percent,PERCENT)

#---------------------Autonomous Short ------------------
def autonomous_short():
    cprint(1, 'Auton. ON (SHORT')
    while spinner_switch == False:
        drivetrain.drive(REVERSE)
    drivetrain.stop()
    spinner.spin_for(FORWARD,10,DEGREES)
    drivetrain.turn_for(LEFT,10,DEGREES)
    
#---------------------Autonomous Long --------------------
def autonomous_long():
#Updating status on screen utilizing cprint function
    cprint(1, "Auton. ON (LONG)")
#Defining Variables
    shooter_veloc = 0
#Setting Velocities
    driveveloc(70)
#Autonomous Program
    #While loop to reverse until distance sensor is roughly 700
    while rear_distance.object_distance(MM) > 700:
        #30 MSEC wait to prevent distorientation on cprint function
        wait(30, MSEC)
        #consistently updating controller screen for debugging purposes
        cprint(1, "Dist. Rem.: "+ str(700-rear_distance.object_distance(MM))+'mm')
        #finally - we do what the function is intended to - reverse
        drivetrain.drive(REVERSE)
    #updating status on screen.
    cprint(1,'Turning To Roller')
    #turning right in preperation to get in contact with roller
    drivetrain.turn_for(RIGHT,90,DEGREES)
    #Updating status on screen
    cprint(1, 'Reversing To Roller')
    #Reversing to roller until the switch contact sensor detects contact
    while spinner_switch == False:
        drivetrain.drive(REVERSE)
    #Updating status on screen 
    cprint(1, 'Sensor Contact')
    #Terminating reverse functions
    drivetrain.stop()
    #updating spinner status
    cprint(1,'Rotating Spinner')
    #spinning spinner for 10 degrees
    spinner.spin_for(FORWARD,10,DEGREES)
    #go forwards in order to prevent turning against spinner
    drivetrain.drive_for(FORWARD,1,INCHES)
    #updating status on screen
    cprint(1,"Calculating Angle's") 
    #calculating the total distance between robot and net
    net_dist = 1175-int(rear_distance.object_distance(MM))
    #using magic invented by Muhammad ibn Mūsā al-Khwārizmī in 9th century AD
    shoot_angle = math.atan(1175-int(rear_distance.object_distance(MM)))/(right_distance.distance(MM))
    #updating status on screen to display that the angle has indeed been calculated
    cprint(1,'Angle Calculated: '+str(shoot_angle)+'%')
    #turning to the angle previously calculated
    drivetrain.turn_for(RIGHT,int(shoot_angle),DEGREES)
    #we shall create a statement that calcualted velocity based off of how much 
    # we calculate each percent changed the mm distance by.
 
      
    
# ----------------------- Autonomous Skills (ALEX) -----------------------
def autonomous_skills_alex():
    #Setting Velocities
    driveveloc(70)
    #Spinning 1
    while spinner_switch is False:
        drivetrain.drive(REVERSE)
    #Spinner 1 Completed
    spinner.spin_for(FORWARD,10,DEGREES)
    drivetrain.stop()
    #-------Spinner 2 Start---------
    #driving towards other spinner
    drivetrain.drive_for(FORWARD,10,INCHES) #modify this variable, again.
    #turning to align
    drivetrain.turn_for(RIGHT,90,DEGREES)
    #reversing until spinner contact
    while spinner_switch is False: 
        drivetrain.drive(REVERSE)
    #Correction amount
    drivetrain.set_drive_velocity((60,PERCENT))
    drivetrain.drive(REVERSE)
    spinner.spin_for(FORWARD,10,DEGREES)
    drivetrain.stop()
    #--------Spinner 2 Completed--------
    #Updating velocity move to other spinners
    driveveloc(100)
    #Aligning with the diagnal line
    drivetrain.turn_for(LEFT,45,DEGREES)
    #Driving enough to prepare for reverse enterence
    drivetrain.drive_for(FORWARD,5,INCHES)
    #Reversing (Sensors are on rear)
    drivetrain.turn_for(LEFT,360,DEGREES)
    #Reversing until something is detected
    while not(rear_distance.is_object_detected()):
        drivetrain.drive(REVERSE)
    #Reversing until near the things
    while rear_distance.object_distance(INCHES) > 15: #Again modify this variable to whatever fits
        drivetrain.drive(REVERSE)
        


# ----------------------- Autonomous Skills (Ryan)---------------------
def autonomous_skills():
    #Ryan - plz use comments to make this readable
    drivetrain.drive_for(REVERSE, 2, INCHES)
    spinner.spin_for(REVERSE, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 28, INCHES)
    drivetrain.turn_for(RIGHT, 90, DEGREES)
    drivetrain.drive_for(REVERSE, 32, INCHES)
    spinner.spin_for(REVERSE, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 65, INCHES) 
    drivetrain.turn_for(LEFT, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 88, INCHES)
    drivetrain.turn_for(LEFT, 90, DEGREES)
    drivetrain.drive_for(REVERSE, 58, INCHES)
    spinner.spin_for(REVERSE, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 30, INCHES)
    drivetrain.turn_for(LEFT, 90, DEGREES)
    drivetrain.drive_for(REVERSE, 32, INCHES)
    spinner.spin_for(REVERSE, 90, DEGREES)   


#--------------Version Developed Prior to Distance Sensor---------------
#def autonomous_long():
#    cprint(1,"Auton. ON (LONG)")
#    #           Autonomous Code
#    # -------------------------------------
#    drivetrain.set_drive_velocity(100, PERCENT)
#    drivetrain.set_turn_velocity(100, PERCENT)
#    ShooterGroup.set_velocity(100,PERCENT)
#    drivetrain.drive_for(FORWARD,20, INCHES)
#    drivetrain.set_turn_velocity(75,PERCENT)
#    drivetrain.turn_for(LEFT,90,DEGREES)
#    drivetrain.drive(REVERSE)
#    wait(2,SECONDS)
#    spinner.spin_for(REVERSE,100,DEGREES)
#    drivetrain.stop()
#    ShooterGroup.spin(FORWARD) 
#    wait(6, SECONDS)
#    pusher.set(True)
#    wait(2,SECONDS)
#    pusher.set(False)
#    cprint(1, 'Auton. Ended')
#    controller_1.rumble('--')
#    drivetrain.stop()
#    controller_1.screen.clear_row(1)


#Creating user_control function
def user_control():
    #initilizing full screen for text commands
    controller_1.screen.clear_screen()
    #setting shooter velocity variable to 75%
    s_velocity = 75
    #updating the shooter velocity after autonomous mode
    cprint(1, 'Shooter: Veloc: '+str(s_velocity)+'%')
    # place driver control in this while loop
    while True:
        #Print Motor Temperature Status
        #ShooterGroup
        bprint(1,'ShooterA Temp: '+str(ShooterGroup_motor_a.temperature(PERCENT))+ '%')
        bprint(2,'ShooterB Temp: '+str(ShooterGroup_motor_b.temperature(PERCENT))+'%')
        #Intake
        bprint(3,'Intake Temp: '+str(Intake.temperature(PERCENT))+'%')
        #Drivetrain
        bprint(4,'DrivetrainL1 Temp: '+str(left_motor_a.temperature(PERCENT))+'%')
        bprint(5,'DrivetrainL2 Temp: '+str(left_motor_b.temperature(PERCENT))+'%')
        bprint(6,'DrivetrainR1 Temp: '+str(right_motor_a.temperature(PERCENT))+'%')
        bprint(7,'DrivetrainR2 Temp: '+str(right_motor_b.temperature(PERCENT))+'%')
        #Spinner
        bprint(8,'Spinner Temp: '+str(spinner.temperature(PERCENT))+'%')
        bprint(9,'Spinner Temp: '+str(spinner.temperature(PERCENT))+'%')
        #Print Distance Sensor (For Debbuging)
        bprint(10, 'RearDistance: '+ str(rear_distance.object_distance(MM))+'mm')
        bprint(11, 'LeftDistance: '+ str(left_distance.distance(MM))+'mm')
        bprint(12, 'RightDistance: '+ str(right_distance.distance(MM))+'mm')
        #Update ShooterGroup Velocity
        ShooterGroup.set_velocity(int(s_velocity), PERCENT)
        #Setting Buttons
        if controller_1.buttonL1.pressing():
            cprint(2, 'Shooter: '+ str(round(((((ShooterGroup_motor_a.velocity(PERCENT)\
                *ShooterGroup_motor_b.velocity(PERCENT))/2)/s_velocity)*100))) +'%')
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
            cprint(1, 'Shooter: Veloc: '+str(s_velocity)+'%')
            controller_1.rumble(".")
            #ShooterGroup + 10
        if controller_1.buttonY.pressing() and (int(s_velocity) <= 90):
            s_velocity += 10
            #update status with text/vibration
            cprint(1, 'Shooter: Veloc: '+str(s_velocity)+'%')
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
        else:
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
            autonomous_long()

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


