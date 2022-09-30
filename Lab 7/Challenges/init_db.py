import mysql.connector as mysql
import os
from dotenv import load_dotenv #only required if using dotenv for creds
 
load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
 
db = mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Plate_Gallery;")
cursor.execute("USE Plate_Gallery;")
 
cursor.execute("DROP TABLE IF EXISTS Gallery_details;")
 
try:
  cursor.execute("""
    CREATE TABLE Gallery_details (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      name        VARCHAR(50) NOT NULL,
      text       VARCHAR(50) NOT NULL,    
      timestamp      VARCHAR(50) NOT NULL
    );
  """)
except RuntimeError as err:
  print("runtime error: {0}".format(err))
  
db.commit()