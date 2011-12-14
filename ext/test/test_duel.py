from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.src.player import Player

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('duel', 1, card.SPADE),
            test_data.CardInfo('fire attack', 2, card.HEART),
            test_data.CardInfo('slash', 3, card.DIAMOND),
            test_data.CardInfo('duel', 4, card.SPADE),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('fire attack', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('slash', 8, card.DIAMOND),

            test_data.CardInfo('duel', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.SPADE),
     ])), pc, ActionStack())
players = [Player(91, 0), Player(1729, 1)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [players[1].player_id],
        'cards': [0],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('duel', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('duel', event['use'][0]['name'])
    assert_eq(1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    assert_eq(0, event['use'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('duel', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('duel', event['use'][0]['name'])
    assert_eq(1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
last_event_id += 1

result = gc.player_act({
        'token': players[1].token,
        'play': [7],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('slash', event['play'][0]['name'])
    assert_eq(8, event['play'][0]['rank'])
    assert_eq(card.DIAMOND, event['play'][0]['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('slash', event['play'][0]['name'])
    assert_eq(8, event['play'][0]['rank'])
    assert_eq(card.DIAMOND, event['play'][0]['suit'])
    assert_eq(7, event['play'][0]['id'])
last_event_id += 1

result = gc.player_act({
        'token': players[0].token,
        'play': [2],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('slash', event['play'][0]['name'])
    assert_eq(3, event['play'][0]['rank'])
    assert_eq(card.DIAMOND, event['play'][0]['suit'])
    assert_eq(2, event['play'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('slash', event['play'][0]['name'])
    assert_eq(3, event['play'][0]['rank'])
    assert_eq(card.DIAMOND, event['play'][0]['suit'])
last_event_id += 1

result = gc.player_act({
        'token': players[1].token,
        'play': [],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('normal', event['category'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)
last_event_id += 1

result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [players[1].player_id],
        'cards': [0],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [players[1].player_id],
        'cards': [2],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [],
        'cards': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [players[0].player_id],
        'cards': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target self',
          }, result)

result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [players[0].player_id, players[1].player_id],
        'cards': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [players[1].player_id],
        'cards': [3],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('duel', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('duel', event['use'][0]['name'])
    assert_eq(4, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    assert_eq(3, event['use'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('duel', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('duel', event['use'][0]['name'])
    assert_eq(4, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
last_event_id += 1

result = gc.player_act({
        'token': players[0].token,
        'play': [9],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

result = gc.player_act({
        'token': players[1].token,
        'play': [9],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

result = gc.player_act({
        'token': players[1].token,
        'play': [7],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

result = gc.player_act({
        'token': players[1].token,
        'play': [4, 5],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
        'play': [4],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'token',
          }, result)

result = gc.player_act({
        'token': players[1].token,
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'play',
          }, result)

result = gc.player_act({
        'token': players[1].token,
        'play': [4],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('slash', event['play'][0]['name'])
    assert_eq(5, event['play'][0]['rank'])
    assert_eq(card.CLUB, event['play'][0]['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('slash', event['play'][0]['name'])
    assert_eq(5, event['play'][0]['rank'])
    assert_eq(card.CLUB, event['play'][0]['suit'])
    assert_eq(4, event['play'][0]['id'])
last_event_id += 1

result = gc.player_act({
        'token': players[0].token,
        'play': [],
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
last_event_id += 1

result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [],
        'cards': [8],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [players[0].player_id, players[1].player_id],
        'cards': [8],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [players[0].player_id],
        'cards': [8],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target self',
          }, result)

result = gc.player_act({
        'token': players[0].token,
        'action': 'duel',
        'targets': [players[1].player_id],
        'cards': [8],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('duel', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('duel', event['use'][0]['name'])
    assert_eq(9, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    assert_eq(8, event['use'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('duel', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('duel', event['use'][0]['name'])
    assert_eq(9, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
last_event_id += 1

result = gc.player_act({
        'token': players[1].token,
        'play': [],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('normal', event['category'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)
last_event_id += 1
