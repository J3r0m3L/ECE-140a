from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import FileResponse

def home_page(request):
    return FileResponse('index.html')

def music_page(request):
    return FileResponse('music.html')

def resume_page(request):
    return FileResponse('Jerome_Lam_Resume.pdf')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('music', '/music')

        config.add_view(home_page, route_name='home')
        config.add_view(music_page, route_name='music')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        config.add_static_view(name='/music', path='./public', cache_max_age=3600)

        app = config.make_wsgi_app()

    print("Server started on port 6453")
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()