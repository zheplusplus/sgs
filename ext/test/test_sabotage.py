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
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        0: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        1: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        2: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        3: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        8: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        9: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
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
                           'action': 'card',
                           'targets': [players[1].player_id],
                           'use': [0],
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

assert_eq({
              'code': ret_code.OK,
              'action': 'region',
              'regions': ['onhand'],
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'region',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))

result = gc.player_act({
                           'token': players[0].token,
                           'region': 'onhand',
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('onhand', event['discard'][0]['region'])
    assert_eq(5, event['discard'][0]['rank'])
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(card.SPADE, event['discard'][0]['suit'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('onhand', event['discard'][0]['region'])
    assert_eq(5, event['discard'][0]['rank'])
    assert_eq(4, event['discard'][0]['id'])
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(card.SPADE, event['discard'][0]['suit'])
last_event_id += 1

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        1: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        2: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        3: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        8: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        9: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
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
                           'action': 'card',
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
                           'region': 'onhand',
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('onhand', event['discard'][0]['region'])
    assert_eq(6, event['discard'][0]['rank'])
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(card.HEART, event['discard'][0]['suit'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('onhand', event['discard'][0]['region'])
    assert_eq(6, event['discard'][0]['rank'])
    assert_eq(5, event['discard'][0]['id'])
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
last_event_id += 1

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        2: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        3: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        8: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        9: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
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
                           'action': 'card',
                           'targets': [players[1].player_id],
                           'use': [2],
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
                           'region': 'onhand',
                       })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('onhand', event['discard'][0]['region'])
    assert_eq(7, event['discard'][0]['rank'])
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(card.CLUB, event['discard'][0]['suit'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('onhand', event['discard'][0]['region'])
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
                           'action': 'card',
                           'targets': [players[1].player_id],
                           'use': [2],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'use': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'targets',
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target self',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [],
                           'use': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [players[0].player_id,
                                       players[1].player_id],
                           'use': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [players[1].player_id],
                           'use': [3, 8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [players[1].player_id],
                           'use': [],
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
                           'action': 'card',
                           'targets': [players[1].player_id],
                           'use': [3],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'region',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'region': 'undef',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'no such equipment',
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'region': 'onhand',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'region': 'onhand',
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
    assert_eq('onhand', event['discard'][0]['region'])
    assert_eq(8, event['discard'][0]['rank'])
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(card.DIAMOND, event['discard'][0]['suit'])
if True: # just indent for a nice appearance
    event = p1_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['discard']))
    assert_eq('onhand', event['discard'][0]['region'])
    assert_eq(8, event['discard'][0]['rank'])
    assert_eq(7, event['discard'][0]['id'])
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(card.DIAMOND, event['discard'][0]['suit'])
last_event_id += 2

assert_eq({
              'code': ret_code.OK,
              'action': 'use',
              'card': {
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

# cards:
# name     | rank | suit

# sabotage | 9    | HEART
# sabotage | 10   | CLUB
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'card',
                           'targets': [players[1].player_id],
                           'use': [8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target no card',
          }, result)

# sabotage weapon
pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('duel', 1, card.SPADE),
            test_data.CardInfo('zhangba serpent spear', 2, card.SPADE),
            test_data.CardInfo('slash', 3, card.DIAMOND),
            test_data.CardInfo('dodge', 4, card.DIAMOND),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('sabotage', 6, card.HEART),
            test_data.CardInfo('sabotage', 7, card.DIAMOND),
            test_data.CardInfo('slash', 8, card.DIAMOND),

            test_data.CardInfo('duel', 9, card.SPADE),
            test_data.CardInfo('zhangba serpent spear', 10, card.HEART),

            test_data.CardInfo('duel', 11, card.DIAMOND),
            test_data.CardInfo('sabotage', 12, card.HEART),
     ])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

result = gc.player_act({
                          'token': players[0].token,
                          'action': 'equip',
                          'use': [1],
                      })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                          'token': players[0].token,
                          'action': 'abort',
                      })
assert_eq(ret_code.OK, result['code'])

# cards:
# name                  | rank (id = rank - 1) | suit

# duel                  | 1                    | SPADE   <- discard this
# zhangba serpent spear | 2                    | SPADE   -- equipped
# slash                 | 3                    | DIAMOND
# dodge                 | 4                    | DIAMOND
# duel                  | 9                    | SPADE
# zhangba serpent spear | 10                   | HEART

# slash                 | 5                    | CLUB
# sabotage              | 6                    | HEART
# sabotage              | 7                    | DIAMOND
# slash                 | 8                    | DIAMOND
result = gc.player_act({
                          'token': players[0].token,
                          'discard': [0],
                      })
assert_eq(ret_code.OK, result['code'])

# cards:
# name                  | rank (id = rank - 1) | suit

# zhangba serpent spear | 2                    | SPADE   -- equipped
# slash                 | 3                    | DIAMOND
# dodge                 | 4                    | DIAMOND
# duel                  | 9                    | SPADE
# zhangba serpent spear | 10                   | HEART

# slash                 | 5                    | CLUB
# sabotage              | 6                    | HEART
# sabotage              | 7                    | DIAMOND
# slash                 | 8                    | DIAMOND
# duel                  | 11                   | DIAMOND <- draw this and use it
# sabotage              | 12                   | HEART   <- draw this
result = gc.player_act({
                          'token': players[1].token,
                          'action': 'duel',
                          'targets': [players[0].player_id],
                          'use': [10],
                      })
assert_eq(ret_code.OK, result['code'])

# cards:
# name                  | rank (id = rank - 1) | suit

# zhangba serpent spear | 2                    | SPADE   -- equipped
# slash                 | 3                    | DIAMOND
# dodge                 | 4                    | DIAMOND <- play this
# duel                  | 9                    | SPADE
# zhangba serpent spear | 10                   | HEART   <-  and this

# slash                 | 5                    | CLUB
# sabotage              | 6                    | HEART
# sabotage              | 7                    | DIAMOND
# slash                 | 8                    | DIAMOND
# sabotage              | 12                   | HEART
result = gc.player_act({
                          'token': players[0].token,
                          'method': 'zhangba serpent spear',
                          'discard': [3, 9],
                      })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                          'token': players[1].token,
                          'method': 'slash',
                          'discard': [4],
                      })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                          'token': players[0].token,
                          'method': 'slash',
                          'discard': [2],
                      })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                          'token': players[1].token,
                          'method': 'abort',
                          'discard': [],
                      })
