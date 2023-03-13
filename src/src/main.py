from vex import *

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
drivetrain_inertial = Inertial(Ports.PORT7)
#Drivetrain Declaration
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)
controller_1 = Controller(PRIMARY)
spinner = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
intake = spinner
shooter = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
#Phnumatics
pusher = DigitalOut(brain.three_wire_port.a)
expansion = DigitalOut(brain.three_wire_port.b)
# wait for rotation sensor to fully initialize
rear_distance = Distance(Ports.PORT20)
left_distance = Sonar(brain.three_wire_port.e)
right_distance = Sonar(brain.three_wire_port.d)
wait(30, MSEC)

spinner_for: int = 100

def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    sleep(200, MSEC)
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)

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

#shooter Shooting Function
def disk_launch(percent, times):
    intake.set_velocity(100, PERCENT)
    intake.spin(FORWARD)
    for i in range(times):
        shooter.set_velocity(percent,PERCENT)
        shooter.spin(FORWARD)
        wait(3,SECONDS)
        pusher.set(False)
        wait(200,MSEC)
        pusher.set(True)
    shooter.stop()
    intake.stop()

def preAutonomous():
    calibrate_drivetrain()

def autonomous_short():
    global spinner_for 

    cprint(1, 'Auton. ON (SHORT)')
    while rear_distance.object_distance(MM) > 70: 
        drivetrain.drive(REVERSE)
    #Terminating reverse functions
    drivetrain.stop()
    #Rotating Spinner
    spinner.spin_for(REVERSE,spinner_for,DEGREES)
    #Driving Forward for Launch
    drivetrain.drive_for(FORWARD,50,MM)
    pid(90)
    disk_launch(80,2)
    wait(2,SECONDS)    

def autonomous_long():
    drivetrain.set_drive_velocity(60,PERCENT)
    #Updating status on screen utilizing cprint function
    cprint(1, "Auton. ON (LONG)")
    disk_launch(65,2)
    #Setting Velocities
    #Autonomous Program
    #While loop to reverse until distance sensor is roughly 700
    drivetrain.drive_for(REVERSE, 580, MM)
    #updating status on screen.
    cprint(1,'Turning To Roller')
    #turning right in preperation to get in contact with roller
    pid(90)
    #Updating status on screen
    cprint(1, 'Reversing To Roller')
    #Reversing to roller until the switch contact sensor detects contact
    while rear_distance.object_distance(MM) > 70: 
        drivetrain.drive(REVERSE)
    #updating spinner status
    cprint(1,'Rotating Spinner')
    #spinning spinner for 10 degrees
    spinner.spin_for(REVERSE,spinner_for,DEGREES)
    drivetrain.stop()
    controller_1.screen.clear_screen()
      

def autonomous_skills():
    global spinner_for

    pusher.set(True)
    intake.set_velocity(100,PERCENT)
    intake.spin(FORWARD)
    #Updating Velocities
    drivetrain.set_stopping(COAST)
    drivetrain.set_drive_velocity(60,PERCENT)
    #Reversing into Spinner #1
    while rear_distance.object_distance(MM) > 70: 
        drivetrain.drive(REVERSE)
    spinner.spin_for(FORWARD,spinner_for,DEGREES)
    drivetrain.stop()
    #Going Forwards; preparing to pid into Spinner #2
    while rear_distance.object_distance(MM) < 300:
        drivetrain.drive(FORWARD)
    drivetrain.stop()
    #Reversing into Spinner #2
    pid(90,70)
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
    pid(17,70)
    disk_launch(75,3)
    intake.spin(FORWARD)
    pid(73,70)
    #At Middle
    while rear_distance.object_distance(MM) > 700 or not(rear_distance.is_object_detected()):
        drivetrain.drive(REVERSE)
    drivetrain.stop()
    pid(90,70)
    #Going to Spinner #3
    while rear_distance.object_distance(MM) > 65: 
        drivetrain.drive(REVERSE)
    drivetrain.set_drive_velocity(50,PERCENT)
    spinner.spin_for(FORWARD,spinner_for,DEGREES)
    drivetrain.stop()
    drivetrain.set_drive_velocity(70,PERCENT)
    #Going to Spinner #4
    while rear_distance.object_distance(MM) < 300:
        drivetrain.drive(FORWARD)
    drivetrain.stop()
    pid(-90,70)
    while rear_distance.object_distance(MM) > 70: 
        drivetrain.drive(REVERSE)
    spinner.spin_for(FORWARD,spinner_for,DEGREES)
    drivetrain.stop()
    drivetrain.drive_for(FORWARD,5,INCHES)
    pid(45)
    expansion.set(True)
    wait(5,SECONDS)
    expansion.set(False)
    controller_1.screen.clear_screen()
    intake.stop()

