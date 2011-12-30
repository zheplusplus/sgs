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
            test_data.CardInfo('-chitu', 5, card.HEART),
            test_data.CardInfo('-dawan', 13, card.SPADE),
            test_data.CardInfo('+jueying', 5, card.SPADE),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('steal', 7, card.CLUB),
            test_data.CardInfo('duel', 8, card.DIAMOND),
            test_data.CardInfo('-zixing', 13, card.DIAMOND),
            test_data.CardInfo('+dilu', 5, card.CLUB),

            test_data.CardInfo('slash', 1, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('steal', 9, card.HEART),
            test_data.CardInfo('steal', 10, card.CLUB),

            test_data.CardInfo('steal', 9, card.HEART),
            test_data.CardInfo('steal', 10, card.CLUB),
     ])), pc, ActionStack())
players = [Player(19), Player(91), Player(1729)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# +jueying | 5    | 2  | SPADE
# slash    | 1    | 3  | CLUB
# steal    | 9    | 12 | HEART <- use this
# steal    | 10   | 13 | CLUB

# steal    | 7    | 4  | CLUB
# duel     | 8    | 5  | DIAMOND
# -zixing  | 13   | 6  | DIAMOND
# +dilu    | 5    | 7  | CLUB
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'steal',
                           'targets': [players[1].player_id],
                           'cards': [12],
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('steal', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('steal', event['use'][0]['name'])
    assert_eq(9, event['use'][0]['rank'])
    assert_eq(card.HEART, event['use'][0]['suit'])
    assert_eq(12, event['use'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('steal', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('steal', event['use'][0]['name'])
    assert_eq(9, event['use'][0]['rank'])
    assert_eq(card.HEART, event['use'][0]['suit'])
p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(p1_events, p2_events)
last_event_id += 1

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# +jueying | 5    | 2  | SPADE
# slash    | 1    | 3  | CLUB
# steal    | 10   | 13 | CLUB

# steal    | 7    | 4  | CLUB <- steal this
# duel     | 8    | 5  | DIAMOND
# -zixing  | 13   | 6  | DIAMOND
# +dilu    | 5    | 7  | CLUB
result = gc.player_act({
                           'token': players[0].token,
                           'steal': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['source'])
    assert_eq(players[0].player_id, event['target'])
    assert_eq(1, len(event['cards']))
    assert_eq('cards', event['cards'][0]['region'])
    assert_eq(7, event['cards'][0]['rank'])
    assert_eq('steal', event['cards'][0]['name'])
    assert_eq(card.CLUB, event['cards'][0]['suit'])
    assert_eq(4, event['cards'][0]['id'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)

p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(1, len(p2_events))
if True: # just indent for a nice appearance
    event = p2_events[0]
    assert_eq(players[1].player_id, event['source'])
    assert_eq(players[0].player_id, event['target'])
    assert_eq(1, event['cards'])
last_event_id += 1

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# +jueying | 5    | 2  | SPADE
# slash    | 1    | 3  | CLUB
# steal    | 10   | 13 | CLUB
# steal    | 7    | 4  | CLUB <- use this

# duel     | 8    | 5  | DIAMOND
# -zixing  | 13   | 6  | DIAMOND
# +dilu    | 5    | 7  | CLUB
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'steal',
                           'targets': [players[1].player_id],
                           'cards': [4],
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('steal', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('steal', event['use'][0]['name'])
    assert_eq(7, event['use'][0]['rank'])
    assert_eq(card.CLUB, event['use'][0]['suit'])
    assert_eq(4, event['use'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('steal', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('steal', event['use'][0]['name'])
    assert_eq(7, event['use'][0]['rank'])
    assert_eq(card.CLUB, event['use'][0]['suit'])
p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(p1_events, p2_events)
last_event_id += 1

result = gc.player_act({
                           'token': players[0].token,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'steal',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'steal': 'weapon',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'no such equipment',
          }, result)

result = gc.player_act({
                           'token': players[2].token,
                           'steal': 'cards',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# +jueying | 5    | 2  | SPADE
# slash    | 1    | 3  | CLUB
# steal    | 10   | 13 | CLUB

# duel     | 8    | 5  | DIAMOND <- steal this
# -zixing  | 13   | 6  | DIAMOND
# +dilu    | 5    | 7  | CLUB
result = gc.player_act({
                           'token': players[0].token,
                           'steal': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['source'])
    assert_eq(players[0].player_id, event['target'])
    assert_eq(1, len(event['cards']))
    assert_eq('cards', event['cards'][0]['region'])
    assert_eq(8, event['cards'][0]['rank'])
    assert_eq('duel', event['cards'][0]['name'])
    assert_eq(card.DIAMOND, event['cards'][0]['suit'])
    assert_eq(5, event['cards'][0]['id'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)

p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(1, len(p2_events))
if True: # just indent for a nice appearance
    event = p2_events[0]
    assert_eq(players[1].player_id, event['source'])
    assert_eq(players[0].player_id, event['target'])
    assert_eq(1, event['cards'])
last_event_id += 1

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'steal',
                           'cards': [13],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'targets',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'steal',
                           'targets': [players[1].player_id],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'steal',
                           'targets': [],
                           'cards': [13],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'steal',
                           'targets': [players[1].player_id,
                                       players[2].player_id],
                           'cards': [13],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'steal',
                           'targets': [players[0].player_id],
                           'cards': [13],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target self',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'cards': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'give up',
                       })
assert_eq(ret_code.OK, result['code'])

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# +jueying | 5    | 2  | SPADE   <- equipped
# slash    | 1    | 3  | CLUB
# steal    | 10   | 13 | CLUB    <- discard
# duel     | 8    | 5  | DIAMOND <- discard

# -zixing  | 13   | 6  | DIAMOND
# +dilu    | 5    | 7  | CLUB
result = gc.player_act({
                           'token': players[0].token,
                           'discard': [13, 5],
                       })

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# +jueying | 5    | 2  | SPADE   <- equipped
# slash    | 1    | 3  | CLUB

# -zixing  | 13   | 6  | DIAMOND
# +dilu    | 5    | 7  | CLUB
# steal    | 9    | 14 | HEART
# steal    | 10   | 15 | CLUB
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'steal',
                           'targets': [players[0].player_id],
                           'cards': [14],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'out of range',
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'equip',
                           'cards': [7],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'steal',
                           'targets': [players[0].player_id],
                           'cards': [14],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'out of range',
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'steal',
                           'targets': [players[2].player_id],
                           'cards': [14],
                       })
assert_eq(ret_code.OK, result['code'])

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# +jueying | 5    | 2  | SPADE   <- equipped
# slash    | 1    | 3  | CLUB

# -zixing  | 13   | 6  | DIAMOND
# +dilu    | 5    | 7  | CLUB
# steal    | 9    | 14 | HEART <- use this
# steal    | 10   | 15 | CLUB

# slash    | 1    | 8  | CLUB  <- steal this
# slash    | 1    | 9  | CLUB
# slash    | 1    | 10 | CLUB
# slash    | 1    | 11 | CLUB
result = gc.player_act({
                           'token': players[1].token,
                           'steal': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'equip',
                           'cards': [6],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'steal',
                           'targets': [players[0].player_id],
                           'cards': [14],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

last_event_id = len(gc.get_events(players[0].token, 0)) # until player

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# +jueying | 5    | 2  | SPADE <- equipped, steal this
# slash    | 1    | 3  | CLUB

# -zixing  | 13   | 6  | DIAMOND
# +dilu    | 5    | 7  | CLUB
# steal    | 10   | 15 | CLUB  <- use this
# slash    | 1    | 8  | CLUB
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'steal',
                           'targets': [players[0].player_id],
                           'cards': [15],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'steal': '+1 horse',
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(3, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[0].player_id, event['targets'][0])
    assert_eq('steal', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('steal', event['use'][0]['name'])
    assert_eq(10, event['use'][0]['rank'])
    assert_eq(card.CLUB, event['use'][0]['suit'])
    event = p0_events[1]
    assert_eq('+1 horse', event['region'])
    assert_eq('+jueying', event['unequip']['name'])
    assert_eq(5, event['unequip']['rank'])
    assert_eq(card.SPADE, event['unequip']['suit'])
    event = p0_events[2]
    assert_eq(players[0].player_id, event['source'])
    assert_eq(players[1].player_id, event['target'])
    assert_eq(1, len(event['cards']))
    assert_eq('+1 horse', event['cards'][0]['region'])
    assert_eq(5, event['cards'][0]['rank'])
    assert_eq('+jueying', event['cards'][0]['name'])
    assert_eq(card.SPADE, event['cards'][0]['suit'])
    assert_eq(2, event['cards'][0]['id'])

p1_events = gc.get_events(players[1].token, last_event_id)
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[0].player_id, event['targets'][0])
    assert_eq('steal', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('steal', event['use'][0]['name'])
    assert_eq(10, event['use'][0]['rank'])
    assert_eq(card.CLUB, event['use'][0]['suit'])
    assert_eq(15, event['use'][0]['id'])

    assert_eq(p0_events[1], p1_events[1])
    assert_eq(p0_events[2], p1_events[2])

p2_events = gc.get_events(players[2].token, last_event_id)
if True: # just indent for a nice appearance
    assert_eq(p0_events[0], p2_events[0])
    assert_eq(p0_events[1], p2_events[1])

    event = p2_events[2]
    assert_eq(players[0].player_id, event['source'])
    assert_eq(players[1].player_id, event['target'])
    assert_eq(1, len(event['cards']))
    assert_eq('+1 horse', event['cards'][0]['region'])
    assert_eq(5, event['cards'][0]['rank'])
    assert_eq('+jueying', event['cards'][0]['name'])
    assert_eq(card.SPADE, event['cards'][0]['suit'])

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# slash    | 1    | 3  | CLUB

# -zixing  | 13   | 6  | DIAMOND
# +dilu    | 5    | 7  | CLUB
# slash    | 1    | 8  | CLUB
# +jueying | 5    | 2  | SPADE <- equipp this
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'equip',
                           'cards': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'equip',
                           'cards': [2],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong region',
          }, result)
