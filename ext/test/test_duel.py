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
            test_data.CardInfo('duel', 1, card.SPADE),
            test_data.CardInfo('arson attack', 2, card.HEART),
            test_data.CardInfo('slash', 3, card.DIAMOND),
            test_data.CardInfo('duel', 4, card.SPADE),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('arson attack', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('slash', 8, card.DIAMOND),

            test_data.CardInfo('duel', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.SPADE),
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
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        1: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [0, 1],
        },
        2: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        3: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        8: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        9: {
            'require': ['fix target'],
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
# name         | rank (id = rank - 1) | suit

# duel         | 1                    | SPADE   <- use this to duel
# arson attack | 2                    | HEART
# slash        | 3                    | DIAMOND
# duel         | 4                    | SPADE
# duel         | 9                    | SPADE
# slash        | 10                   | SPADE

# slash        | 5                    | CLUB
# arson attack | 6                    | HEART
# dodge        | 7                    | DIAMOND
# slash        | 8                    | DIAMOND
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

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'players': [players[1].player_id],
}, gc.hint(players[0].token))
assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'slash': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [4, 7],
        },
    },
    'abort': 'allow',
    'players': [players[1].player_id],
}, gc.hint(players[1].token))

# cards:
# name         | rank | suit

# arson attack | 2    | HEART
# slash        | 3    | DIAMOND
# duel         | 4    | SPADE
# duel         | 9    | SPADE
# slash        | 10   | SPADE

# slash        | 5    | CLUB
# arson attack | 6    | HEART
# dodge        | 7    | DIAMOND
# slash        | 8    | DIAMOND <- play this
result = gc.player_act({
        'token': players[1].token,
        'method': 'slash',
        'discard': [7],
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

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'slash': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [2, 9],
        },
    },
    'abort': 'allow',
    'players': [players[0].player_id],
}, gc.hint(players[0].token))
assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'players': [players[0].player_id],
}, gc.hint(players[1].token))

# cards:
# name         | rank | suit

# arson attack | 2    | HEART
# slash        | 3    | DIAMOND <- play this
# duel         | 4    | SPADE
# duel         | 9    | SPADE
# slash        | 10   | SPADE

# slash        | 5    | CLUB
# arson attack | 6    | HEART
# dodge        | 7    | DIAMOND
result = gc.player_act({
        'token': players[0].token,
        'method': 'slash',
        'discard': [2],
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

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'players': [players[1].player_id],
}, gc.hint(players[0].token))
assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'slash': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [4],
        },
    },
    'abort': 'allow',
    'players': [players[1].player_id],
}, gc.hint(players[1].token))

result = gc.player_act({
    'token': players[1].token,
    'method': 'abort',
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

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        1: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [0, 1],
        },
        3: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        8: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        9: {
            'require': ['fix target'],
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
# name         | rank | suit

# arson attack | 2    | HEART
# duel         | 4    | SPADE
# duel         | 9    | SPADE
# slash        | 10   | SPADE

# slash        | 5    | CLUB
# arson attack | 6    | HEART
# dodge        | 7    | DIAMOND
result = gc.player_act({
        'token': players[0].token,
        'action': 'card',
        'targets': [players[1].player_id],
        'use': [0],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
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
        'targets': [players[0].player_id, players[1].player_id],
        'use': [3],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

# cards:
# name         | rank | suit

# arson attack | 2    | HEART
# duel         | 4    | SPADE <- use this
# duel         | 9    | SPADE
# slash        | 10   | SPADE

# slash        | 5    | CLUB
# arson attack | 6    | HEART
# dodge        | 7    | DIAMOND
result = gc.player_act({
        'token': players[0].token,
        'action': 'card',
        'targets': [players[1].player_id],
        'use': [3],
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
        'discard': [9],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

# cards:
# name         | rank | suit

# arson attack | 2    | HEART
# duel         | 9    | SPADE
# slash        | 10   | SPADE

# slash        | 5    | CLUB
# arson attack | 6    | HEART
# dodge        | 7    | DIAMOND
result = gc.player_act({
        'token': players[1].token,
        'method': 'slash',
        'discard': [9],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

result = gc.player_act({
        'token': players[1].token,
        'method': 'slash',
        'discard': [7],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

result = gc.player_act({
        'token': players[1].token,
        'method': 'slash',
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
        'token': players[1].token,
        'method': 'slash',
        'discard': [4, 5],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
        'method': 'slash',
        'discard': [4],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'token',
          }, result)

result = gc.player_act({
        'token': players[1].token,
        'method': 'slash',
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

# cards:
# name         | rank | suit

# arson attack | 2    | HEART
# duel         | 9    | SPADE
# slash        | 10   | SPADE

# slash        | 5    | CLUB <- play this
# arson attack | 6    | HEART
# dodge        | 7    | DIAMOND
result = gc.player_act({
        'token': players[1].token,
        'method': 'slash',
        'discard': [4],
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
        'method': 'abort',
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

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        1: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [0, 1],
        },
        8: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        9: {
            'require': ['fix target'],
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
# name         | rank | suit

# arson attack | 2    | HEART
# duel         | 9    | SPADE
# slash        | 10   | SPADE

# arson attack | 6    | HEART
# dodge        | 7    | DIAMOND
result = gc.player_act({
        'token': players[0].token,
        'action': 'card',
        'targets': [],
        'use': [8],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'card',
        'targets': [players[0].player_id, players[1].player_id],
        'use': [8],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)
result = gc.player_act({
        'token': players[0].token,
        'action': 'card',
        'targets': [players[0].player_id],
        'use': [8],
    })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target self',
          }, result)

# cards:
# name         | rank | suit

# arson attack | 2    | HEART
# duel         | 9    | SPADE <- use this
# slash        | 10   | SPADE

# arson attack | 6    | HEART
# dodge        | 7    | DIAMOND
result = gc.player_act({
        'token': players[0].token,
        'action': 'card',
        'targets': [players[1].player_id],
        'use': [8],
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
        'method': 'abort',
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

# fake duel

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('duel', 1, card.SPADE),
            test_data.CardInfo('dodge', 2, card.HEART),
            test_data.CardInfo('slash', 3, card.DIAMOND),
            test_data.CardInfo('duel', 4, card.SPADE),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('arson attack', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('slash', 8, card.DIAMOND),

            test_data.CardInfo('duel', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.SPADE),
     ])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

result = gc.player_act({
    'token': players[0].token,
    'action': 'duel',
    'targets': [players[0].player_id],
    'use': [1],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
}, result)
