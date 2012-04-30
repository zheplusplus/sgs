import json

from core.src import ret_code
from test_common import *
from .. import server

def send_to_server(controller, data):
    data['controller'] = controller
    return server.game_response(json.dumps(data))

result = send_to_server('info/status', dict())
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(0, result['players'])

result = send_to_server('ctrl/add', { 'name': 'alice' })
assert_eq(ret_code.OK, result['code'])
tokena = result['token']

result = send_to_server('info/status', dict())
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(1, result['players'])

result = send_to_server('ctrl/add', { 'name': 'bob' })
assert_eq(ret_code.OK, result['code'])
tokenb = result['token']

result = send_to_server('info/status', dict())
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(2, result['players'])

result = send_to_server('ctrl/start', { 'token': tokena })
assert_eq(ret_code.OK, result['code'])

result = send_to_server('info/status', dict())
assert_eq(ret_code.OK, result['code'])
assert_eq(1, result['started'])
assert_eq(2, result['players'])

result = send_to_server('info/hint', { 'token': '' })
assert_eq(ret_code.OK, result['code'])

result = send_to_server('info/hint', { 'token': tokena })
assert_eq(ret_code.OK, result['code'])

result = send_to_server('info/hint', { 'token': tokenb })
assert_eq(ret_code.OK, result['code'])

result = send_to_server('info/events', {
                                           'token': tokena,
                                           'previous event id': 0,
                                       })
assert_eq(ret_code.OK, result['code'])

from .. import game

game.game_room = game.GameRoom()

result = send_to_server('info/hint', { 'token': tokenb })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Game not started',
          }, result)

result = send_to_server('ctrl/add', { 'name': 'alice' })
assert_eq(ret_code.OK, result['code'])
tokena = result['token']

result = send_to_server('info/events', { 'token': tokenb })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Game not started',
          }, result)

result = send_to_server('ctrl/start', { 'token': tokena })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Need at least 2 players',
          }, result)

result = send_to_server('info/status', dict())
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(1, result['players'])

result = send_to_server('ctrl/add', { 'name': 'bob' })
assert_eq(ret_code.OK, result['code'])
tokenb = result['token']

result = send_to_server('info/status', dict())
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(2, result['players'])

result = send_to_server('ctrl/start', { 'token': tokenb })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Not the host',
          }, result)

result = send_to_server('info/status', dict())
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(2, result['players'])

result = send_to_server('info/hint', { 'token': tokenb })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Game not started',
          }, result)

game.game_room = game.GameRoom()

result = send_to_server('ctrl/add', { 'name': 'alice' })
assert_eq(ret_code.OK, result['code'])
tokena = result['token']

result = send_to_server('ctrl/add', { 'name': 'bob' })
assert_eq(ret_code.OK, result['code'])
tokenb = result['token']

result = send_to_server('ctrl/exit', { 'token': tokena })
assert_eq(ret_code.OK, result['code'])

result = send_to_server('ctrl/exit', { 'token': tokena })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Not joined in',
          }, result)

result = send_to_server('ctrl/add', { 'name': 'chiharaminori' })
assert_eq(ret_code.OK, result['code'])
tokenc = result['token']

result = send_to_server('ctrl/start', { 'token': tokenb })
assert_eq(ret_code.OK, result['code'])

game.game_room = game.GameRoom()

result = send_to_server('ctrl/add', { 'name': 'alice' })
assert_eq(ret_code.OK, result['code'])
tokena = result['token']

result = send_to_server('ctrl/add', { 'name': 'bob' })
assert_eq(ret_code.OK, result['code'])
tokenb = result['token']

result = send_to_server('ctrl/exit', { 'token': tokena })
assert_eq(ret_code.OK, result['code'])

result = send_to_server('ctrl/exit', { 'token': tokenb })
assert_eq(ret_code.OK, result['code'])

result = send_to_server('ctrl/add', { 'name': 'david' })
assert_eq(ret_code.OK, result['code'])
tokend = result['token']

result = send_to_server('ctrl/add', { 'name': 'emiri' })
assert_eq(ret_code.OK, result['code'])
tokene = result['token']

result = send_to_server('ctrl/start', { 'token': tokend })
assert_eq(ret_code.OK, result['code'])

game.game_room = game.GameRoom()
for i in range(8):
    result = send_to_server('ctrl/add', { 'name': str(i) })
    assert_eq(ret_code.OK, result['code'])
result = send_to_server('ctrl/add', { 'name': 'x' })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'room full',
          }, result)
