import os
from wsgiref.simple_server import make_server

def start():
    make_server('', 8000, app).serve_forever()

def response_ok(start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])

def response_bad_request(start_response):
    start_response('400 Bad Request', [('Content-type', 'text/plain')])

def app(env, start_response):
    path = env['PATH_INFO']
    if '/' == path:
        response_ok(start_response)
        return read_index()
    if '/act' == path:
        response_body = ''
        try:
            request_body_size = int(env['CONTENT_LENGTH'])
            request_body = env['wsgi.input'].read(request_body_size)
            response_ok(start_response)
        except Exception, e:
            response_bad_request(start_response)
            request_body = e.message
        return [response_body]
    start_response('404 Not Found', [('content-type', 'text/html')])
    return []

def read_index():
    path = os.path.join(os.path.dirname(__file__), 'htmls/index.html')
    with open(path) as f:
        return f.readlines()