#----------------PID----------------

def pid(expected,d_velocity=100):
    expected = (expected + drivetrain_inertial.rotation(DEGREES))

    wait(0.25, SECONDS)
    
    error = expected

    while True:
        actual = drivetrain_inertial.rotation(DEGREES)
        error = (expected - actual)
        speed = (error * 0.5) #Re-Adjust Variable through experimentation. 

        #---Velocity Updates---
        #LeftGroup 
        left_motor_a.set_velocity(speed,PERCENT)
        left_motor_b.set_velocity(speed,PERCENT)
        left_motor_c.set_velocity(speed,PERCENT)
        #RightGroup
        right_motor_a.set_velocity(-speed,PERCENT)
        right_motor_b.set_velocity(-speed,PERCENT)
        right_motor_c.set_velocity(-speed,PERCENT)
        
        #---Spinning---
        #LeftGroup Spin
        left_motor_a.spin(FORWARD)
        left_motor_b.spin(FORWARD)
        left_motor_c.spin(FORWARD)
        #RightGroup Spin
        right_motor_a.spin(FORWARD)
        right_motor_b.spin(FORWARD)
        right_motor_c.spin(FORWARD)
        cprint(2,str(error))

        if abs(error) < 2:
            break

        wait(0.15,SECONDS)
            
    drivetrain.stop()
    
    left_motor_a.set_velocity(d_velocity,PERCENT)
    left_motor_b.set_velocity(d_velocity,PERCENT)
    left_motor_c.set_velocity(d_velocity,PERCENT)
    right_motor_a.set_velocity(d_velocity,PERCENT)
    right_motor_b.set_velocity(d_velocity,PERCENT)
    right_motor_c.set_velocity(d_velocity,PERCENT)
    cprint(2,'PID Completed') 

s_velocity = 0 

def driverControl():

    global s_velocity
    
    userFeedbackThread = Thread(userFeedback) #Creating Threads to maximize efficency

    driveTrainControl = Thread(drivetrainControl)

    drivetrain.set_drive_velocity(100,PERCENT)

    while True: 
        if controller_1.buttonL1.pressing():
            #Displaying the shooter Velocity on Screen
            shooter.spin(FORWARD)
        else:
            controller_1.screen.clear_row(2)
            shooter.stop()            
            #shooter: - 10
        if controller_1.buttonA.pressing() and (int(s_velocity) >= 70):
            s_velocity -= 10
            #update status with text/vibration
            #shooter: +5
        if controller_1.buttonX.pressing() and (int(s_velocity) <= 95):
            s_velocity += 5
            #update status with text/vibration
            #shooter + 10
        if controller_1.buttonY.pressing() and (int(s_velocity) <= 90):
            s_velocity += 10
            #update status with text/vibration
        if controller_1.buttonR1.pressing(): 
            intake.set_velocity(100, PERCENT)
            intake.spin(FORWARD)
        elif controller_1.buttonR2.pressing():
            intake.set_velocity(100, PERCENT)
            intake.spin(REVERSE)
        else:
            intake.set_velocity(0, PERCENT)
        if controller_1.buttonDown.pressing():
            pusher.set(False)
        else:
            pusher.set(True)
        if controller_1.buttonLeft.pressing():
            spinner.set_velocity(100, PERCENT)
            spinner.spin(FORWARD)
        elif controller_1.buttonRight.pressing():
            spinner.spin(REVERSE)
        else:
            spinner.stop() 



