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
            test_data.CardInfo('slash', 1, card.SPADE),
            test_data.CardInfo('fire attack', 2, card.HEART),
            test_data.CardInfo('dodge', 3, card.DIAMOND),
            test_data.CardInfo('fire attack', 4, card.HEART),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('fire attack', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('dodge', 8, card.DIAMOND),

            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.SPADE),

            test_data.CardInfo('dodge', 11, card.HEART),
            test_data.CardInfo('dodge', 12, card.DIAMOND),
     ])), pc, ActionStack())
players = [Player(91, 0), Player(1729, 1)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'cards': [1],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('fire attack', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('fire attack', event['use'][0]['name'])
    assert_eq(2, event['use'][0]['rank'])
    assert_eq(card.HEART, event['use'][0]['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
last_event_id += 1

result = gc.player_act({
        'token': players[1].token,
        'show': [6],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player_id'])
    assert_eq(1, len(event['show']))
    assert_eq('dodge', event['show'][0]['name'])
    assert_eq(7, event['show'][0]['rank'])
    assert_eq(card.DIAMOND, event['show'][0]['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
last_event_id += 1

result = gc.player_act({
        'token': players[0].token,
        'discard': [2],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player_id'])
    assert_eq(1, len(event['discard']))
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(3, event['discard'][0]['rank'])
    assert_eq(card.DIAMOND, event['discard'][0]['suit'])
if True: # just indent for a nice appearance
    event = p0_events[1]
    assert_eq(players[1].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('fire', event['category'])
p1_events = gc.get_events(players[1].token, last_event_id)
last_event_id += 2

result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'cards': [0],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'cards': [5],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'cards': [],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'cards': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'targets',
          }, result)
result = gc.player_act({
        'token': players[1].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'cards': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'cards': [1],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [],
        'cards': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id, players[0].player_id],
        'cards': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'cards': [3],
    })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
        'token': players[0].token,
        'show': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)
result = gc.player_act({
        'token': players[1].token,
        'show': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[1].token,
        'show': [5, 6],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[1].token,
        'show': [],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
        'token': players[1].token,
        'show': [6],
    })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
        'token': players[1].token,
        'discard': [6],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'discard': [1],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'discard': [0],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'discard': [2],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'discard': [0, 2],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'discard': [],
    })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('fire attack', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('fire attack', event['use'][0]['name'])
    assert_eq(4, event['use'][0]['rank'])
    assert_eq(card.HEART, event['use'][0]['suit'])
if True: # just indent for a nice appearance
    event = p0_events[1]
    assert_eq(players[1].player_id, event['player_id'])
    assert_eq(1, len(event['show']))
    assert_eq('dodge', event['show'][0]['name'])
    assert_eq(7, event['show'][0]['rank'])
    assert_eq(card.DIAMOND, event['show'][0]['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
last_event_id += 2

result = gc.player_act({
        'token': players[0].token,
        'discard': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'action',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'give up',
    })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
        'token': players[0].token,
        'discard': [],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
result = gc.player_act({
        'token': players[0].token,
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'discard',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'discard': [0, 1],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
        'token': players[0].token,
        'discard': [0, 8],
    })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player_id'])
    assert_eq(2, len(event['discard']))
    if True: # just indent for a nice appearance, check cards
        cards = event['discard']
        assert_eq('slash', cards[0]['name'])
        assert_eq(1, cards[0]['rank'])
        assert_eq(card.SPADE, cards[0]['suit'])
        assert_eq('slash', cards[1]['name'])
        assert_eq(9, cards[1]['rank'])
        assert_eq(card.SPADE, cards[1]['suit'])
    event = p0_events[1]
    assert_eq(players[1].player_id, event['player_id'])
    assert_eq(2, event['get'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events[0], p1_events[0])
event = p1_events[1]
assert_eq(players[1].player_id, event['player_id'])
if True: # just indent for a nice appearance, check cards
    cards = event['get']
    assert_eq('dodge', cards[0]['name'])
    assert_eq(11, cards[0]['rank'])
    assert_eq(card.HEART, cards[0]['suit'])
    assert_eq(10, cards[0]['id'])
    assert_eq('dodge', cards[1]['name'])
    assert_eq(12, cards[1]['rank'])
    assert_eq(card.DIAMOND, cards[1]['suit'])
    assert_eq(11, cards[1]['id'])
