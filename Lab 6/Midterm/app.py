from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse

import mysql.connector as mysql
from dotenv import load_dotenv
import os

import RPi.GPIO as GPIO
import time


def index_page(req):
    return FileResponse("index.html")

def select_sensor(req):
    sensor = int(req.matchdict['selected_name'])
    db = mysql.connect(host = db_host, user = db_user, password = db_pass, database = db_name)
    cursor = db.cursor()

    if (sensor == 1): # greater than or equal to 150cm
        cursor.execute("select * from sensor_data where sensor = 'ultra_sonic';")
        records = cursor.fetchall()
    elif (sensor == 2): # from 100cm (inclusive) to 150cm (exclusive)
        cursor.execute("select * from sensor_data where sensor = 'photo_res';")
        records = cursor.fetchall()

    db.close()
    return records

def select_distance(req):
    distance = int(req.matchdict['distance_range'])
    db = mysql.connect(host = db_host, user = db_user, password = db_pass, database = db_name)
    cursor = db.cursor()

    if (distance == 1): # greater than or equal to 150cm
        cursor.execute("select * from sensor_data where distance >= 150;")
        records = cursor.fetchall()
    elif (distance == 2): # from 100cm (inclusive) to 150cm (exclusive)
        cursor.execute("select * from sensor_data where distance >= 100 and distance < 150;")
        records = cursor.fetchall()
    elif (distance == 3): # from 50cm (inclusive) to 100cm (exclusive)
        cursor.execute("select * from sensor_data where distance >= 50 and distance < 100;")
        records = cursor.fetchall()
    elif (distance == 4): # from 0cm (inclusive) to 50cm (exclusive)
        cursor.execute("select * from sensor_data where distance >= 0 and distance < 50;")
        records = cursor.fetchall()
    else:
        cursor.execute("select * from sensor_data")
        records = cursor.fetchall()

    db.close()
    return records

def select_voltage(req):
    voltage = int(req.matchdict['voltage_range'])
    db = mysql.connect(host = db_host, user = db_user, password = db_pass, database = db_name)
    cursor = db.cursor()

    if (voltage == 1): # greater than or equal to 1v
        cursor.execute("select * from sensor_data where voltage >= 1;")
        records = cursor.fetchall()
    elif (voltage == 2): # from .75v (inclusive) to 1v (exclusive)
        cursor.execute("select * from sensor_data where voltage >= 0.75 and voltage < 1;")
        records = cursor.fetchall()
    elif (voltage == 3): # from .5v (inclusive) to .75v (exclusive)
        cursor.execute("select * from sensor_data where voltage >= 0.5 and voltage < 0.75;")
        records = cursor.fetchall()
    elif (voltage == 4): # from .25v (inclusive) to .5 (exclusive)
        cursor.execute("select * from sensor_data where voltage >= 0.25 and voltage < 0.5;")
        records = cursor.fetchall()
    elif (voltage == 5): # from 0v (inclusive) to .25 (exclusive)
        cursor.execute("select * from sensor_data where voltage >= 0 and voltage < 0.25;")
        records = cursor.fetchall()
    else:
        cursor.execute("select * from sensor_data")
        records = cursor.fetchall()


    db.close()
    return records

def select_sensor_distance(req):
    sensor_record = select_sensor(req)
    distance_record = select_distance(req)

    if sensor_record is None and distance_record is None:
        return {
        "error" :"No data was found for the given parameters.",
        "id" : "",
        "sensor" : "",
        "distance" : "",
        "voltage" : ""
        }
    response = {}
    # May Not Work
    for sensor_index, sensor_row in enumerate(sensor_record):
        for distance_index, distance_row in enumerate(distance_record):
            if (sensor_row[0] == distance_row[0]):
                response[sensor_index] = {
                    "id" : sensor_row[0],
                    "sensor" : sensor_row[1],
                    "distance" : sensor_row[2],
                    "voltage" : sensor_row[3]
                }
    return response
