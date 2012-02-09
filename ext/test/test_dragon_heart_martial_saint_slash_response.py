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
            test_data.CardInfo('arson attack', 2, card.HEART),
            test_data.CardInfo('slash', 3, card.CLUB),
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
martial_saint.add_to(players[0])
dragon_heart.add_to(players[1])

gc.start()

# cards:
# name         | rank (id = rank - 1) | suit

# duel         | 1                    | SPADE   <- use this to duel
# arson attack | 2                    | HEART
# slash        | 3                    | CLUB
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
last_event_id = len(gc.get_events(players[0].token, 0)) # until duel

result = gc.player_act({
                          'token': players[1].token,
                          'method': 'dragon heart',
                          'discard': [7],
                      })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
                          'token': players[1].token,
                          'method': 'martial saint',
                          'discard': [7],
                      })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'no such method',
          }, result)

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
        'dragon heart': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [6],
        },
    },
    'abort': 'allow',
    'players': [players[1].player_id],
}, gc.hint(players[1].token))

# cards:
# name         | rank (id = rank - 1) | suit

# arson attack | 2                    | HEART
# slash        | 3                    | CLUB
# duel         | 4                    | SPADE
# duel         | 9                    | SPADE
# slash        | 10                   | SPADE

# slash        | 5                    | CLUB
# arson attack | 6                    | HEART
# dodge        | 7                    | DIAMOND <- dragon heart play a dodge
# slash        | 8                    | DIAMOND
result = gc.player_act({
                          'token': players[1].token,
                          'method': 'dragon heart',
                          'discard': [6],
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
                          'discard': [3],
                      })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'no such method',
          }, result)

result = gc.player_act({
                          'token': players[0].token,
                          'method': 'martial saint',
                          'discard': [3],
                      })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'slash': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [2, 9],
        },
        'martial saint': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [1],
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
# name         | rank (id = rank - 1) | suit

# arson attack | 2                    | HEART <- dragon heart play a red card
# slash        | 3                    | CLUB
# duel         | 4                    | SPADE
# duel         | 9                    | SPADE
# slash        | 10                   | SPADE

# slash        | 5                    | CLUB
# arson attack | 6                    | HEART
# slash        | 8                    | DIAMOND
result = gc.player_act({
                          'token': players[0].token,
                          'method': 'martial saint',
                          'discard': [1],
                      })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('arson attack', event['play'][0]['name'])
    assert_eq(2, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq(1, event['play'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('arson attack', event['play'][0]['name'])
    assert_eq(2, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
last_event_id += 1

# cards:
# name         | rank (id = rank - 1) | suit

# slash        | 3                    | CLUB    <- slash this
# duel         | 4                    | SPADE
# duel         | 9                    | SPADE
# slash        | 10                   | SPADE

# slash        | 5                    | CLUB
# arson attack | 6                    | HEART
# slash        | 8                    | DIAMOND <- slash this
result = gc.player_act({
                          'token': players[1].token,
                          'method': 'slash',
                          'discard': [7],
                      })
assert_eq(ret_code.OK, result['code'])
result = gc.player_act({
                          'token': players[0].token,
                          'method': 'slash',
                          'discard': [2],
                      })
assert_eq(ret_code.OK, result['code'])

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
    test_data.CardInfo('duel', 1, card.SPADE),
    test_data.CardInfo('arson attack', 2, card.HEART),
    test_data.CardInfo('+hualiu', 5, card.DIAMOND),
    test_data.CardInfo('-dawan', 13, card.SPADE),

    test_data.CardInfo('steal', 5, card.CLUB),
    test_data.CardInfo('arson attack', 6, card.HEART),
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

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'use': [2],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'use': [3],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[1].player_id],
    'use': [0],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'method': 'dragon heart',
    'discard': [6],
})
assert_eq(ret_code.OK, result['code'])

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'slash': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [9],
        },
        'martial saint': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [1, 2],
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

result = gc.player_act({
    'token': players[0].token,
    'method': 'martial saint',
    'discard': [2],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'method': 'slash',
    'discard': [7],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'method': 'martial saint',
    'discard': [2],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'not own this card',
}, result)

result = gc.player_act({
    'token': players[0].token,
    'method': 'martial saint',
    'discard': [3],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
}, result)

result = gc.player_act({
    'token': players[0].token,
    'method': 'abort',
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'action': 'abort',
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'action': 'card',
    'targets': [players[0].player_id],
    'use': [4],
})
assert_eq(ret_code.OK, result['code'])

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('duel', 1, card.SPADE),
            test_data.CardInfo('-chitu', 5, card.HEART),
            test_data.CardInfo('slash', 3, card.CLUB),
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
martial_saint.add_to(players[0])

gc.start()

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'use': [1],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[1].player_id],
    'use': [0],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'method': 'slash',
    'discard': [7],
})
assert_eq(ret_code.OK, result['code'])
last_event_id = len(gc.get_events(players[0].token, 0)) # until playing slash

# cards:
# name         | rank (id) | suit

# -chitu       | 5    (1)  | HEART (equipped)
# slash        | 3    (2)  | CLUB
# duel         | 4    (3)  | SPADE
# duel         | 9    (8)  | SPADE
# slash        | 10   (9)  | SPADE

# slash        | 5    (4)  | CLUB
# arson attack | 6    (5)  | HEART
# dodge        | 7    (6)  | SPADE
assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'martial saint': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [1],
        },
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

result = gc.player_act({
    'token': players[0].token,
    'method': 'martial saint',
    'discard': [1],
})
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('-chitu', event['play'][0]['name'])
    assert_eq(5, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq('-1 horse', event['play'][0]['region'])
    assert_eq(1, event['play'][0]['id'])
    event = p0_events[1]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('-chitu', event['unequip']['name'])
    assert_eq(5, event['unequip']['rank'])
    assert_eq(card.HEART, event['unequip']['suit'])
    assert_eq('-1 horse', event['unequip']['region'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('-chitu', event['play'][0]['name'])
    assert_eq(5, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq('-1 horse', event['play'][0]['region'])
    assert_eq(p0_events[1], p1_events[1])
