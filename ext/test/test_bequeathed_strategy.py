from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player
import ext.src.skills.bequeathed_strategy as bequeathed_strategy

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('slash', 1, card.SPADE),
            test_data.CardInfo('rattan armor', 2, card.CLUB),
            test_data.CardInfo('fire attack', 3, card.HEART),
            test_data.CardInfo('slash', 4, card.HEART),

            test_data.CardInfo('dodge', 5, card.HEART),
            test_data.CardInfo('dodge', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.HEART),
            test_data.CardInfo('dodge', 8, card.HEART),

            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.CLUB),

            test_data.CardInfo('dodge', 11, card.HEART),
            test_data.CardInfo('dodge', 12, card.HEART),
            test_data.CardInfo('dodge', 13, card.HEART),
            test_data.CardInfo('duel', 1, card.DIAMOND),

            test_data.CardInfo('dodge', 2, card.DIAMOND),
            test_data.CardInfo('dodge', 3, card.DIAMOND),
     ])), pc, ActionStack())
players = [Player(91, 3), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
bequeathed_strategy.add_to(players[0])
gc.start()

# cards:
# name         | rank | id | suit

# slash        | 1    | 0  | SPADE <- show & discard this
# rattan armor | 2    | 1  | CLUB <- equip this
# fire attack  | 3    | 2  | HEART <- use this
# slash        | 4    | 3  | HEART
# slash        | 9    | 8  | SPADE
# slash        | 10   | 9  | CLUB

# dodge        | 5    | 4  | HEART
# dodge        | 6    | 5  | HEART
# dodge        | 7    | 6  | HEART
# dodge        | 8    | 7  | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [1],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [0],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until show a card

result = gc.player_act({
                           'token': players[0].token,
                           'method': 'discard',
                           'discard': [0],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(3, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq(1, event['discard'][0]['rank'])
    assert_eq(card.SPADE, event['discard'][0]['suit'])
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq('cards', event['discard'][0]['region'])
    assert_eq(0, event['discard'][0]['id'])
    event = p0_events[1]
    assert_eq(players[0].player_id, event['victim'])
    assert_eq(2, event['damage'])
    assert_eq('fire', event['category'])
    event = p0_events[2]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(2, len(event['draw']))
    assert_eq(11, event['draw'][0]['rank'])
    assert_eq(card.HEART, event['draw'][0]['suit'])
    assert_eq('dodge', event['draw'][0]['name'])
    assert_eq(10, event['draw'][0]['id'])
    assert_eq(12, event['draw'][1]['rank'])
    assert_eq(card.HEART, event['draw'][1]['suit'])
    assert_eq('dodge', event['draw'][1]['name'])
    assert_eq(11, event['draw'][1]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(3, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq(1, event['discard'][0]['rank'])
    assert_eq(card.SPADE, event['discard'][0]['suit'])
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq('cards', event['discard'][0]['region'])
    event = p1_events[1]
    assert_eq(players[0].player_id, event['victim'])
    assert_eq(2, event['damage'])
    assert_eq('fire', event['category'])
    event = p1_events[2]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(2, event['draw'])
last_event_id += 3

assert_eq({
              'code': ret_code.OK,
              'action': 'transfer',
              'transfer': {
                  10: {
                      'type': 'fix target',
                      'count': 1,
                      'candidates': [players[1].player_id],
                  },
                  11: {
                      'type': 'fix target',
                      'count': 1,
                      'candidates': [players[1].player_id],
                  },
              },
              'abort': 'allow',
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'transfer',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(2, len(event['draw']))
    assert_eq(13, event['draw'][0]['rank'])
    assert_eq(card.HEART, event['draw'][0]['suit'])
    assert_eq('dodge', event['draw'][0]['name'])
    assert_eq(12, event['draw'][0]['id'])
    assert_eq(1, event['draw'][1]['rank'])
    assert_eq(card.DIAMOND, event['draw'][1]['suit'])
    assert_eq('duel', event['draw'][1]['name'])
    assert_eq(13, event['draw'][1]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(2, event['draw'])
last_event_id += 1

assert_eq({
              'code': ret_code.OK,
              'action': 'transfer',
              'transfer': {
                  12: {
                      'type': 'fix target',
                      'count': 1,
                      'candidates': [players[1].player_id],
                  },
                  13: {
                      'type': 'fix target',
                      'count': 1,
                      'candidates': [players[1].player_id],
                  },
              },
              'abort': 'allow',
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'transfer',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))

result = gc.player_act({
                           'token': players[0].token,
                           'target': players[1].player_id,
                           'action': 'transfer',
                           'transfer': [13],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq('PrivateCardsTransfer', event['type'])
    assert_eq(players[0].player_id, event['source'])
    assert_eq(players[1].player_id, event['target'])
    assert_eq(1, len(event['transfer']))
    assert_eq(1, event['transfer'][0]['rank'])
    assert_eq(card.DIAMOND, event['transfer'][0]['suit'])
    assert_eq('duel', event['transfer'][0]['name'])
    assert_eq('bequeathed strategy', event['transfer'][0]['region'])
    assert_eq(13, event['transfer'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 1  | CLUB <- equipped
# slash        | 4    | 3  | HEART <- discard
# slash        | 9    | 8  | SPADE <- discard
# slash        | 10   | 9  | CLUB <- discard
# dodge        | 11   | 10 | HEART <- discard
# dodge        | 12   | 11 | HEART <- discard
# dodge        | 13   | 12 | HEART

# dodge        | 5    | 4  | HEART
# dodge        | 6    | 5  | HEART
# dodge        | 7    | 6  | HEART
# dodge        | 8    | 7  | HEART
# duel         | 1    | 13 | DIAMOND
result = gc.player_act({
                           'token': players[0].token,
                           'discard': [3, 8, 9, 10],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'must discard 5 cards',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [3, 8, 9, 10, 11],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'targets': [players[0].player_id],
                           'action': 'duel',
                           'use': [13],
                       })
assert_eq(ret_code.OK, result['code'])

# on error

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('slash', 1, card.SPADE),
            test_data.CardInfo('rattan armor', 2, card.CLUB),
            test_data.CardInfo('fire attack', 3, card.HEART),
            test_data.CardInfo('slash', 4, card.HEART),

            test_data.CardInfo('dodge', 5, card.HEART),
            test_data.CardInfo('dodge', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.HEART),
            test_data.CardInfo('dodge', 8, card.HEART),

            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.CLUB),

            test_data.CardInfo('dodge', 11, card.HEART),
            test_data.CardInfo('dodge', 12, card.HEART),
            test_data.CardInfo('dodge', 13, card.HEART),
            test_data.CardInfo('duel', 1, card.DIAMOND),

            test_data.CardInfo('peach', 2, card.DIAMOND),
            test_data.CardInfo('peach', 3, card.DIAMOND),
     ])), pc, ActionStack())
players = [Player(91, 3), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
bequeathed_strategy.add_to(players[0])
gc.start()

# cards:
# name         | rank | id | suit

# slash        | 1    | 0  | SPADE <- show & discard this
# rattan armor | 2    | 1  | CLUB <- equip this
# fire attack  | 3    | 2  | HEART <- use this
# slash        | 4    | 3  | HEART
# slash        | 9    | 8  | SPADE
# slash        | 10   | 9  | CLUB

# dodge        | 5    | 4  | HEART
# dodge        | 6    | 5  | HEART
# dodge        | 7    | 6  | HEART
# dodge        | 8    | 7  | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [1],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [0],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'method': 'discard',
                           'discard': [0],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'transfer': [10],
                           'target': players[1].player_id,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'action',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'transfer',
                           'transfer': [10],
                           'target': players[0].player_id,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target self',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'transfer',
                           'transfer': [1],
                           'target': players[1].player_id,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong region',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'transfer',
                           'transfer': [10],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'target',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'transfer',
                           'target': players[1].player_id,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'transfer',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'transfer',
                           'transfer': [9, 10],
                           'target': players[1].player_id,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong region',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'transfer',
                           'transfer': [14],
                           'target': players[1].player_id,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong region',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'transfer',
                           'transfer': [],
                           'target': players[1].player_id,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'bad cards',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'transfer',
                           'transfer': [11],
                           'target': players[1].player_id,
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'transfer',
                           'transfer': [10],
                           'target': players[1].player_id,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong region',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'transfer',
                           'transfer': [12, 13],
                           'target': players[1].player_id,
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])
