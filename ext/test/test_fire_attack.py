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
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

assert_eq({
              'code': ret_code.OK,
              'action': 'UseCards',
              'card': {
                          0: { 'type': 'forbid' },
                          1: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [0, 1],
                             },
                          2: { 'type': 'forbid' },
                          3: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [0, 1],
                             },
                          8: { 'type': 'forbid' },
                          9: { 'type': 'forbid' },
                      },
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'UseCards',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))
# cards:
# name        | rank (id = rank - 1) | suit

# slash       | 1                    | SPADE
# fire attack | 2                    | HEART <- use this
# dodge       | 3                    | DIAMOND
# fire attack | 4                    | HEART
# slash       | 9                    | SPADE
# slash       | 10                   | SPADE

# slash       | 5                    | CLUB
# fire attack | 6                    | HEART
# dodge       | 7                    | DIAMOND
# dodge       | 8                    | DIAMOND
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'use': [1],
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
    assert_eq(1, event['use'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('fire attack', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('fire attack', event['use'][0]['name'])
    assert_eq(2, event['use'][0]['rank'])
    assert_eq(card.HEART, event['use'][0]['suit'])
last_event_id += 1

assert_eq({
              'code': ret_code.OK,
              'action': 'ShowCards',
              'players': [players[1].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'ShowCards',
              'players': [players[1].player_id],
          }, gc.hint(players[1].token))

# cards:
# name        | rank | suit

# slash       | 1    | SPADE
# dodge       | 3    | DIAMOND
# fire attack | 4    | HEART
# slash       | 9    | SPADE
# slash       | 10   | SPADE

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND <- show this
# dodge       | 8    | DIAMOND
result = gc.player_act({
        'token': players[1].token,
        'show': [6],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['show']))
    assert_eq('dodge', event['show'][0]['name'])
    assert_eq(7, event['show'][0]['rank'])
    assert_eq(card.DIAMOND, event['show'][0]['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)
last_event_id += 1

assert_eq({
              'code': ret_code.OK,
              'action': 'DiscardCards',
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'DiscardCards',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))

# cards:
# name        | rank | suit

# slash       | 1    | SPADE
# dodge       | 3    | DIAMOND <- discard this
# fire attack | 4    | HEART
# slash       | 9    | SPADE
# slash       | 10   | SPADE

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND <- show this
# dodge       | 8    | DIAMOND
result = gc.player_act({
        'token': players[0].token,
        'discard': [2],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p0_events))
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(3, event['discard'][0]['rank'])
    assert_eq(card.DIAMOND, event['discard'][0]['suit'])
    assert_eq(2, event['discard'][0]['id'])
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(3, event['discard'][0]['rank'])
    assert_eq(card.DIAMOND, event['discard'][0]['suit'])
if True: # just indent for a nice appearance
    event = p0_events[1]
    assert_eq(players[1].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('fire', event['category'])
assert_eq(p0_events[1], p1_events[1])
last_event_id += 2

# cards:
# name        | rank | suit

# slash       | 1    | SPADE
# fire attack | 4    | HEART
# slash       | 9    | SPADE
# slash       | 10   | SPADE

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
assert_eq({
              'code': ret_code.OK,
              'action': 'UseCards',
              'card': {
                          0: { 'type': 'forbid' },
                          3: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [0, 1],
                             },
                          8: { 'type': 'forbid' },
                          9: { 'type': 'forbid' },
                      },
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'UseCards',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))

result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'use': [0],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'use': [5],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'use': [],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'use': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'targets',
          }, result)
result = gc.player_act({
        'token': players[1].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'use': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'use': [1],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [],
        'use': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id, players[0].player_id],
        'use': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

# cards:
# name        | rank | suit

# slash       | 1    | SPADE
# fire attack | 4    | HEART <- use this
# slash       | 9    | SPADE
# slash       | 10   | SPADE

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'use': [3],
    })
assert_eq(ret_code.OK, result['code'])

# cards:
# name        | rank | suit

# slash       | 1    | SPADE
# slash       | 9    | SPADE
# slash       | 10   | SPADE

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
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
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)
result = gc.player_act({
        'token': players[1].token,
        'show': [5, 6],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'need exactly one card'
          }, result)
result = gc.player_act({
        'token': players[1].token,
        'show': [],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'need exactly one card',
          }, result)

# cards:
# name        | rank | suit

# slash       | 1    | SPADE
# slash       | 9    | SPADE
# slash       | 10   | SPADE

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND <- show this
# dodge       | 8    | DIAMOND
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
        'discard': [0],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG %
                                        'need exactly one card of same suit',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'discard': [2],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'discard': [0, 8],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG %
                                        'need exactly one card of same suit',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'discard': [],
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
    assert_eq('fire attack', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('fire attack', event['use'][0]['name'])
    assert_eq(4, event['use'][0]['rank'])
    assert_eq(card.HEART, event['use'][0]['suit'])
    assert_eq(3, event['use'][0]['id'])
if True: # just indent for a nice appearance
    event = p1_events[0]
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
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['show']))
    assert_eq('dodge', event['show'][0]['name'])
    assert_eq(7, event['show'][0]['rank'])
    assert_eq(card.DIAMOND, event['show'][0]['suit'])
assert_eq(p0_events[1], p1_events[1])
last_event_id += 2

assert_eq({
              'code': ret_code.OK,
              'action': 'UseCards',
              'card': {
                          0: { 'type': 'forbid' },
                          8: { 'type': 'forbid' },
                          9: { 'type': 'forbid' },
                      },
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'UseCards',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))

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
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

# fire attack to a player without cards
pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('fire attack', 1, card.DIAMOND),
            test_data.CardInfo('fire attack', 2, card.DIAMOND),
            test_data.CardInfo('fire attack', 3, card.HEART),
            test_data.CardInfo('fire attack', 4, card.HEART),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('fire attack', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('dodge', 8, card.DIAMOND),

            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.CLUB),

            test_data.CardInfo('steal', 11, card.CLUB),
            test_data.CardInfo('steal', 12, card.CLUB),
     ])), pc, ActionStack())
