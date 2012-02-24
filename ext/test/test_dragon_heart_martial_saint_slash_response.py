from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player
import ext.src.skills.martial_saint as martial_saint
import ext.src.skills.dragon_heart as dragon_heart

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('duel', 1, card.SPADE),
            test_data.CardInfo('fire attack', 2, card.HEART),
            test_data.CardInfo('slash', 3, card.CLUB),
            test_data.CardInfo('duel', 4, card.SPADE),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('fire attack', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('slash', 8, card.DIAMOND),

            test_data.CardInfo('duel', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.SPADE),
     ])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
martial_saint.add_to(players[0])
dragon_heart.add_to(players[1])

gc.start()
last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

# cards:
# name        | rank (id = rank - 1) | suit

# duel        | 1                    | SPADE   <- use this to duel
# fire attack | 2                    | HEART
# slash       | 3                    | CLUB
# duel        | 4                    | SPADE
# duel        | 9                    | SPADE
# slash       | 10                   | SPADE

# slash       | 5                    | CLUB
# fire attack | 6                    | HEART
# dodge       | 7                    | DIAMOND
# slash       | 8                    | DIAMOND

result = gc.player_act({
                          'token': players[0].token,
                          'action': 'duel',
                          'targets': [players[1].player_id],
                          'use': [0],
                      })
assert_eq(ret_code.OK, result['code'])
last_event_id = len(gc.get_events(players[0].token, 0)) # until duel

result = gc.player_act({
                          'token': players[1].token,
                          'method': 'dragon heart',
                          'play': [7],
                      })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
                          'token': players[1].token,
                          'method': 'martial saint',
                          'play': [7],
                      })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'no such method',
          }, result)

assert_eq({
              'code': ret_code.OK,
              'action': 'PlayCards',
              'players': [players[1].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'PlayCards',
              'methods': {
                             'slash': {
                                 'require': ['count', 'candidates'],
                                 'count': 1,
                                 'candidates': [4, 7],
                             },
                             'dragon heart': {
                                 'require': ['count', 'candidates'],
                                 'count': 1,
                                 'candidates': [6],
                             },
                             'abort': {
                                 'require': ['count'],
                                 'count': 0,
                             },
                         },
              'players': [players[1].player_id],
          }, gc.hint(players[1].token))

# cards:
# name        | rank (id = rank - 1) | suit

# fire attack | 2                    | HEART
# slash       | 3                    | CLUB
# duel        | 4                    | SPADE
# duel        | 9                    | SPADE
# slash       | 10                   | SPADE

# slash       | 5                    | CLUB
# fire attack | 6                    | HEART
# dodge       | 7                    | DIAMOND <- dragon heart play a dodge
# slash       | 8                    | DIAMOND
result = gc.player_act({
                          'token': players[1].token,
                          'method': 'dragon heart',
                          'play': [6],
                      })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('dodge', event['play'][0]['name'])
    assert_eq(7, event['play'][0]['rank'])
    assert_eq(card.DIAMOND, event['play'][0]['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('dodge', event['play'][0]['name'])
    assert_eq(7, event['play'][0]['rank'])
    assert_eq(card.DIAMOND, event['play'][0]['suit'])
    assert_eq(6, event['play'][0]['id'])
last_event_id += 1

result = gc.player_act({
                          'token': players[0].token,
                          'method': 'dragon heart',
                          'play': [3],
                      })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'no such method',
          }, result)

result = gc.player_act({
                          'token': players[0].token,
                          'method': 'martial saint',
                          'play': [3],
                      })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

assert_eq({
              'code': ret_code.OK,
              'action': 'PlayCards',
              'methods': {
                             'slash': {
                                 'require': ['count', 'candidates'],
                                 'count': 1,
                                 'candidates': [2, 9],
                             },
                             'martial saint': {
                                 'require': ['count', 'candidates'],
                                 'count': 1,
                                 'candidates': [1],
                             },
                             'abort': {
                                 'require': ['count'],
                                 'count': 0,
                             },
                         },
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'PlayCards',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))

# cards:
# name        | rank (id = rank - 1) | suit

# fire attack | 2                    | HEART <- dragon heart play a red card
# slash       | 3                    | CLUB
# duel        | 4                    | SPADE
# duel        | 9                    | SPADE
# slash       | 10                   | SPADE

# slash       | 5                    | CLUB
# fire attack | 6                    | HEART
# slash       | 8                    | DIAMOND
result = gc.player_act({
                          'token': players[0].token,
                          'method': 'martial saint',
                          'play': [1],
                      })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('fire attack', event['play'][0]['name'])
    assert_eq(2, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq(1, event['play'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('fire attack', event['play'][0]['name'])
    assert_eq(2, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
last_event_id += 1

# cards:
# name        | rank (id = rank - 1) | suit

# slash       | 3                    | CLUB    <- slash this
# duel        | 4                    | SPADE
# duel        | 9                    | SPADE
# slash       | 10                   | SPADE

# slash       | 5                    | CLUB
# fire attack | 6                    | HEART
# slash       | 8                    | DIAMOND <- slash this
result = gc.player_act({
                          'token': players[1].token,
                          'method': 'slash',
                          'play': [7],
                      })
assert_eq(ret_code.OK, result['code'])
result = gc.player_act({
                          'token': players[0].token,
                          'method': 'slash',
                          'play': [2],
                      })
assert_eq(ret_code.OK, result['code'])
