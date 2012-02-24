from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player

from test_common import *
import test_data

players = [Player(19, 3), Player(91, 3), Player(1729, 3)]
pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('rattan armor', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.SPADE),
            test_data.CardInfo('slash', 3, card.HEART),
            test_data.CardInfo('peach', 4, card.HEART),

            test_data.CardInfo('slash', 5, card.HEART),
            test_data.CardInfo('fire attack', 6, card.HEART),
            test_data.CardInfo('fire attack', 7, card.HEART),
            test_data.CardInfo('peach', 8, card.HEART),

            test_data.CardInfo('peach', 9, card.HEART),
            test_data.CardInfo('peach', 10, card.HEART),
            test_data.CardInfo('peach', 11, card.HEART),
            test_data.CardInfo('peach', 12, card.HEART),

            test_data.CardInfo('slash', 13, card.SPADE),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('dodge', 2, card.HEART),
            test_data.CardInfo('dodge', 3, card.HEART),
     ])), pc, ActionStack())
map(lambda p: pc.add_player(p), players)
gc.start()

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 0  | CLUB <- equip this
# slash        | 2    | 1  | SPADE
# slash        | 3    | 2  | HEART
# peach        | 4    | 3  | HEART
# slash        | 13   | 12 | SPADE <- discard this
# slash        | 1    | 13 | CLUB  <- and this

# slash        | 5    | 4  | CLUB
# fire attack  | 6    | 5  | HEART
# fire attack  | 7    | 6  | HEART
# peach        | 8    | 7  | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [0],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [12, 13],
                       })
assert_eq(ret_code.OK, result['code'])

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 0  | CLUB <- equipped
# slash        | 2    | 1  | SPADE
# slash        | 3    | 2  | HEART <- show this
# peach        | 4    | 3  | HEART

# slash        | 5    | 4  | CLUB
# fire attack  | 6    | 5  | HEART <- use this
# fire attack  | 7    | 6  | HEART
# peach        | 8    | 7  | HEART
# dodge        | 2    | 14 | HEART <-discard this
# dodge        | 3    | 15 | HEART
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [5],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'discard': [14],
                       })
assert_eq(ret_code.OK, result['code'])

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 0  | CLUB <- equipped
# slash        | 2    | 1  | SPADE
# slash        | 3    | 2  | HEART <- show this
# peach        | 4    | 3  | HEART

# slash        | 5    | 4  | CLUB
# fire attack  | 7    | 6  | HEART <- use this
# peach        | 8    | 7  | HEART
# dodge        | 3    | 15 | HEART <- discard this
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [6],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'discard': [15],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until brink of death

assert_eq({
              'code': ret_code.OK,
              'action': 'discard',
              'players': [players[1].player_id],
          }, gc.hint(players[0].token))
assert_eq(gc.hint(players[0].token), gc.hint(players[2].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'discard',
              'methods': {
                             'peach': {
                                 'require': ['count', 'candidates'],
                                 'count': 1,
                                 'candidates': [7],
                             },
                         },
              'abort': 'allow',
              'players': [players[1].player_id],
          }, gc.hint(players[1].token))

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 0  | CLUB <- equipped
# slash        | 2    | 1  | SPADE
# slash        | 3    | 2  | HEART
# peach        | 4    | 3  | HEART