assert_eq(ret_code.OK, result['code'])

# cards:
# name                  | rank (id = rank - 1) | suit

# zhangba serpent spear | 2                    | SPADE   -- equipped
# duel                  | 9                    | SPADE   <- sabotage this

# sabotage              | 6                    | HEART   <- use this
# sabotage              | 7                    | DIAMOND
# slash                 | 8                    | DIAMOND
# sabotage              | 12                   | HEART
result = gc.player_act({
                          'token': players[1].token,
                          'action': 'card',
                          'targets': [players[0].player_id],
                          'use': [5],
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
              'regions': ['onhand', 'weapon'],
              'players': [players[1].player_id],
          }, gc.hint(players[1].token))

result = gc.player_act({
                          'token': players[1].token,
                          'region': 'onhand',
                      })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                          'token': players[1].token,
                          'action': 'card',
                          'targets': [players[0].player_id],
                          'use': [6],
                      })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                          'token': players[1].token,
                          'region': 'onhand',
                      })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'bad region',
          }, result)

last_event_id = len(gc.get_events(players[0].token, 0)) # about to sabotage
result = gc.player_act({
                          'token': players[1].token,
                          'region': 'weapon',
                      })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('weapon', event['region'])
    assert_eq('zhangba serpent spear', event['unequip']['name'])
    assert_eq(2, event['unequip']['rank'])
    assert_eq(card.SPADE, event['unequip']['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)

# cards:
# name                  | rank (id = rank - 1) | suit

# sabotage              | 7                    | DIAMOND <- use this
# slash                 | 8                    | DIAMOND
# sabotage              | 12                   | HEART
result = gc.player_act({
                          'token': players[1].token,
                          'action': 'card',
                          'targets': [players[0].player_id],
                          'use': [11],
                      })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target no card',
          }, result)
