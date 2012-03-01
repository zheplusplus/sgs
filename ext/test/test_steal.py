from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player

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
players = [Player(19, 3), Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'card': {
                          0: { 'type': 'implicit target' },
                          1: { 'type': 'implicit target' },
                          2: { 'type': 'implicit target' },
                          3: { 'type': 'forbid' },
                          12: {
                                  'type': 'fix target',
                                  'count': 1,
                                  'candidates': [1, 2],
                              },
                          13: {
                                  'type': 'fix target',
                                  'count': 1,
                                  'candidates': [1, 2],
                              },
                      },
              'abort': 'allow',
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))
assert_eq(gc.hint(players[1].token), gc.hint(players[2].token))

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
                           'action': 'card',
                           'targets': [players[1].player_id],
                           'use': [12],
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

assert_eq({
              'code': ret_code.OK,
              'action': 'region',
              'candidates': ['cards'],
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'region',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))

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
                           'region': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['source'])
    assert_eq(players[0].player_id, event['target'])
    assert_eq(1, len(event['transfer']))
    assert_eq('cards', event['transfer'][0]['region'])
    assert_eq(7, event['transfer'][0]['rank'])
    assert_eq('steal', event['transfer'][0]['name'])
    assert_eq(card.CLUB, event['transfer'][0]['suit'])
    assert_eq(4, event['transfer'][0]['id'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)

p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(1, len(p2_events))
if True: # just indent for a nice appearance
    event = p2_events[0]
    assert_eq(players[1].player_id, event['source'])
    assert_eq(players[0].player_id, event['target'])
    assert_eq(1, event['transfer'])
last_event_id += 1

assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'card': {
                          0: { 'type': 'implicit target' },
                          1: { 'type': 'implicit target' },
                          2: { 'type': 'implicit target' },
                          3: { 'type': 'forbid' },
                          4: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [1, 2],
                             },
                          13: {
                                  'type': 'fix target',
                                  'count': 1,
                                  'candidates': [1, 2],
                              },
                      },
              'abort': 'allow',
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))
assert_eq(gc.hint(players[1].token), gc.hint(players[2].token))

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
                           'action': 'card',
                           'targets': [players[1].player_id],
                           'use': [4],
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
              'reason': ret_code.BR_MISSING_ARG % 'region',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'region': 'weapon',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'no such equipment',
          }, result)

result = gc.player_act({
                           'token': players[2].token,
                           'region': 'cards',
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
                           'region': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['source'])
    assert_eq(players[0].player_id, event['target'])
    assert_eq(1, len(event['transfer']))
    assert_eq('cards', event['transfer'][0]['region'])
    assert_eq(8, event['transfer'][0]['rank'])
    assert_eq('duel', event['transfer'][0]['name'])
    assert_eq(card.DIAMOND, event['transfer'][0]['suit'])
    assert_eq(5, event['transfer'][0]['id'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)

p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(1, len(p2_events))
if True: # just indent for a nice appearance
    event = p2_events[0]
    assert_eq(players[1].player_id, event['source'])
    assert_eq(players[0].player_id, event['target'])
    assert_eq(1, event['transfer'])
last_event_id += 1

assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'card': {
                          0: { 'type': 'implicit target' },
                          1: { 'type': 'implicit target' },
                          2: { 'type': 'implicit target' },
                          3: { 'type': 'forbid' },
                          5: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [1, 2],
                             },
                          13: {
                                  'type': 'fix target',
                                  'count': 1,
                                  'candidates': [1, 2],
                              },
                      },
              'abort': 'allow',
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))
assert_eq(gc.hint(players[1].token), gc.hint(players[2].token))

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'use': [13],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'targets',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [players[1].player_id],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'use',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [],
                           'use': [13],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [players[1].player_id,
                                       players[2].player_id],
                           'use': [13],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [13],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target self',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [2],
                       })
assert_eq(ret_code.OK, result['code'])

assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'card': {
                          0: { 'type': 'implicit target' },
                          1: { 'type': 'implicit target' },
                          3: { 'type': 'forbid' },
                          5: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [1, 2],
                             },
                          13: {
                                  'type': 'fix target',
                                  'count': 1,
                                  'candidates': [1, 2],
                              },
                      },
              'abort': 'allow',
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))
assert_eq(gc.hint(players[1].token), gc.hint(players[2].token))

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
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
assert_eq(ret_code.OK, result['code'])

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
assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'players': [players[1].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'card': {
                          6: { 'type': 'implicit target' },
                          7: { 'type': 'implicit target' },
                          14: {
                                  'type': 'fix target',
                                  'count': 1,
                                  'candidates': [2],
                              },
                          15: {
                                  'type': 'fix target',
                                  'count': 1,
                                  'candidates': [2],
                              },
                      },
              'abort': 'allow',
              'players': [players[1].player_id],
          }, gc.hint(players[1].token))
