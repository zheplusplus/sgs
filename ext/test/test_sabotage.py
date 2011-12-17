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
            test_data.CardInfo('sabotage', 1, card.SPADE),
            test_data.CardInfo('sabotage', 2, card.SPADE),
            test_data.CardInfo('sabotage', 3, card.SPADE),
            test_data.CardInfo('sabotage', 4, card.SPADE),

            test_data.CardInfo('slash', 5, card.SPADE),
            test_data.CardInfo('dodge', 6, card.HEART),
            test_data.CardInfo('slash', 7, card.CLUB),
            test_data.CardInfo('dodge', 8, card.DIAMOND),

            test_data.CardInfo('sabotage', 9, card.HEART),
            test_data.CardInfo('sabotage', 10, card.CLUB),
     ])), pc, ActionStack())
players = [Player(91, 0), Player(1729, 1)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

# cards:
# name     | rank (id = rank - 1) | suit

# sabotage | 1                    | SPADE   <- use this to duel
# sabotage | 2                    | SPADE
# sabotage | 3                    | SPADE
# sabotage | 4                    | SPADE
# sabotage | 9                    | HEART
# sabotage | 10                   | CLUB

# slash    | 5                    | SPADE   <- discard this
# dodge    | 6                    | HEART
# slash    | 7                    | CLUB
# dodge    | 8                    | DIAMOND
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
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
    assert_eq('sabotage', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
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
    assert_eq('sabotage', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
last_event_id += 1

result = gc.player_act({
                           'token': players[0].token,
                           'sabotage': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('cards', event['discard'][0]['region'])
    assert_eq(5, event['discard'][0]['rank'])
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(card.SPADE, event['discard'][0]['suit'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('cards', event['discard'][0]['region'])
    assert_eq(5, event['discard'][0]['rank'])
    assert_eq(4, event['discard'][0]['id'])
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(card.SPADE, event['discard'][0]['suit'])
last_event_id += 1

# cards:
# name     | rank | suit

# sabotage | 2    | SPADE   <- use this
# sabotage | 3    | SPADE
# sabotage | 4    | SPADE
# sabotage | 9    | HEART
# sabotage | 10   | CLUB

# dodge    | 6    | HEART   <- discard this
# slash    | 7    | CLUB
# dodge    | 8    | DIAMOND
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
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
    assert_eq('sabotage', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(2, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    assert_eq(1, event['use'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('sabotage', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(2, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
last_event_id += 1

result = gc.player_act({
                           'token': players[0].token,
                           'sabotage': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('cards', event['discard'][0]['region'])
    assert_eq(6, event['discard'][0]['rank'])
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(card.HEART, event['discard'][0]['suit'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('cards', event['discard'][0]['region'])
    assert_eq(6, event['discard'][0]['rank'])
    assert_eq(5, event['discard'][0]['id'])
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
last_event_id += 1

# cards:
# name     | rank | suit

# sabotage | 3    | SPADE   <- use this
# sabotage | 4    | SPADE
# sabotage | 9    | HEART
# sabotage | 10   | CLUB

# slash    | 7    | CLUB    <- discard this
# dodge    | 8    | DIAMOND
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [2],
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('sabotage', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(3, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    assert_eq(2, event['use'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('sabotage', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(3, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
last_event_id += 1

result = gc.player_act({
                           'token': players[0].token,
                           'sabotage': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('cards', event['discard'][0]['region'])
    assert_eq(7, event['discard'][0]['rank'])
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(card.CLUB, event['discard'][0]['suit'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('cards', event['discard'][0]['region'])
    assert_eq(7, event['discard'][0]['rank'])
    assert_eq(6, event['discard'][0]['id'])
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(card.CLUB, event['discard'][0]['suit'])
last_event_id += 1

# cards:
# name     | rank | suit

# sabotage | 4    | SPADE
# sabotage | 9    | HEART
# sabotage | 10   | CLUB

# dodge    | 8    | DIAMOND
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [2],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'cards': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'targets',
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'sabotage',
                           'targets': [players[0].player_id],
                           'cards': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[0].player_id],
                           'cards': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target self',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [],
                           'cards': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[0].player_id,
                                       players[1].player_id],
                           'cards': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [3, 8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

# cards:
# name     | rank | suit

# sabotage | 4    | SPADE   <- use this
# sabotage | 9    | HEART
# sabotage | 10   | CLUB

# dodge    | 8    | DIAMOND <- discard this
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [3],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'sabotage',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'sabotage': 'undef',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'bad message',
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'sabotage': 'cards',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'sabotage': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p0_events))
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('sabotage', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(4, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    assert_eq(3, event['use'][0]['id'])
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('sabotage', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(4, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])

if True: # just indent for a nice appearance
    event = p0_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('cards', event['discard'][0]['region'])
    assert_eq(8, event['discard'][0]['rank'])
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(card.DIAMOND, event['discard'][0]['suit'])
if True: # just indent for a nice appearance
    event = p1_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('cards', event['discard'][0]['region'])
    assert_eq(8, event['discard'][0]['rank'])
    assert_eq(7, event['discard'][0]['id'])
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(card.DIAMOND, event['discard'][0]['suit'])
last_event_id += 2

# cards:
# name     | rank | suit

# sabotage | 9    | HEART
# sabotage | 10   | CLUB
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target no card',
          }, result)
