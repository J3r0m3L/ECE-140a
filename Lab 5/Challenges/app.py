from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import os
 
load_dotenv('credentials.env')
 
''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

geisel_photos = [
    {"id":1, "img_src": "geisel-1.jpg"},
    {"id":2, "img_src": "geisel-2.jpg"},
    {"id":3, "img_src": "geisel-3.jpg"},
    {"id":4, "img_src": "geisel-4.jpg"},
    {"id":5, "img_src": "geisel-5.jpg"},
]

def return_photo(req):
    request = req.matchdict['id']
    request = request.split("-")



    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()
    if request[0] != 'NA' and request[2] != 'NA':
        cursor.execute("""SELECT id,name,owner,height,age FROM gallery_details WHERE 
            height >= %s AND 
            height < %s AND
            age >= %s AND 
            age < %s;""",
        (int(request[0]), int(request[1]), int(request[2]), int(request[3])))
    elif request[0] != 'NA':
        cursor.execute("""SELECT id,name,owner,height,age FROM gallery_details WHERE 
            height >= %s AND 
            height < %s;""",
        (int(request[0]), int(request[1])))
    elif request[2] != 'NA':
        cursor.execute("""SELECT id,name,owner,height,age FROM gallery_details WHERE 
            age >= %s AND 
            age < %s;""",
        (int(request[2]), int(request[3])))
    record = cursor.fetchone()
    db.close()

    #if no record found, return error json
    if record is None:
        return {
        'error' : "No data was found for the given ID" ,
        'id': "",
        'name' : "",
        'owner': "",
        'height': "",
        'age': ""
        }
    
    #populate json with values
    response = {
        'id':           record[0],
        'name':         record[1],
        'owner':        record[2],
        'height':       record[3],
        'age':          record[4]
    }
    
    return response


def get_home(req):
    return FileResponse("index.html")

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('return_photo','/photos/{id}')
        config.add_view(return_photo, route_name='return_photo', renderer='json')
  
        config.add_route('home', '/')
        config.add_view(get_home, route_name='home')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)

        app = config.make_wsgi_app()
 
server = make_server('0.0.0.0', 6543, app)
print('Web server started on: http://0.0.0.0:6543')
server.serve_forever()