assert_eq(gc.hint(players[0].token), gc.hint(players[2].token))

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [14],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'out of range',
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'equip',
                           'use': [7],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [14],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'out of range',
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[2].player_id],
                           'use': [14],
                       })
assert_eq(ret_code.OK, result['code'])

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# +jueying | 5    | 2  | SPADE   <- equipped
# slash    | 1    | 3  | CLUB

# -zixing  | 13   | 6  | DIAMOND
# +dilu    | 5    | 7  | CLUB  <- equipped
# steal    | 9    | 14 | HEART <- use this
# steal    | 10   | 15 | CLUB

# slash    | 1    | 8  | CLUB  <- steal this
# slash    | 1    | 9  | CLUB
# slash    | 1    | 10 | CLUB
# slash    | 1    | 11 | CLUB
result = gc.player_act({
                           'token': players[1].token,
                           'region': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'equip',
                           'use': [6],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [14],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

last_event_id = len(gc.get_events(players[0].token, 0)) # until player

assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'players': [players[1].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'card': {
                          8: { 'type': 'forbid' },
                          15: {
                                  'type': 'fix target',
                                  'count': 1,
                                  'candidates': [2, 0],
                              },
                      },
              'abort': 'allow',
              'players': [players[1].player_id],
          }, gc.hint(players[1].token))
assert_eq(gc.hint(players[0].token), gc.hint(players[2].token))

# cards:
# name     | rank | id | suit

# -chitu   | 5    | 0  | HEART
# -dawan   | 13   | 1  | SPADE
# +jueying | 5    | 2  | SPADE <- equipped, steal this
# slash    | 1    | 3  | CLUB

# -zixing  | 13   | 6  | DIAMOND <- equipped
# +dilu    | 5    | 7  | CLUB  <- equipped
# steal    | 10   | 15 | CLUB  <- use this
# slash    | 1    | 8  | CLUB
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [15],
                       })
assert_eq(ret_code.OK, result['code'])

assert_eq({
              'code': ret_code.OK,
              'action': 'region',
              'players': [players[1].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'region',
              'candidates': ['cards', '+1 horse'],
              'players': [players[1].player_id],
          }, gc.hint(players[1].token))

result = gc.player_act({
                           'token': players[1].token,
                           'region': '+1 horse',
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
    assert_eq(1, len(event['transfer']))
    assert_eq('+1 horse', event['transfer'][0]['region'])
    assert_eq(5, event['transfer'][0]['rank'])
    assert_eq('+jueying', event['transfer'][0]['name'])
    assert_eq(card.SPADE, event['transfer'][0]['suit'])
    assert_eq(2, event['transfer'][0]['id'])

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
    assert_eq(1, len(event['transfer']))
    assert_eq('+1 horse', event['transfer'][0]['region'])
    assert_eq(5, event['transfer'][0]['rank'])
    assert_eq('+jueying', event['transfer'][0]['name'])
    assert_eq(card.SPADE, event['transfer'][0]['suit'])

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
                           'use': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'equip',
                           'use': [2],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong region',
          }, result)

# steal player without cards in hand

players = [Player(91, 3), Player(1729, 4)]
pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('-chitu', 5, card.HEART),
            test_data.CardInfo('steal', 1, card.CLUB),
            test_data.CardInfo('steal', 1, card.CLUB),
            test_data.CardInfo('steal', 1, card.CLUB),

            test_data.CardInfo('steal', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.CLUB),

            test_data.CardInfo('slash', 1, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('slash', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.CLUB),
     ])), pc, ActionStack())
map(lambda p: pc.add_player(p), players)
gc.start()

assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'card': {
                          0: { 'type': 'implicit target' },
                          1: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [1],
                             },
                          2: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [1],
                             },
                          3: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [1],
                             },
                          8: { 'type': 'forbid' },
                          9: { 'type': 'forbid' },
                      },
              'abort': 'allow',
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))

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
                           'discard': [8, 9],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [4],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'region': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])

for i in (1, 2):
    result = gc.player_act({
                               'token': players[1].token,
                               'action': 'card',
                               'targets': [players[0].player_id],
                               'use': [i],
                           })
    assert_eq(ret_code.OK, result['code'])

    result = gc.player_act({
                               'token': players[1].token,
                               'region': 'cards',
                           })
    assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [3],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'region': 'cards',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'bad region',
          }, result)

# with horsemanship and prodigy

import ext.src.skills.horsemanship as horsemanship
import ext.src.skills.prodigy as prodigy

