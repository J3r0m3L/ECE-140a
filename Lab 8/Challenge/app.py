import numpy as np
import cv2
import os
import RPi.GPIO as GPIO
import time
import serial               #import serial package
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package
from dotenv import load_dotenv
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from RpiMotorLib import RpiMotorLib
from GPS import GPS_Info
#import GPS
counter = 0
object_found = False

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

objects = [
    {"id":1, "object_name": "red"},
    {"id":2, "object_name": "green"},
    {"id":3, "object_name": "blue"}
]

def find_object(req):
    object = int(req.matchdict['find_obj'])
    print(object)
    # object detection
    global counter
    #video capture likely to be 0 or 1
    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    #Stepper Motor Setup
    GpioPins = [18, 23, 24, 25]

    # Declare a named instance of class pass a name and motor type
    mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")

    while True:
        
        _,frame=cap.read()

        #convert to hsv deals better with lighting
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        if object == 1: # Red
            lower1 = np.array([00, 150, 20])
            upper1 = np.array([10, 255, 255])
            lower2 = np.array([160,100,20])
            upper2 = np.array([179,255,255])
            
        elif object == 2: # Green
            lower1 = np.array([50, 150, 20])
            upper1 = np.array([60, 255, 255])
            lower2 = np.array([60,100,20])
            upper2 = np.array([70,255,255])
            
        elif object == 3: # Blue
            lower1 = np.array([110, 150, 20])
            upper1 = np.array([120, 255, 255])
            lower2 = np.array([120, 100, 20])
            upper2 = np.array([130, 255, 255])
        
        #masks input image with upper and lower red ranges
        color_only1 = cv2.inRange(hsv, lower1, upper1)
        color_only2 = cv2.inRange(hsv, lower2 , upper2)
        
        color_only = color_only1 + color_only2
        
        mask=np.ones((5,5),np.uint8)
        
        
        #run an opening to get rid of any noise
        opening=cv2.morphologyEx(color_only,cv2.MORPH_OPEN,mask)

        #run connected components algo to return all objects it sees.
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opening,4, cv2.CV_32S)
        b=np.matrix(labels)
        if num_labels > 1:
            coordinates = get_coords()
            return coordinates
        
        
        if counter < 50:
            mymotortest.motor_run(GpioPins , .003, 5, False, False, "full", .05)
        elif counter >= 50:
            mymotortest.motor_run(GpioPins , .003, 5, True, False, "full", .05)
        
        counter += 1
        
        if counter == 100:
            counter = 0
        
            

    GPIO.cleanup()
    print("This Program Worked")
    return True

def pid_tracking(req):
    
    object = int(req.matchdict['object'])
    print(object)
    
    #video capture likely to be 0 or 1
    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    #Stepper Motor Setup
    GpioPins = [18, 23, 24, 25]

    # Declare a named instance of class pass a name and motor type
    mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
    #min time between motor steps (ie max speed)
    step_time = .002

    #PID Gain Values (these are just starter values)
    Kp = 0.003
    Kd = 0.0001
    Ki = 0.00015

    #error values
    d_error = 0
    last_error = 0
    sum_error = 0

    frames = 0
    

    while True:
        _,frame=cap.read()
        
        frames += 1

        #convert to hsv deals better with lighting
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
        if object == 1: # Red
            lower1 = np.array([0, 150, 20])
            upper1 = np.array([10, 255, 255])
            lower2 = np.array([160,100,20])
            upper2 = np.array([179,255,255])
            
        elif object == 2: # Green
            lower1 = np.array([50, 150, 20])
            upper1 = np.array([60, 255, 255])
            lower2 = np.array([60,100,20])
            upper2 = np.array([70,255,255])
            
        elif object == 3: # Blue
            lower1 = np.array([110, 150, 20])
            upper1 = np.array([120, 255, 255])
            lower2 = np.array([120, 100, 20])
            upper2 = np.array([130, 255, 255])
        
        #masks input image with upper and lower red ranges
        color_only1 = cv2.inRange(hsv, lower1, upper1)
        color_only2 = cv2.inRange(hsv, lower2 , upper2)
        
        color_only = color_only1 + color_only2
        
        mask=np.ones((5,5),np.uint8)
        
        
        #run an opening to get rid of any noise
        opening=cv2.morphologyEx(color_only,cv2.MORPH_OPEN,mask)
        

        #run connected components algo to return all objects it sees.
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opening,4, cv2.CV_32S)
        b=np.matrix(labels)
        if num_labels > 1:
            start = time.time()
            #extracts the label of the largest none background component and displays distance from center and image.
            max_label, max_size = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key = lambda x: x[1])
            Obj = b == max_label
            Obj = np.uint8(Obj)
            Obj[Obj > 0] = 255
            
            #calculate error from center column of masked image
            error = -1 * (320 - centroids[max_label][0])
            
            #speed gain calculated from PID gain values
            speed = Kp * error + Ki * sum_error + Kd * d_error
            
            #if negative speed change direction
            if speed < 0:
                direction = False
            else:
                direction = True
            
            #inverse speed set for multiplying step time (lower step time = faster speed)
            speed_inv = abs(1/(speed))
            
            #get delta time between loops
            delta_t = time.time() - start
            #calculate derivative error
            d_error = (error - last_error)/delta_t
            #integrated error
            sum_error += (error * delta_t)
            last_error = error
            
            #buffer of 20 only runs within 20
            if abs(error) > 20:
                mymotortest.motor_run(GpioPins , speed_inv * step_time, 1, direction, False, "full", .05)
            else:
                #run 0 steps if within an error of 20
                mymotortest.motor_run(GpioPins , step_time, 0, direction, False, "full", .05)
            
        else:
            print("broken")
            break
            

        k=cv2.waitKey(5)
        if k==27:
            break

    cv2.destroyAllWindows()
    GPIO.cleanup()


def get_coords():
#     lat_in_degrees, long_in_degrees = GPS_Info()
#     coords = "lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n'
    coords = "Lat in degrees: 32.879461, long in degrees: -117.236036" #GPS was not working after 3 hours, hard coded previously found values
    
    return coords


def store_coords(req):
    value = req.matchdict['obj_coord']
    item = int(value[0]) - 1
    coord = str(value[1:len(value)])

    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()

    cursor.execute("USE final;")
    query = "INSERT INTO found_objects (object_name, address) VALUES (%s, %s);"
    cursor.execute(query, (objects[item]["object_name"], coord))
    print(objects[item])

    db.commit()
    return 0

#def save_coords(req):
 #   id = int(req.matchdict['obj_coord'])
  #  object_name = objects[id]["object_name"]

   # address = get_coords()

    #db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    #cursor = db.cursor()

    #insert detected plate text into mysql table
    #query = "INSERT INTO objects (id, object_name, address) VALUES (%s, %s, %s);"
    #cursor.execute(query, (id, object_name, address))
    #db.commit()
    #print("Inserted into database")

def index_page(req):
    return FileResponse("index.html")

#Rest routes
if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(index_page, route_name='home')

        config.add_route('find_object', '/find_object/{find_obj}')
        config.add_view(find_object, route_name='find_object', renderer='json')
        
        config.add_route('pid_tracking', '/pid_tracking/{object}')
        config.add_view(pid_tracking, route_name='pid_tracking', renderer='json')

        config.add_route('store_coords', '/store_coords/{obj_coord}')
        config.add_view(store_coords, route_name='store_coords', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()
        
    print("Server started on port 6453")
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()