def userFeedback():
    #Log Start:
    brain.timer.clear()
    #Initiate Full Screen
    controller_1.screen.clear_screen()
    #setting shooter velocity variable to 75%
    s_velocity = 75
    #updating the shooter velocity after autonomous mode
    cprint(1, 'Shooter: Veloc: '+str(s_velocity)+'%')
    #Drive Velocity
    while True:
        #--- Time Start ---
        time_left = 105 - round(brain.timer.time(SECONDS))

        if time_left > 0:
            f_time = (105 - round(brain.timer.time(SECONDS)))

        else:
            f_time = round(brain.timer.time(SECONDS))

        if f_time < 10 and f_time > 0: 
            rumble("---") #Calls rumble function which vibrates said 
            cprint(2,"Press B")

        cprint(3, "Time: "+str(f_time)+"s")
        #--- Time Function Over ---

        #--- Instrument Status Print ---
        bprint(1,"LeftA Temperature: "+ str(left_motor_a.temperature(PERCENT))+"%")
        bprint(2,"LeftB Temperature: "+ str(left_motor_b.temperature(PERCENT))+"%")
        bprint(3,"LeftC Temperature: "+ str(left_motor_c.temperature(PERCENT))+"%")
        bprint(4,"RightA Temperature: "+str(right_motor_a.temperature(PERCENT))+"%")
        bprint(5,"RightB Temperature: "+str(right_motor_b.temperature(PERCENT))+"%")
        bprint(6,"RightC Temperature: "+str(right_motor_c.temperature(PERCENT))+"%")
        bprint(7,"Shooter Temperature: "+str(shooter.temperature(PERCENT))+"%")
        bprint(8,"intake/Spinner Temperature: "+str(intake.temperature(PERCENT))+"%")
        bprint(9, 'RearDistance:'+str(rear_distance.object_distance(MM))+ 'mm')
        bprint(10, 'LeftDistance: '+ str(left_distance.distance(MM))+'mm')
        bprint(11, 'RightDistance: '+ str(right_distance.distance(MM))+'mm' )        
        #--- Instrument Status Print Over ---

        #----- Misceleanious -----

        #Shooter Velocity Update
        shooter.set_velocity(int(s_velocity), PERCENT)
    

        #--- Expansion Launch ---
        if (controller_1.buttonB.pressing() and f_time < 10 and f_time > 0):
            expansion.set(True)
            rumble("-")
            wait(5,SECONDS)
            expansion.set(False)

        #--- Shooter Velocity Print ---
        if controller_1.buttonL1.pressing():
            #Displaying the shooter Velocity on Screen
            cprint(2, 'Shooter: '+str(round((shooter.velocity(PERCENT)/s_velocity*100)))+'%')
        else:
            controller_1.screen.clear_row(2)      

        #--- ShooterGroup Velocity Updates --- 
        if controller_1.buttonA.pressing() and (int(s_velocity) >= 70):
            rumble(".")
            cprint(1, 'Shooter: Veloc: '+str(s_velocity)+'%')
        if controller_1.buttonX.pressing() and (int(s_velocity) <= 95):
            cprint(1, 'Shooter: Veloc: '+ str(s_velocity) +'%')
            rumble(".")
        if controller_1.buttonY.pressing() and (int(s_velocity) <= 90):
            cprint(1, 'Shooter: Veloc: '+str(s_velocity)+ '%')
            rumble(".")
        if controller_1.buttonDown.pressing():
            controller_1.rumble(".")
            
def drivetrainControl():
    while True:
        left_speed = controller_1.axis3.position()
        right_speed = controller_1.axis2.position()

        left_drive_smart.set_velocity(left_speed)
        left_drive_smart.spin(FORWARD)

        right_drive_smart.set_velocity(right_speed)
        right_drive_smart.spin(FORWARD)




#--Competition Template--

comp = Competition(driverControl, autonomous_short)
preAutonomous()