players = [Player(i, 3) for i in range(0, 6)]
horsemanship.add_to(players[0])
prodigy.add_to(players[1])

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('-chitu', 5, card.HEART),
            test_data.CardInfo('steal', 1, card.SPADE),
            test_data.CardInfo('slash', 1, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('steal', 7, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('slash', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.CLUB),

            test_data.CardInfo('slash', 3, card.CLUB), # <- player 0 steal this
            test_data.CardInfo('slash', 3, card.CLUB),
            test_data.CardInfo('slash', 3, card.CLUB),
            test_data.CardInfo('slash', 3, card.CLUB),

            test_data.CardInfo('slash', 4, card.CLUB),
            test_data.CardInfo('slash', 4, card.CLUB),
            test_data.CardInfo('slash', 4, card.CLUB),
            test_data.CardInfo('slash', 4, card.CLUB),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('slash', 5, card.CLUB),

            test_data.CardInfo('slash', 1, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('slash', 1, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),
     ])), pc, ActionStack())
map(lambda p: pc.add_player(p), players)
gc.start()

assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'card': {
                          0: { 'type': 'implicit target' },
                          1: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [1, 2, 4, 5],
                             },
                          2: { 'type': 'forbid' },
                          3: { 'type': 'forbid' },
                          24: { 'type': 'forbid' },
                          25: { 'type': 'forbid' },
                      },
              'abort': 'allow',
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))
assert_eq(gc.hint(players[1].token), gc.hint(players[2].token))
assert_eq(gc.hint(players[1].token), gc.hint(players[3].token))
assert_eq(gc.hint(players[1].token), gc.hint(players[4].token))
assert_eq(gc.hint(players[1].token), gc.hint(players[5].token))

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [players[3].player_id],
                           'use': [1],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'out of range',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [0],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [players[3].player_id],
                           'use': [1],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'region': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [2, 12],
                       })
assert_eq(ret_code.OK, result['code'])

assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'players': [players[1].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'card': {
                          4: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [2, 3, 4, 5, 0],
                             },
                          5: { 'type': 'forbid' },
                          6: { 'type': 'forbid' },
                          7: { 'type': 'forbid' },
                          26: { 'type': 'forbid' },
                          27: { 'type': 'forbid' },
                      },
              'abort': 'allow',
              'players': [players[1].player_id],
          }, gc.hint(players[1].token))
assert_eq(gc.hint(players[0].token), gc.hint(players[2].token))
assert_eq(gc.hint(players[0].token), gc.hint(players[3].token))
assert_eq(gc.hint(players[0].token), gc.hint(players[4].token))
assert_eq(gc.hint(players[0].token), gc.hint(players[5].token))

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[4].player_id],
                           'use': [4],
                       })
assert_eq(ret_code.OK, result['code'])

# steal hint after sabotage +1 horse

players = [Player(91, 4), Player(1729, 4)]
pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('-chitu', 5, card.HEART),
            test_data.CardInfo('+dilu', 5, card.CLUB),
            test_data.CardInfo('steal', 1, card.CLUB),
            test_data.CardInfo('steal', 1, card.CLUB),

            test_data.CardInfo('steal', 4, card.DIAMOND),
            test_data.CardInfo('sabotage', 12, card.HEART),
            test_data.CardInfo('slash', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.CLUB),

            test_data.CardInfo('slash', 1, card.CLUB),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('slash', 2, card.CLUB),
            test_data.CardInfo('slash', 2, card.CLUB),
     ])), pc, ActionStack())
map(lambda p: pc.add_player(p), players)
gc.start()

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'use': [0],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'use': [1],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

assert_eq({
              'code': ret_code.OK,
              'players': [players[1].player_id],
              'action': 'use',
              'card': {
                  4: { 'type': 'forbid' },
                  5: {
                      'type': 'fix target',
                      'count': 1,
                      'candidates': [players[0].player_id],
                  },
                  6: { 'type': 'forbid' },
                  7: { 'type': 'forbid' },
                  10: { 'type': 'forbid' },
                  11: { 'type': 'forbid' },
              },
              'abort': 'allow',
          }, gc.hint(players[1].token))

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'use': [5],
                           'targets': [players[0].player_id],
                       })
assert_eq(ret_code.OK, result['code'])

assert_eq({
              'code': ret_code.OK,
              'players': [players[1].player_id],
              'action': 'region',
              'candidates': [ 'cards', '-1 horse', '+1 horse' ],
          }, gc.hint(players[1].token))

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'region',
                           'region': '+1 horse',
                       })
assert_eq(ret_code.OK, result['code'])

assert_eq({
              'code': ret_code.OK,
              'players': [players[1].player_id],
              'action': 'use',
              'card': {
                  4: {
                      'type': 'fix target',
                      'count': 1,
                      'candidates': [players[0].player_id],
                  },
                  6: { 'type': 'forbid' },
                  7: { 'type': 'forbid' },
                  10: { 'type': 'forbid' },
                  11: { 'type': 'forbid' },
              },
              'abort': 'allow',
          }, gc.hint(players[1].token))

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'use': [4],
                           'targets': [players[0].player_id],
                       })
assert_eq(ret_code.OK, result['code'])

assert_eq({
              'code': ret_code.OK,
              'players': [players[1].player_id],
              'action': 'region',
              'candidates': [ 'cards', '-1 horse' ],
          }, gc.hint(players[1].token))