map(lambda p: pc.add_player(p), players)
gc.start()

# cards:
# name        | rank | suit

# fire attack | 1    | DIAMOND <- use this
# fire attack | 2    | DIAMOND <- use this
# fire attack | 3    | HEART <- use this
# fire attack | 4    | HEART <- use this
# slash       | 9    | SPADE
# slash       | 10   | CLUB

# slash       | 5    | CLUB <- show this
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
for i in range(0, 4):
    assert_eq(ret_code.OK, gc.player_act({
                                             'token': players[0].token,
                                             'action': 'fire attack',
                                             'targets': [players[1].player_id],
                                             'use': [i],
                                         })['code'])
    assert_eq(ret_code.OK, gc.player_act({
                                             'token': players[1].token,
                                             'show': [4],
                                         })['code'])
    assert_eq(ret_code.OK, gc.player_act({
                                             'token': players[0].token,
                                             'discard': [],
                                         })['code'])

assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'action': 'give up',
                                     })['code'])
# cards:
# name        | rank | suit

# slash       | 9    | SPADE
# slash       | 10   | CLUB

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
# steal       | 11   | CLUB
# steal       | 12   | CLUB
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'steal',
                           'targets': [players[0].player_id],
                           'use': [10],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'steal': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'steal',
                           'targets': [players[0].player_id],
                           'use': [11],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'steal': 'cards',
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
              'reason': ret_code.BR_WRONG_ARG % 'forbid target no card',
          }, result)

assert_eq({
              'code': ret_code.OK,
              'action': 'UseCards',
              'players': [players[1].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'UseCards',
              'card': {
                          4: { 'type': 'forbid' },
                          5: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [1],
                             },
                          6: { 'type': 'forbid' },
                          7: { 'type': 'forbid' },
                          8: { 'type': 'forbid' },
                          9: { 'type': 'forbid' },
                      },
              'players': [players[1].player_id],
          }, gc.hint(players[1].token))

# fire attack to a player itself, with only the fire attack card
pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('fire attack', 1, card.DIAMOND),
            test_data.CardInfo('fire attack', 2, card.DIAMOND),
            test_data.CardInfo('fire attack', 3, card.HEART),
            test_data.CardInfo('fire attack', 4, card.HEART),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('fire attack', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('dodge', 8, card.DIAMOND),

            test_data.CardInfo('fire attack', 9, card.HEART),
            test_data.CardInfo('fire attack', 10, card.HEART),
     ])), pc, ActionStack())
