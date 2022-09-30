# imports
import RPi.GPIO as GPIO
import time
from ADCDevice import *

import mysql.connector as mysql
#import pandas as pd
import os 
from dotenv import load_dotenv

# obtain pulse time of a pin under timeOut
def pulseIn(pin,level,timeOut):
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0
    pulseTime = (time.time() - t0)*1000000
    return pulseTime

def Buzzer(distance):
    if distance > 0:
        GPIO.output(buzzerPin,GPIO.HIGH)
    else:
        GPIO.output(buzzerPin,GPIO.LOW)

 # get measurement of ultrasonic module, unit: cm
def getSonar():
    GPIO.output(trigPin, GPIO.HIGH)   # make trigPin output 10us HIGH level
    time.sleep(1)               # 1s
    GPIO.output(trigPin,GPIO.LOW)     # make trigPin output LOW level
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut) # read echoPin pulse time
    distance = pingTime*340.0/2.0/10000.0 # distance w/sound speed @ 340m/s
    return distance

def first_setup():
    GPIO.setmode(GPIO.BCM)     
    GPIO.setup(trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)    # set echoPin to INPUT mode
    GPIO.setup(buzzerPin, GPIO.OUT)

def second_setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
    GPIO.setmode(GPIO.BOARD)

def loops():
    first_setup()
    for i in range(10): # Runs this loop a certain number of times
        distance = getSonar() # get distance
        print("The distance is : %.2f cm" % (distance))
        query = "INSERT INTO sensor_data (sensor, distance) VALUES (%s, %s);"
        cursor.execute(query, ("ultra_sonic", distance)) # insert the type of sensor along with the distance
        Buzzer(distance)
        time.sleep(1)
    GPIO.cleanup()  # release GPIO resources
	
    second_setup()
    for i in range(10): # Runs this loop a certain number of times
        value = adc.analogRead(7)    # read the ADC value of channel 7
        voltage = value / 255.0 * 3.3
        print('ADC Value : %d, Voltage : %.2f'%(value, voltage))
        query = "INSERT INTO sensor_data (sensor, voltage) VALUES (%s, %s);"
        cursor.execute(query, ("photo_res", voltage)) # insert the type of sensor along with the voltage
        time.sleep(1)
    db.commit()
    GPIO.cleanup()  # release GPIO resources / says nothing to cleanup
    adc.close()
    

trigPin = 23
echoPin = 24
MAX_DISTANCE = 220          # define maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # calculate timeout w.r.t to maximum distance
buzzerPin= 6
adc = ADCDevice() # Define an ADCDevice class object

# grab credentials
load_dotenv('credentials.env')

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

db = mysql.connect(
    host = db_host,
    user = db_user,
    password = db_pass,
    database = db_name
)

if __name__ == '__main__': # Program entrance
    # create a new table
    cursor = db.cursor()
    cursor.execute("USE midterm;") # Why use Credentials.env

    cursor.execute("DROP TABLE IF EXISTS sensor_data;")
    cursor.execute(
        """CREATE TABLE sensor_data(
        id integer NOT NULL AUTO_INCREMENT primary key,
        sensor varchar(32),
        distance float(5, 2) DEFAULT NULL,
        voltage float(5, 2) DEFAULT NULL
        );"""
    )
    print("Program is starting!")
    try:
        loops()
    except KeyboardInterrupt: # Press CTRL-C to end the program
        db.commit()
        GPIO.cleanup()  # release GPIO resources
        adc.close()