def select_sensor_voltage(req):
    sensor_record = select_sensor(req)
    voltage_record = select_voltage(req)

    if sensor_record is None and voltage_record is None:
        return {
        "error" : "No data was found for the given parameters.",
        "id" : "",
        "sensor" : "",
        "distance" : "",
        "voltage" : ""
        }
    response = {}
    # May Not Work
    for sensor_index, sensor_row in enumerate(sensor_record):
        for voltage_index, voltage_row in enumerate(voltage_record):
            if (sensor_row[0] == voltage_row[0]):
                response[sensor_index] = {
                    "id" : sensor_row[0],
                    "sensor" : sensor_row[1],
                    "distance" : sensor_row[2],
                    "voltage" : sensor_row[3]
                }
    return response

def sensor_any(req):
    pass

def select_all(req):

    distance_record = select_distance(req)
    voltage_record = select_voltage(req)



    if int(req.matchdict['distance_range']) == 5 and int(req.matchdict['voltage_range']) == 6:
        sensor_record =  select_sensor(req)
        response = {}
        for sensor_index, sensor_row in enumerate(sensor_record):
            response[sensor_index] = {
                "id" : sensor_row[0],
                "sensor" : sensor_row[1],
                "distance" : sensor_row[2],
                "voltage" : sensor_row[3]
            }
        return response


    elif int(req.matchdict['distance_range']) == 5 and int(req.matchdict['voltage_range']) != 6:
        return select_sensor_voltage(req)
    elif int(req.matchdict['distance_range']) != 5 and int(req.matchdict['voltage_range']) == 6:
        return select_sensor_distance(req)
    else:
        return {
            "error" : "No data was found for the given parameters.",
            "id" : "",
            "sensor" : "",
            "distance" : "",
            "voltage" : ""
        }

def select_distance_voltage(req):
    return {
        "error" : "No data was found for the given parameters.",
        "id" : "",
        "sensor" : "",
        "distance" : "",
        "voltage" : ""
    }

def buzz(req):
  	buzzerPin= 6
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzerPin, GPIO.OUT)
    GPIO.output(buzzerPin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(buzzerPin,GPIO.LOW)  
    return 0
    
# load database variables
load_dotenv('credentials.env')

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(index_page, route_name='home')

        # grab based off of sensor
        config.add_route('select_sensor', '/name/{selected_name}')
        config.add_view(select_sensor, route_name='select_sensor', renderer='json')

        # grab based off of distance
        config.add_route('select_distance', '/distance/{distance_range}')
        config.add_view(select_distance, route_name='select_distance', renderer='json')

        # grab based off of voltage
        config.add_route('select_voltage', '/voltage/{voltage_range}')
        config.add_view(select_voltage, route_name='select_voltage', renderer='json')

        # grab based off of sensor and distance
        config.add_route('select_sensor_distance', '/name/{selected_name}/distance/{distance_range}')
        config.add_view(select_sensor_distance, route_name='select_sensor_distance', renderer = 'json')

        # grab based off of sensor and voltage
        config.add_route('select_sensor_voltage', '/name/{selected_name}/voltage/{voltage_range}')
        config.add_view(select_sensor_voltage, route_name='select_sensor_voltage', renderer = 'json')

        # grab based off of distance and voltage
        config.add_route('select_distance_voltage', '/distance/{distance_range}/voltage/{voltage_range}')
        config.add_view(select_distance_voltage, route_name='select_distance_voltage', renderer = 'json')
        
        # buzz route
        config.add_route('buzz', '/buzzer')
        config.add_view(buzzer, route_name='buzz', renderer='json')

        # grab based off of all table columns
        config.add_route('select_all', '/name/{selected_name}/distance/{distance_range}/voltage/{voltage_range}')
        config.add_view(select_all, route_name='select_all', renderer = 'json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 6543, app)
    print('Web server started on: http://0.0.0.0:6543')
    server.serve_forever()
