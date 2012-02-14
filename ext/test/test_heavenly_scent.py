from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player
import ext.src.skills.heavenly_scent as heavenly_scent

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('slash', 1, card.SPADE),
            test_data.CardInfo('rattan armor', 2, card.CLUB),
            test_data.CardInfo('slash', 3, card.HEART),
            test_data.CardInfo('slash', 4, card.HEART),

            test_data.CardInfo('rattan armor', 2, card.SPADE),
            test_data.CardInfo('fire attack', 6, card.HEART),
            test_data.CardInfo('fire attack', 7, card.HEART),
            test_data.CardInfo('duel', 8, card.HEART),

            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.CLUB),

            test_data.CardInfo('dodge', 11, card.HEART),
            test_data.CardInfo('dodge', 12, card.HEART),

            test_data.CardInfo('dodge', 13, card.DIAMOND),
            test_data.CardInfo('dodge', 1, card.DIAMOND),
            test_data.CardInfo('dodge', 2, card.DIAMOND),
            test_data.CardInfo('dodge', 3, card.DIAMOND),
     ])), pc, ActionStack())
players = [Player(91, 3), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
heavenly_scent.add_to(players[0])
gc.start()

# cards:
# name         | rank | id | suit

# slash        | 1    | 0  | SPADE <- discard this
# rattan armor | 2    | 1  | CLUB <- equip this
# slash        | 3    | 2  | HEART
# slash        | 4    | 3  | HEART
# slash        | 9    | 8  | SPADE <- discard this
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 4  | SPADE
# fire attack  | 6    | 5  | HEART
# fire attack  | 7    | 6  | HEART
# duel         | 8    | 7  | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [1],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'give up',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [0, 8],
                       })
assert_eq(ret_code.OK, result['code'])

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 1  | CLUB <- equipped
# slash        | 3    | 2  | HEART <- show this
# slash        | 4    | 3  | HEART
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 4  | SPADE
# fire attack  | 6    | 5  | HEART <- use this
# fire attack  | 7    | 6  | HEART
# duel         | 8    | 7  | HEART
# dodge        | 11   | 10 | HEART <- discard this
# dodge        | 12   | 11 | HEART
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [5],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'show': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'discard': [10],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [5],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'targets': [players[0].player_id],
                           'discard': [2],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target self',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'targets': map(lambda p: p.player_id, players),
                           'discard': [2],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'targets': [players[1].player_id],
                           'discard': [9],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'targets': [players[1].player_id],
                           'discard': [2, 3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

last_event_id = len(gc.get_events(players[0].token, 0)) # until discard a card
# cards:
# name         | rank | id | suit

# rattan armor | 2    | 1  | CLUB <- equipped
# slash        | 3    | 2  | HEART <- discard this
# slash        | 4    | 3  | HEART
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 4  | SPADE
# fire attack  | 7    | 6  | HEART
# duel         | 8    | 7  | HEART
# dodge        | 12   | 11 | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'targets': [players[1].player_id],
                           'discard': [2],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(3, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(1, len(event['discard']))
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(3, event['discard'][0]['rank'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
    assert_eq(2, event['discard'][0]['id'])
    event = p0_events[1]
    assert_eq(players[1].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('fire', event['category'])
    event = p0_events[2]
    assert_eq(1, event['draw'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(3, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(1, len(event['discard']))
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(3, event['discard'][0]['rank'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
    assert_eq(p0_events[1], p1_events[1])
    event = p1_events[2]
    assert_eq(1, len(event['draw']))
    assert_eq(13, event['draw'][0]['rank'])
    assert_eq(card.DIAMOND, event['draw'][0]['suit'])
    assert_eq('dodge', event['draw'][0]['name'])
    assert_eq(12, event['draw'][0]['id'])

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 1  | CLUB <- equipped
# slash        | 4    | 3  | HEART
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 4  | SPADE
# fire attack  | 7    | 6  | HEART
# duel         | 8    | 7  | HEART <- use this
# dodge        | 12   | 11 | HEART
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'duel',
                           'targets': [players[0].player_id],
                           'use': [7],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'method': 'give up',
                           'play': [],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until heavenly scent
result = gc.player_act({
                           'token': players[0].token,
                           'discard': [],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('normal', event['category'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 1  | CLUB <- equipped
# slash        | 4    | 3  | HEART <- show this
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 4  | SPADE <- equip this
# fire attack  | 7    | 6  | HEART <- use this
# dodge        | 12   | 11 | HEART <- discard this
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'equip',
                           'use': [4],
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
                           'show': [3],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'discard': [11],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until heavenly scent
# cards:
# name         | rank | id | suit

# rattan armor | 2    | 1  | CLUB <- equipped
# slash        | 4    | 3  | HEART <- discard this
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 4  | SPADE <- equipped
result = gc.player_act({
                           'token': players[0].token,
                           'targets': [players[1].player_id],
                           'discard': [3],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(3, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(1, len(event['discard']))
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(4, event['discard'][0]['rank'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
    assert_eq(3, event['discard'][0]['id'])
    event = p0_events[1]
    assert_eq(players[1].player_id, event['victim'])
    assert_eq(2, event['damage'])
    assert_eq('fire', event['category'])
    event = p0_events[2]
    assert_eq(3, event['draw'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(3, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(1, len(event['discard']))
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(4, event['discard'][0]['rank'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
    assert_eq(p0_events[1], p1_events[1])
    event = p1_events[2]
    assert_eq(3, len(event['draw']))
    assert_eq(1, event['draw'][0]['rank'])
    assert_eq(card.DIAMOND, event['draw'][0]['suit'])
    assert_eq('dodge', event['draw'][0]['name'])
    assert_eq(13, event['draw'][0]['id'])
    assert_eq(2, event['draw'][1]['rank'])
    assert_eq(card.DIAMOND, event['draw'][1]['suit'])
    assert_eq('dodge', event['draw'][1]['name'])
    assert_eq(14, event['draw'][1]['id'])
    assert_eq(3, event['draw'][2]['rank'])
    assert_eq(card.DIAMOND, event['draw'][2]['suit'])
    assert_eq('dodge', event['draw'][2]['name'])
    assert_eq(15, event['draw'][2]['id'])
