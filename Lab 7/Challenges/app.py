from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import os
from detector import get_text, detect_plate, detect_arizona, get_text_arizona
from PIL import Image
from datetime import datetime
import cv2

load_dotenv('credentials.env')
 
''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

car_photos = [
    {"id":1, "img_src": "Arizona_47.jpg"},
    {"id":2, "img_src": "Contrast.jpg"},
    {"id":3, "img_src": "Delaware_Plate.png"}
]

#reads photo id
def get_photo(req):
    idx = int(req.matchdict['photo_id'])-1
    return car_photos[idx]

#runs decector.py functions to get text from image
def get_the_text(req):
    print("start of code")
    idx = int(req.matchdict['read_text'])-1
    size = len(car_photos[idx]["img_src"])
    photo_name = car_photos[idx]["img_src"][:size - 4]
    file_name = car_photos[idx]["img_src"]
    print(file_name)
    

    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()
    
    image_url = "./public/images/" + file_name
    print(image_url)

    #special case for Arizona_47
    if (photo_name == "Arizona_47"):
        img = cv2.imread(image_url)
        result, location = detect_arizona(img)
        print("running arizona")
    else:
        img = cv2.imread(image_url,0)
        result, location = detect_plate(img)
    

    cv2.imwrite("./public/images/Result.png", result)

    #special case for Arizona_47
    the_result = Image.open("./public/images/Result.png")
    if (photo_name == "Arizona_47"):
        result_txt = get_text_arizona(the_result)
    else:
        result_txt = get_text(the_result)
    print(result_txt)

    #genrate timestamp
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)

    #insert detected plate text into mysql table
    query = "INSERT INTO Gallery_details (name, text, timestamp) VALUES (%s, %s, %s);"
    cursor.execute(query, (photo_name, result_txt, current_time))
    db.commit()
    print("Insert into database")

    if (photo_name == "Arizona_47"):
        cursor.execute('SELECT text FROM Gallery_details WHERE name = "Arizona_47";')
        record = cursor.fetchone()
    elif (photo_name == "Contrast"):
        cursor.execute('SELECT text FROM Gallery_details WHERE name = "Contrast";')
        record = cursor.fetchone()
    elif (photo_name == "Delaware_Plate"):
        cursor.execute('SELECT text FROM Gallery_details WHERE name = "Delaware_Plate";')
        record = cursor.fetchone()
    db.close()
    print(record)

    return record 
    
def index_page(req):
    return FileResponse("index.html")

#Rest routes
if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(index_page, route_name='home')

        config.add_route('photos', '/photos/{photo_id}')
        config.add_view(get_photo, route_name='photos', renderer='json')

        config.add_route('text', '/text/{read_text}')
        config.add_view(get_the_text, route_name='text', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()
        
    print("Server started on port 6453")
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()