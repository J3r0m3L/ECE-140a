# Import WSGI ref for importing the serving library
from wsgiref.simple_server import make_server

# Configurator defines all the settings and configs in your web app
from pyramid.config import Configurator

# Response is used to respond to requests to the server
from pyramid.response import FileResponse

# The function is added as a view in the app.
# The response module returns the info to be shown on the webpage
def hello_world(request):
    print('Incoming request')
    return FileResponse('index.html') # the HTML file to be shown


# This line is to tell the interpreter to start execution from here
if __name__ == '__main__':

    # This is a common style to open an external class as an object
    with Configurator() as config:

   	    # Adds different routes possible in the website
        config.add_route('hello', '/')

    	# Directs the route to the function that can generate the view
        config.add_view(hello_world, route_name='hello')

        # Add static view
        config.add_static_view(name='/', path='./public', cache_max_age=3600)

    	# This is the overall compiled app with the given configurations
        app = config.make_wsgi_app()

	# This line is used to start serving on port 6543 on the localhost
    print("Server started on port 6453")
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
