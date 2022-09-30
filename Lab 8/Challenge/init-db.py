import mysql.connector as mysql
import os
from dotenv import load_dotenv

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

db = mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS final;")
cursor.execute("USE final;")

cursor.execute("DROP TABLE IF EXISTS objects;")
cursor.execute("DROP TABLE IF EXISTS found_objects")

try:
    cursor.execute("""
        CREATE TABLE objects (
        id          integer  AUTO_INCREMENT PRIMARY KEY,
        hsv        VARCHAR(100) NOT NULL,
        contours       VARCHAR(100) NOT NULL,    
        size      VARCHAR(100) NOT NULL
    );
    """)
    query = "INSERT INTO objects (hsv, contours, size) VALUES (%s, %s, %s);"
    cursor.execute(query, ("50, 150, 20 - 60, 255, 255 - 60,100,20 - 70,255,255", "0,0-0,40-50,0-50,40", "50,40")) # Red
    cursor.execute(query, ("0, 150, 20 - 10, 255, 255 - 160,100,20 - 179,255,255", "0,0-0,80-105,0, 105,80", "105,80")) # Green
    cursor.execute(query, ("110, 150, 20 - 120, 255, 255 - 120,100,20 - 130, 255, 255", "0,0-100,0-0,100-100,100", "100,100")) # Blue

except RuntimeError as err:
    print("runtime error: {0}".format(err))

try:
    cursor.execute("""
        CREATE TABLE found_objects (
        id          integer  AUTO_INCREMENT PRIMARY KEY,
        object_name        VARCHAR(50) NOT NULL,
        address       VARCHAR(50) NOT NULL
    );
    """)
except RuntimeError as err:
    print("runtime error: {0}".format(err))

db.commit()