# slash        | 5    | 4  | CLUB
# peach        | 8    | 7  | HEART <- rescue
result = gc.player_act({
                           'token': players[1].token,
                           'method': 'peach',
                           'discard': [7],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq(8, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq('peach', event['play'][0]['name'])
    event = p0_events[1]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, event['point'])
    assert_eq('VigorRegain', event['type'])
p1_events = gc.get_events(players[1].token, last_event_id)
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq(8, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq('peach', event['play'][0]['name'])
    assert_eq(7, event['play'][0]['id'])
    assert_eq(p0_events[1], p1_events[1])
p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(p0_events, p2_events)
last_event_id += 2

assert_eq({
              'code': ret_code.OK,
              'action': 'discard',
              'players': [players[1].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'discard',
              'methods': {
                             'peach': {
                                 'require': ['count', 'candidates'],
                                 'count': 1,
                                 'candidates': [],
                             },
                         },
              'abort': 'allow',
              'players': [players[1].player_id],
          }, gc.hint(players[1].token))
assert_eq(gc.hint(players[0].token), gc.hint(players[2].token))

result = gc.player_act({
                           'token': players[2].token,
                           'method': 'peach',
                           'discard': [8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'peach',
                           'discard': [7],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

assert_eq({
              'code': ret_code.OK,
              'action': 'discard',
              'players': [players[2].player_id],
          }, gc.hint(players[0].token))
assert_eq(gc.hint(players[0].token), gc.hint(players[1].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'discard',
              'methods': {
                             'peach': {
                                 'require': ['count', 'candidates'],
                                 'count': 1,
                                 'candidates': [8, 9, 10, 11],
                             },
                         },
              'abort': 'allow',
              'players': [players[2].player_id],
          }, gc.hint(players[2].token))

result = gc.player_act({
                           'token': players[2].token,
                           'method': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 0  | CLUB <- equipped
# slash        | 2    | 1  | SPADE
# slash        | 3    | 2  | HEART
# peach        | 4    | 3  | HEART <- rescue

# slash        | 5    | 4  | CLUB
result = gc.player_act({
                           'token': players[0].token,
                           'method': 'peach',
                           'discard': [3],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq(4, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq('peach', event['play'][0]['name'])
    assert_eq(3, event['play'][0]['id'])
    event = p0_events[1]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, event['point'])
    assert_eq('VigorRegain', event['type'])
p1_events = gc.get_events(players[1].token, last_event_id)
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq(4, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq('peach', event['play'][0]['name'])
    assert_eq(p0_events[1], p1_events[1])
p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(p1_events, p2_events)

assert players[0].alive
assert players[1].alive
assert players[2].alive

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

# a player is killed

players = [Player(19, 3), Player(91, 3), Player(1729, 3)]
pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('rattan armor', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.SPADE),
            test_data.CardInfo('slash', 3, card.HEART),
            test_data.CardInfo('peach', 4, card.HEART),

            test_data.CardInfo('slash', 5, card.HEART),
            test_data.CardInfo('fire attack', 6, card.HEART),
            test_data.CardInfo('fire attack', 7, card.HEART),
            test_data.CardInfo('peach', 8, card.HEART),

            test_data.CardInfo('peach', 9, card.HEART),
            test_data.CardInfo('peach', 10, card.HEART),
            test_data.CardInfo('peach', 11, card.HEART),
            test_data.CardInfo('peach', 12, card.HEART),

            test_data.CardInfo('slash', 13, card.SPADE),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('dodge', 2, card.HEART),
            test_data.CardInfo('dodge', 3, card.HEART),
     ])), pc, ActionStack())
map(lambda p: pc.add_player(p), players)
gc.start()

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [0],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [12, 13],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [5],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'discard': [14],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [6],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'discard': [15],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[2].token,
                           'method': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until giving up
result = gc.player_act({
                           'token': players[0].token,
                           'method': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

assert not players[0].alive
assert players[1].alive
assert players[2].alive

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('PlayerKilled', event['type'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)
p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(p0_events, p2_events)

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

# fury pith after rescued

import ext.src.skills.fury_pith as fury_pith

players = [Player(19, 3), Player(91, 3), Player(1729, 3)]
fury_pith.add_to(players[1])
pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('rattan armor', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.SPADE),
            test_data.CardInfo('slash', 3, card.HEART),
            test_data.CardInfo('peach', 4, card.HEART),

            test_data.CardInfo('slash', 5, card.HEART),
            test_data.CardInfo('fire attack', 6, card.HEART),
            test_data.CardInfo('fire attack', 7, card.HEART),
            test_data.CardInfo('peach', 8, card.HEART),

            test_data.CardInfo('peach', 9, card.HEART),
            test_data.CardInfo('peach', 10, card.HEART),
            test_data.CardInfo('peach', 11, card.HEART),
            test_data.CardInfo('peach', 12, card.HEART),

            test_data.CardInfo('slash', 13, card.SPADE),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('dodge', 2, card.HEART),
            test_data.CardInfo('dodge', 3, card.HEART),
     ])), pc, ActionStack())
map(lambda p: pc.add_player(p), players)
gc.start()

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [0],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [12, 13],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [5],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'discard': [14],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [6],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'discard': [15],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[2].token,
                           'method': 'peach',
                           'discard': [8],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[2].token,
                           'method': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until the last peach
players[1].vigor -= 1 # manually decrease 1 vigor
result = gc.player_act({
                           'token': players[0].token,
                           'method': 'peach',
                           'discard': [3],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(3, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq(4, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq('peach', event['play'][0]['name'])
    assert_eq(3, event['play'][0]['id'])
    event = p0_events[1]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, event['point'])
    assert_eq('VigorRegain', event['type'])
    event = p0_events[2]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, event['point'])
    assert_eq('VigorRegain', event['type'])
p1_events = gc.get_events(players[1].token, last_event_id)
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq(4, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq('peach', event['play'][0]['name'])
    assert_eq(p0_events[1], p1_events[1])
    event = p1_events[2]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, event['point'])
    assert_eq('VigorRegain', event['type'])
p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(p1_events, p2_events)

assert players[0].alive
assert players[1].alive
assert players[2].alive

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])
