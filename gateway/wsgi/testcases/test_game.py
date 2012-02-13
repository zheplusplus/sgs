from core.src import ret_code
from test_common import *

from .. import game

g = game.GameRoom()

result = g.response('/info/status', '')
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(0, result['players'])

result = g.response('/ctrl/add', 'alice')
assert_eq(ret_code.OK, result['code'])
tokena = result['token']

result = g.response('/info/status', '')
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(1, result['players'])

result = g.response('/ctrl/add', 'bob')
assert_eq(ret_code.OK, result['code'])
tokenb = result['token']

result = g.response('/info/status', '')
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(2, result['players'])

result = g.response('/ctrl/start', tokena)
assert_eq(ret_code.OK, result['code'])

result = g.response('/info/status', '')
assert_eq(ret_code.OK, result['code'])
assert_eq(1, result['started'])
assert_eq(2, result['players'])

result = g.response('/info/hint', '')
assert_eq(ret_code.OK, result['code'])

result = g.response('/info/hint', tokena)
assert_eq(ret_code.OK, result['code'])

result = g.response('/info/hint', tokenb)
assert_eq(ret_code.OK, result['code'])

result = g.response('/info/events', '''{
                                           'token': '%s',
                                           'previous event id': %d,
                                       }''' % (tokena, 0))
assert_eq(ret_code.OK, result['code'])

g = game.GameRoom()

result = g.response('/info/hint', tokenb)
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Game not started',
          }, result)

result = g.response('/ctrl/add', 'alice')
assert_eq(ret_code.OK, result['code'])
tokena = result['token']

result = g.response('/info/events', tokenb)
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Game not started',
          }, result)

result = g.response('/ctrl/start', tokena)
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Need at least 2 players',
          }, result)

result = g.response('/info/status', '')
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(1, result['players'])

result = g.response('/ctrl/add', 'bob')
assert_eq(ret_code.OK, result['code'])
tokenb = result['token']

result = g.response('/info/status', '')
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(2, result['players'])

result = g.response('/ctrl/start', tokenb)
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Not the host',
          }, result)

result = g.response('/info/status', '')
assert_eq(ret_code.OK, result['code'])
assert_eq(0, result['started'])
assert_eq(2, result['players'])

result = g.response('/info/hint', tokenb)
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Game not started',
          }, result)

g = game.GameRoom()

result = g.response('/ctrl/add', 'alice')
assert_eq(ret_code.OK, result['code'])
tokena = result['token']

result = g.response('/ctrl/add', 'bob')
assert_eq(ret_code.OK, result['code'])
tokenb = result['token']

result = g.response('/ctrl/exit', tokena)
assert_eq(ret_code.OK, result['code'])

result = g.response('/ctrl/exit', tokena)
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': 'Not joined in',
          }, result)

result = g.response('/ctrl/add', 'chiharaminori')
assert_eq(ret_code.OK, result['code'])
tokenc = result['token']

result = g.response('/ctrl/start', tokenb)
assert_eq(ret_code.OK, result['code'])

g = game.GameRoom()

result = g.response('/ctrl/add', 'alice')
assert_eq(ret_code.OK, result['code'])
tokena = result['token']

result = g.response('/ctrl/add', 'bob')
assert_eq(ret_code.OK, result['code'])
tokenb = result['token']

result = g.response('/ctrl/exit', tokena)
assert_eq(ret_code.OK, result['code'])

result = g.response('/ctrl/exit', tokenb)
assert_eq(ret_code.OK, result['code'])

result = g.response('/ctrl/add', 'david')
assert_eq(ret_code.OK, result['code'])
tokend = result['token']

result = g.response('/ctrl/add', 'emiri')
assert_eq(ret_code.OK, result['code'])
tokene = result['token']

result = g.response('/ctrl/start', tokend)
assert_eq(ret_code.OK, result['code'])
