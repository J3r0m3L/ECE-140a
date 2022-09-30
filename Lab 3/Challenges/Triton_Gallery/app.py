from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import FileResponse
import numpy as np
import cv2

geisel_photos = [
    {"id":1, "img_src": "geisel-1.jpg"},
    {"id":2, "img_src": "geisel-2.jpg"},
    {"id":3, "img_src": "geisel-3.jpg"},
    {"id":4, "img_src": "geisel-4.jpg"},
    {"id":5, "img_src": "geisel-5.jpg"},
]

def get_photo(req):
    idx = int(req.matchdict['photo_id'])-1
    return geisel_photos[idx]

def get_price(req):
    idx = int(req.matchdict['photo_id'])-1
    img2 = cv2.imread("./public/" + geisel_photos[idx]["img_src"])
    img2 = cv2.Canny(img2, 60, 200)
    # img median
    median_img2 = np.median(img2)
    
    # img mean
    mean_img2 = np.mean(img2)
    
    # img std
    std_img2 = np.std(img2)
    
    # img width
    width_img2 = img2[0, :].shape

    price_float = mean_img2 + (median_img2 * std_img2) + width_img2
    return int(price_float)


def index_page(req):
    return FileResponse("index.html")

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(index_page, route_name='home')

        config.add_route('photos', '/photos/{photo_id}')
        config.add_route('prices', '/prices/{photo_id}')
        config.add_view(get_photo, route_name='photos', renderer='json')
        config.add_view(get_price, route_name='prices', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()
    print("Server started on port 6453")
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()