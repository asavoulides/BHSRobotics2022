from vex import * 

# Brain should be defined by default
brain=Brain()

# Robot configuration code
#Left Drivetrain
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
#Left Group
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
#Right Drivetrain
right_motor_a = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
#Right Group
right_drive_smart = MotorGroup(right_motor_a,right_motor_b)
#Inertial
drivetrain_inertial = Inertial(Ports.PORT7)
#Drivetrain Declaration
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)
controller_1 = Controller(PRIMARY)
intake = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
spinner = Motor(Ports.PORT6, GearSetting.RATIO_6_1, False)
shooterA = Motor(Ports.PORT11, GearSetting.RATIO_6_1) #13 forward
shooterB = Motor(Ports.PORT12, GearSetting.RATIO_6_1,True) #14 reverse
shooter = MotorGroup(shooterA, shooterB)
#Phnumatics
expansion = DigitalOut(brain.three_wire_port.h)
# wait for rotation sensor to fully initialize
rear_distance = Distance(Ports.PORT20)
front_distance = Sonar(brain.three_wire_port.e)
left_distance = Sonar(brain.three_wire_port.c)
right_distance = Sonar(brain.three_wire_port.a)

drivetrain_should_stop = False
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
    if column == 1:
        brain.screen.clear_row(row)
    brain.screen.set_cursor(row, column)
    brain.screen.print(str(text))

#shooter Shooting Function
def disk_launch(percent, times):
    intake.set_velocity(100, PERCENT)
    for i in range(times):
        shooter.set_velocity(percent,PERCENT)
        shooter.spin(FORWARD)
        wait(3,SECONDS)
        intake.spin(REVERSE)
        wait(1,SECONDS)
        intake.stop()   

    shooter.stop()
    intake.stop()
    
#----------------PID----------------
def pid(expected,d_velocity=100):
    global drivetrain_should_stop
    drivetrain_should_stop = True
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
    drivetrain_should_stop = False
    cprint(2,'PID Completed')

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
    intake.spin_for(REVERSE,spinner_for,DEGREES)
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
    #updating intake status
    cprint(1,'Rotating Spinner')
    #spinning intake for 10 degrees
    intake.spin_for(REVERSE,spinner_for,DEGREES)
    drivetrain.stop()
    controller_1.screen.clear_screen()
      


     

s_velocity = 75

def driverControl():
    global s_velocity
    controller_1.screen.clear_screen()

    #Creating Threads to maximize efficency
    DrivetrainControl = Thread(drivetrainControl)
    InstrumentStatus = Thread(instrumentStatus)
    UserFeedback = Thread(userFeedback)
    cprint(1, 'Shooter: Veloc: '+str(s_velocity)+'%')
    while True: 
        shooter.set_velocity(s_velocity,PERCENT)
        #Shooter Spin Forward
        if controller_1.buttonL1.pressing():
            #Displaying the shooter Velocity on Screen
            shooter.spin(FORWARD)
            #Displaying the shooter Velocity on Screen
            cprint(2, 'Shooter: '+str(round((shooter.velocity(PERCENT)/s_velocity*100)))+'%')    
        else:
            controller_1.screen.clear_row(2)
            shooter.stop()            
            #shooter: - 10
        if controller_1.buttonA.pressing() and (int(s_velocity) >= 70):
            s_velocity -= 10
            rumble(".")
            cprint(1, 'Shooter: Veloc: '+str(s_velocity)+'%')
            #shooter: +5
        if controller_1.buttonX.pressing() and (int(s_velocity) <= 95):
            s_velocity += 5
            cprint(1, 'Shooter: Veloc: '+ str(s_velocity) +'%')
            rumble(".")
            #shooter + 10
        if controller_1.buttonY.pressing() and (int(s_velocity) <= 90):
            s_velocity += 10
            cprint(1, 'Shooter: Veloc: '+str(s_velocity)+ '%')
            rumble(".")
        if controller_1.buttonR1.pressing(): 
            intake.set_velocity(100, PERCENT)
            intake.spin(FORWARD)
        elif controller_1.buttonR2.pressing():
            intake.set_velocity(100,PERCENT)
            intake.spin(REVERSE)
        else:
            intake.stop()

        if controller_1.buttonLeft.pressing():
            spinner.set_velocity(100,PERCENT)
            spinner.spin(FORWARD)
        elif controller_1.buttonRight.pressing():
            spinner.set_velocity(100,PERCENT)
            spinner.spin(REVERSE)
        else:
            spinner.stop()

        if controller_1.buttonL2.pressing():
            pid(90)




        


