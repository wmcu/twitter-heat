'''
Simple server.
Usage:
python server.py
    Run in localhost:5000
python server.py deploy
    Run in localhost:80
'''


from application import application
from wsgiref.simple_server import make_server
from gevent.wsgi import WSGIServer
import sys


if __name__ == "__main__":

    if len(sys.argv) <= 1:
        port = 5000
    else:
        port = 80

    httpd = WSGIServer(('', port), application)
    # httpd = make_server('', port, application)
    print "Serving HTTP on port %s..." % port

    httpd.serve_forever()
