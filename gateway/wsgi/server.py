import os
from wsgiref.simple_server import make_server
import simplejson

import core.src.ret_code as ret_code
import game
import static_files

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
    if path == '/':
        start_response('200 OK', [('Content-type', 'text/html')])
        return read_index()
    if path.startswith('/static/'):
        return static_files.serve(path[1:], start_response)
    if path == '/action':
        request_body_size = int(env['CONTENT_LENGTH'])
        request_body = env['wsgi.input'].read(request_body_size)
        response = game_response(request_body)
        RESPONSE_MAPPING[response['code']](start_response)
        return [simplejson.dumps(response)]
    RESPONSE_MAPPING[404](start_response)
    return ['']

def game_response(request_body):
    try:
        request_body = simplejson.loads(request_body)
        handlers = {
            'ctrl/add': game.game_room.add_player,
            'ctrl/exit': game.game_room.player_exit,
            'ctrl/start': game.game_room.start,
            'info/status': game.game_room.game_status,
            'info/events': game.game_room.get_events,
            'info/hint': game.game_room.get_hint,
            'info/checktoken': game.game_room.check_token,
            'act': game.game_room.player_act,
        }
        path = request_body['controller']
        if not path in handlers:
            return { 'code': 404 }
        return handlers[path](request_body)
    except ValueError, e:
        return {
                   'code': ret_code.BAD_REQUEST,
                   'reason': e.message,
               }
    except KeyError, e:
        return {
                   'code': ret_code.BAD_REQUEST,
                   'reason': ret_code.BR_MISSING_ARG % e.message,
               }
    except (NameError, SyntaxError), e:
        return {
                   'code': ret_code.BAD_REQUEST,
                   'reason': 'Syntax error: %s' % e.message,
               }

def read_index():
    path = os.path.join(os.path.dirname(__file__), 'static/index.html')
    with open(path) as f:
        return f.readlines()
