import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib

GpioPins = [18, 23, 24, 25]

# Declare a named instance of class pass a name and motor type
mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")


# call the function pass the parameters

#send 5 step signals 50 times in each direction.
for i in range(50):
    mymotortest.motor_run(GpioPins , .003, 5, False, False, "full", .05) # half is 12.54s
for i in range(50):
    mymotortest.motor_run(GpioPins , .003, 5, True, False, "full", .05) # full is 8.97s

# good practise to cleanup GPIO at some point before exit
GPIO.cleanup()
print("This Program Worked")
