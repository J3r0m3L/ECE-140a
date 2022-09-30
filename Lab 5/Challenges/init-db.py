import mysql.connector as mysql
import pandas as pd
import os 
from dotenv import load_dotenv 

load_dotenv('credentials.env')

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

db = mysql.connect(
  host= db_host,
  user=db_user,
  password=db_pass,
  database=db_name
)

# Create Table
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS Gallery_details;")
cursor.execute(
    """CREATE TABLE Gallery_details(
    id integer NOT NULL AUTO_INCREMENT primary key,
    name varchar(32),
    owner varchar(48),
    height int,
    age int
    );"""
)

# Insert Values
details = pd.read_csv("./public/details.csv", index_col=False, delimiter=',')
listed_details = details.values.tolist()
for rows in listed_details:
    rows.pop(0)
print(listed_details)
query = "INSERT INTO Gallery_details (name, owner, height, age) VALUES (%s, %s, %s, %s)"
cursor.executemany(query, listed_details)
db.commit()