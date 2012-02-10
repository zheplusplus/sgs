import os
from wsgiref.simple_server import make_server

import game

def start():
    make_server('', 8000, app).serve_forever()

def plain_headers():
    return [('Content-type', 'text/plain')]
RESPONSE_MAPPING = {
                       200: lambda sr: sr('200 OK', plain_headers()),
                       400: lambda sr: sr('400 Bad Request', plain_headers()),
                       404: lambda sr: sr('404 Not Found', plain_headers()),
                   }

def app(env, start_response):
    path = env['PATH_INFO']
    if '/' == path:
        start_response('200 OK', [('Content-type', 'text/html')])
        return read_index()
    request_body_size = int(env['CONTENT_LENGTH'])
    request_body = env['wsgi.input'].read(request_body_size)
    response = game.game_room.response(path, request_body)
    RESPONSE_MAPPING[response['code']](start_response)
    return [str(response)]

def read_index():
    path = os.path.join(os.path.dirname(__file__), 'htmls/index.html')
    with open(path) as f:
        return f.readlines()
