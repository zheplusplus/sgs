import core.src.ret_code as ret_code
from ext.src import game_init

from test_common import *

gc = game_init.statuses_mode(range(3))

last_event_id = 0
p0_events = gc.get_events(0, last_event_id)
p1_events = gc.get_events(1, last_event_id)
p2_events = gc.get_events(2, last_event_id)
assert_eq(1, len(p0_events))
assert_eq(1, len(p1_events))
assert_eq(1, len(p2_events))

event = p0_events[0]
assert_eq(3, event['players'])
assert_eq('GameInit', event['type'])
event = p1_events[0]
assert_eq(3, event['players'])
assert_eq('GameInit', event['type'])
event = p2_events[0]
assert_eq(3, event['players'])
assert_eq('GameInit', event['type'])

p0_position = p0_events[0]['position']
assert p0_position == 0 or p0_position == 1 or p0_position == 2

p1_position = p1_events[0]['position']
assert p1_position == 0 or p1_position == 1 or p1_position == 2

p2_position = p2_events[0]['position']
assert p2_position == 0 or p2_position == 1 or p2_position == 2

assert_eq(3, p0_position + p1_position + p2_position)

host_token = -1
other_token_a = -1
other_token_b = -1
if p0_position == 0:
    host_token = 0
    other_token_a = 1
    other_token_b = 2
    assert_eq(3, p1_position + p2_position)
if p1_position == 0:
    host_token = 1
    other_token_a = 0
    other_token_b = 2
    assert_eq(3, p0_position + p2_position)
if p2_position == 0:
    host_token = 2
    other_token_a = 0
    other_token_b = 1
    assert_eq(3, p0_position + p1_position)

last_event_id += 1

result = gc.hint(host_token)
assert_eq(ret_code.OK, result['code'])
assert_eq([0], result['players'])
assert_eq(3, len(result['candidate']))
select = result['candidate'][0]
assert_eq(ret_code.OK, result['code'])
assert_eq('_SelectCharacter', result['action'])

result = gc.hint(other_token_a)
assert_eq(ret_code.OK, result['code'])
assert_eq([0], result['players'])
assert not 'candidate' in result
assert_eq(ret_code.OK, result['code'])
assert_eq('_SelectCharacter', result['action'])

result = gc.hint(other_token_b)
assert_eq(ret_code.OK, result['code'])
assert_eq([0], result['players'])
assert not 'candidate' in result
assert_eq(ret_code.OK, result['code'])
assert_eq('_SelectCharacter', result['action'])

result = gc.player_act({
                           'token': host_token,
                           'select': select,
                       })
assert_eq(ret_code.OK, result['code'])

host_events = gc.get_events(host_token, last_event_id)
assert_eq(1, len(host_events))
if True: # just indent for a nice appearance
    event = host_events[0]
    assert_eq(0, event['player'])
    assert_eq(select, event['character'])
    assert_eq('SelectCharacter', event['type'])
other_events_a = gc.get_events(other_token_a, last_event_id)
assert_eq(host_events, other_events_a)
other_events_b = gc.get_events(other_token_b, last_event_id)
assert_eq(host_events, other_events_b)
last_event_id += 1

result = gc.hint(host_token)
assert_eq(ret_code.OK, result['code'])
assert_eq({1, 2}, set(result['players']))
assert not 'candidate' in result
assert_eq(ret_code.OK, result['code'])
assert_eq('_SelectCharacter', result['action'])

result = gc.hint(other_token_a)
assert_eq(ret_code.OK, result['code'])
assert_eq({1, 2}, set(result['players']))
assert_eq(3, len(result['candidate']))
select_a = result['candidate'][0]
assert_eq(ret_code.OK, result['code'])
assert_eq('_SelectCharacter', result['action'])

result = gc.hint(other_token_b)
assert_eq(ret_code.OK, result['code'])
assert_eq({1, 2}, set(result['players']))
assert_eq(3, len(result['candidate']))
select_b = result['candidate'][0]
assert_eq(ret_code.OK, result['code'])
assert_eq('_SelectCharacter', result['action'])

result = gc.player_act({
                           'token': other_token_a,
                           'select': select_a,
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.hint(host_token)
assert_eq(ret_code.OK, result['code'])
assert_eq(1, len(result['players']))
assert not 'candidate' in result
assert_eq(ret_code.OK, result['code'])
assert_eq('_SelectCharacter', result['action'])

result = gc.hint(other_token_a)
assert_eq(ret_code.OK, result['code'])
assert_eq(1, len(result['players']))
assert not 'candidate' in result
assert_eq(ret_code.OK, result['code'])
assert_eq('_SelectCharacter', result['action'])

result = gc.hint(other_token_b)
assert_eq(ret_code.OK, result['code'])
assert_eq(1, len(result['players']))
assert_eq(3, len(result['candidate']))
assert_eq(ret_code.OK, result['code'])
assert_eq('_SelectCharacter', result['action'])

host_events = gc.get_events(host_token, last_event_id)
assert_eq(0, len(host_events))
other_events_a = gc.get_events(other_token_a, last_event_id)
assert_eq(0, len(other_events_a))
other_events_b = gc.get_events(other_token_b, last_event_id)
assert_eq(0, len(other_events_b))

result = gc.player_act({
                           'token': other_token_b,
                           'select': select_b,
                       })
assert_eq(ret_code.OK, result['code'])

host_events = gc.get_events(host_token, last_event_id)
assert_eq(6, len(host_events))
if True: # just indent for a nice appearance
    event = host_events[0]
    assert_eq(1, event['player'])
    assert_eq('SelectCharacter', event['type'])
    event = host_events[1]
    assert_eq(2, event['player'])
    assert_eq('SelectCharacter', event['type'])
    event = host_events[2]
    assert_eq(0, event['player'])
    assert_eq(4, len(event['draw']))
    event = host_events[3]
    assert_eq(1, event['player'])
    assert_eq(4, event['draw'])
    event = host_events[4]
    assert_eq(2, event['player'])
    assert_eq(4, event['draw'])
    event = host_events[5]
    assert_eq(0, event['player'])
    assert_eq(2, len(event['draw']))
other_events_a = gc.get_events(other_token_a, last_event_id)
assert_eq(6, len(other_events_a))
if True: # just indent for a nice appearance
    assert_eq(host_events[0], other_events_a[0])
    assert_eq(host_events[1], other_events_a[1])
    event = other_events_a[2]
    assert_eq(0, event['player'])
    assert_eq(4, event['draw'])
    event = other_events_a[5]
    assert_eq(0, event['player'])
    assert_eq(2, event['draw'])
other_events_b = gc.get_events(other_token_b, last_event_id)
assert_eq(6, len(other_events_b))
if True: # just indent for a nice appearance
    assert_eq(host_events[0], other_events_b[0])
    assert_eq(host_events[1], other_events_b[1])
    event = other_events_b[2]
    assert_eq(0, event['player'])
    assert_eq(4, event['draw'])
    event = other_events_b[5]
    assert_eq(0, event['player'])
    assert_eq(2, event['draw'])

gc = game_init.statuses_mode(range(2))

p0_events = gc.get_events(0, 0)
host_token = p0_events[0]['position']
other_token = 1 - host_token

result = gc.player_act({
                           'token': other_token,
                           'select': 'Guo Jia',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

result = gc.player_act({
                           'token': host_token,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'select',
          }, result)

result = gc.player_act({
                           'token': host_token,
                           'select': '',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'select wrong character',
          }, result)

select = gc.hint(host_token)['candidate'][0]

result = gc.player_act({
                           'token': host_token,
                           'select': select,
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': host_token,
                           'select': select,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)