map(lambda p: pc.add_player(p), players)
gc.start()

# cards:
# name        | rank | suit

# fire attack | 1    | DIAMOND <- use this
# fire attack | 2    | DIAMOND
# fire attack | 3    | HEART
# fire attack | 4    | HEART
# fire attack | 9    | HEART
# fire attack | 10   | HEART

# slash       | 5    | CLUB <- show this
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'action': 'fire attack',
                                         'targets': [players[1].player_id],
                                         'use': [0],
                                     })['code'])
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[1].token,
                                         'show': [4],
                                     })['code'])
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'discard': [],
                                     })['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until fire attack to 1

# cards:
# name        | rank | suit

# fire attack | 2    | DIAMOND <- use this
# fire attack | 3    | HEART
# fire attack | 4    | HEART
# fire attack | 9    | HEART
# fire attack | 10   | HEART

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'action': 'fire attack',
                                         'targets': [players[0].player_id],
                                         'use': [1],
                                     })['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[0].player_id, event['targets'][0])
    assert_eq('fire attack', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('fire attack', event['use'][0]['name'])
    assert_eq(2, event['use'][0]['rank'])
    assert_eq(card.DIAMOND, event['use'][0]['suit'])
    assert_eq(1, event['use'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[0].player_id, event['targets'][0])
    assert_eq('fire attack', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('fire attack', event['use'][0]['name'])
    assert_eq(2, event['use'][0]['rank'])
    assert_eq(card.DIAMOND, event['use'][0]['suit'])
last_event_id += 1

# cards:
# name        | rank | suit

# fire attack | 3    | HEART
# fire attack | 4    | HEART
# fire attack | 9    | HEART
# fire attack | 10   | HEART

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
result = gc.player_act({
                           'token': players[0].token,
                           'show': [1],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

# cards:
# name        | rank | suit

# fire attack | 3    | HEART <- show this
# fire attack | 4    | HEART
# fire attack | 9    | HEART
# fire attack | 10   | HEART

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'show': [2],
                                     })['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['show']))
    assert_eq('fire attack', event['show'][0]['name'])
    assert_eq(3, event['show'][0]['rank'])
    assert_eq(card.HEART, event['show'][0]['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)
last_event_id += 1

# cards:
# name        | rank | suit

# fire attack | 3    | HEART
# fire attack | 4    | HEART <- discard this
# fire attack | 9    | HEART
# fire attack | 10   | HEART

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'discard': [3],
                                     })['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p0_events))
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('fire attack', event['discard'][0]['name'])
    assert_eq(4, event['discard'][0]['rank'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
    assert_eq(3, event['discard'][0]['id'])
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('fire attack', event['discard'][0]['name'])
    assert_eq(4, event['discard'][0]['rank'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
if True: # just indent for a nice appearance
    event = p0_events[1]
    assert_eq(players[0].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('fire', event['category'])
assert_eq(p0_events[1], p1_events[1])
last_event_id += 1

# cards:
# name        | rank | suit

# fire attack | 3    | HEART <- show this
# fire attack | 9    | HEART <- use this
# fire attack | 10   | HEART

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'action': 'fire attack',
                                         'targets': [players[0].player_id],
                                         'use': [8],
                                     })['code'])
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'show': [2],
                                     })['code'])
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'discard': [],
                                     })['code'])
# cards:
# name        | rank | suit

# fire attack | 3    | HEART <- show this
# fire attack | 10   | HEART <- use this

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'action': 'fire attack',
                                         'targets': [players[0].player_id],
                                         'use': [9],
                                     })['code'])
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'show': [2],
                                     })['code'])
assert_eq(ret_code.OK, gc.player_act({
                                         'token': players[0].token,
                                         'discard': [],
                                     })['code'])

# cards:
# name        | rank | suit

# fire attack | 3    | HEART <- use this, no cards after use it

# slash       | 5    | CLUB
# fire attack | 6    | HEART
# dodge       | 7    | DIAMOND
# dodge       | 8    | DIAMOND
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'fire attack',
                           'targets': [players[0].player_id],
                           'use': [2],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target no card',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'fire attack',
                           'targets': [players[1].player_id],
                           'use': [2],
                       })
assert_eq(ret_code.OK, result['code'])