def instrumentStatus():
    print("User Feedback Loop Ran Succesful")
    while True:
        wait(60,MSEC)
        #--- Instrument Status Print ---
        brain.screen.clear_screen()
        #Headers
        bprint(1,"--MOTORS--")
        bprint(1,"Temp. |", 13)
        bprint(1,"Pos. |", 20 )
        bprint(1,"Torque |",27)
        bprint(1,"Eff. |",37)
        bprint(1, "Port",44)

        #Column #1
        bprint(2,"Drive L : ")
        bprint(3,"Drive R : ")
        bprint(4,"ShooterA :")
        bprint(5,"ShooterB :")
        bprint(6,"Intake :")
        bprint(7, "Spinner: ")
        bprint(8,"--DISTANCE Sensors--")
        bprint(8, "Distance |",25)
        bprint(9, "Left Distance")
        bprint(10, "Right Distance")
        bprint(11, "Front Distance:")
        bprint(12, "Rear Distance:")       

        #Temperature
        left_group_temp = (left_motor_a.temperature(PERCENT) + (left_motor_b.temperature(PERCENT)))/2
        right_group_temp = (right_motor_a.temperature(PERCENT) + (right_motor_b.temperature(PERCENT)))/2
        bprint(2,str(left_group_temp)+"%", 13)
        bprint(3,str(right_group_temp)+"%", 13)
        bprint(4,str(shooterA.temperature(PERCENT))+"%", 13)
        bprint(5,str(shooterB.temperature(PERCENT))+"%", 13)
        bprint(6,str(intake.temperature(PERCENT))+"%", 13)
        bprint(7,str(spinner.temperature(PERCENT))+"%", 13)

        #Position
        bprint(2, "N/A",20)
        bprint(3, "N/A",20)
        bprint(4,str(round(shooterA.position(DEGREES))), 20)
        bprint(5,str(round(shooterB.position(DEGREES))), 20)
        bprint(6,str(round(intake.position(DEGREES))), 20)
        bprint(7,str(round(spinner.position(DEGREES))), 20)

        #Torque
        left_group_torque = (left_motor_a.torque(TorqueUnits.INLB) + left_motor_b.torque(TorqueUnits.INLB)) /2
        right_group_torque = (right_motor_a.torque(TorqueUnits.INLB) + right_motor_b.torque(TorqueUnits.INLB)) /2
        bprint(2,str(round(left_group_torque))+"INLB", 27)
        bprint(3,str(round(right_group_torque))+"INLB", 27)
        bprint(4,str(round(shooterA.torque(TorqueUnits.INLB)))+"INLB", 27)
        bprint(5,str(round(shooterB.torque(TorqueUnits.INLB)))+"INLB", 27)
        bprint(6,str(round(intake.torque(TorqueUnits.INLB)))+"INLB", 27)
        bprint(7,str(round(spinner.torque(TorqueUnits.INLB)))+"INLB", 27)

        #Efficency
        left_group_eff = (left_motor_a.efficiency(PERCENT) + left_motor_b.efficiency(PERCENT))/2
        right_group_eff = (right_motor_a.efficiency(PERCENT) + right_motor_b.efficiency(PERCENT))/2
        bprint(2,str(round(left_group_eff))+"%", 37)
        bprint(3,str(round(right_group_eff))+"%", 37)
        bprint(4,str(round(shooterA.efficiency(PERCENT)))+"%", 37)
        bprint(5,str(round(shooterB.efficiency(PERCENT)))+"%", 37)
        bprint(6,str(round(intake.efficiency(PERCENT)))+"%", 37)   
        bprint(7,str(round(spinner.efficiency(PERCENT)))+"%", 37)   


        #---Port---
        bprint(2,"1,19",44)
        bprint(3, "3,4",44)
        bprint(4, "11",44)
        bprint(5, "12",44)
        bprint(6,"5",44)
        bprint(7,"6",44)
        #---Distance Port---
        bprint(9,"C/E",44)
        bprint(10,"A/B",44)
        bprint(11,"E/F",44)
        bprint(12,"20",44)

        #---Distance---
        bprint(9, str(left_distance.distance(MM))+'mm',25)
        bprint(10,str(right_distance.distance(MM))+'mm',25)
        bprint(11, str(front_distance.distance(MM))+'mm',25)
        bprint(12, str(rear_distance.object_distance(MM))+'mm',25)




def userFeedback():
    print("UserFeedback Successful")
    while True:
        wait(600,MSEC)
        time_left = 105 - round(brain.timer.time(SECONDS))
            
        if time_left > 0:
            f_time = (105 - round(brain.timer.time(SECONDS)))

        else:
            f_time = round(brain.timer.time(SECONDS))

        if f_time < 10 and f_time > 0: 
            cprint(2,"Press B for Expansion")
            rumble("--")

        cprint(3, "Time: "+str(f_time)+"s")

        if (controller_1.buttonB.pressing()): #and f_time < 10 and f_time > 0):
            expansion.set(True)
            rumble("-")
            wait(5,SECONDS)
            expansion.set(False)



    
            
def drivetrainControl():
    print("Drivetrain Control Loop Succesful")
    global drivetrain_should_stop
    while True:
        left_speed = controller_1.axis3.position()
        right_speed = controller_1.axis2.position()

        if not(drivetrain_should_stop):
            left_drive_smart.set_velocity(left_speed,PERCENT)
            left_drive_smart.spin(FORWARD)

            right_drive_smart.set_velocity(right_speed, PERCENT)
            right_drive_smart.spin(FORWARD)



def pid_test():
    pid(90,100)
#--Competition Template--

comp = Competition(driverControl, pid_test)
preAutonomous()

