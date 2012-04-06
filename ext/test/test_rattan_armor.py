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
            test_data.CardInfo('rattan armor', 2, card.CLUB),
            test_data.CardInfo('rattan armor', 2, card.SPADE),
            test_data.CardInfo('slash', 3, card.HEART),
            test_data.CardInfo('slash', 4, card.HEART),

            test_data.CardInfo('steal', 5, card.CLUB),
            test_data.CardInfo('arson attack', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.HEART),
            test_data.CardInfo('duel', 8, card.HEART),

            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.CLUB),

            test_data.CardInfo('arson attack', 11, card.CLUB),
            test_data.CardInfo('dodge', 12, card.HEART),
     ])), pc, ActionStack())
players = [Player(91, 8), Player(1729, 8)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 0  | CLUB <- equip this
# rattan armor | 2    | 1  | SPADE <-  and this
# slash        | 3    | 2  | HEART
# slash        | 4    | 3  | HEART
# slash        | 9    | 8  | SPADE
# slash        | 10   | 9  | CLUB

# steal        | 5    | 4  | CLUB
# arson attack | 6    | 5  | HEART
# dodge        | 7    | 6  | HEART
# duel         | 8    | 7  | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [0],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [1],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [9],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [0],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(4, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('rattan armor', event['equip']['name'])
    assert_eq(2, event['equip']['rank'])
    assert_eq(card.CLUB, event['equip']['suit'])
    assert_eq(0, event['equip']['id'])
    event = p0_events[1]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('armor', event['region'])
    assert_eq('rattan armor', event['unequip']['name'])
    assert_eq(2, event['unequip']['rank'])
    assert_eq(card.CLUB, event['unequip']['suit'])
    event = p0_events[2]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('rattan armor', event['equip']['name'])
    assert_eq(2, event['equip']['rank'])
    assert_eq(card.SPADE, event['equip']['suit'])
    assert_eq(1, event['equip']['id'])
    event = p0_events[3]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(2, event['draw'])

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 1  | SPADE <- equipped
# slash        | 3    | 2  | HEART <- show this
# slash        | 4    | 3  | HEART
# slash        | 9    | 8  | SPADE
# slash        | 10   | 9  | CLUB

# steal        | 5    | 4  | CLUB
# arson attack | 6    | 5  | HEART <- use this
# dodge        | 7    | 6  | HEART <- discard this
# duel         | 8    | 7  | HEART
# arson attack | 11   | 10 | CLUB
# dodge        | 12   | 11 | HEART
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'arson attack',
                           'targets': [players[0].player_id],
                           'use': [5],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [2],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until show a card

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'discard',
                           'discard': [6],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(3, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(1, len(event['discard']))
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(7, event['discard'][0]['rank'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
    event = p0_events[1]
    assert_eq('Invocation', event['type'])
    assert_eq(players[0].player_id, event['player'])
    assert_eq('rattan armor', event['invoke'])
    event = p0_events[2]
    assert_eq(players[0].player_id, event['victim'])
    assert_eq(2, event['damage'])
    assert_eq('fire', event['category'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(3, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(1, len(event['discard']))
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(7, event['discard'][0]['rank'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
    assert_eq(6, event['discard'][0]['id'])
    assert_eq(p0_events[1], p1_events[1])
    assert_eq(p0_events[2], p1_events[2])

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 1  | SPADE <- equipped
# slash        | 3    | 2  | HEART
# slash        | 4    | 3  | HEART
# slash        | 9    | 8  | SPADE
# slash        | 10   | 9  | CLUB

# steal        | 5    | 4  | CLUB
# duel         | 8    | 7  | HEART <- use this
# arson attack | 11   | 10 | CLUB
# dodge        | 12   | 11 | HEART
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'duel',
                           'targets': [players[0].player_id],
                           'use': [7],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until duel
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

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 1  | SPADE <- equipped
# slash        | 3    | 2  | HEART
# slash        | 4    | 3  | HEART
# slash        | 9    | 8  | SPADE
# slash        | 10   | 9  | CLUB

# steal        | 5    | 4  | CLUB <- steal rattan armor
# arson attack | 11   | 10 | CLUB
# dodge        | 12   | 11 | HEART
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [4],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'region': 'armor',
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until steal
# cards:
# name         | rank | id | suit

# slash        | 3    | 2  | HEART
# slash        | 4    | 3  | HEART
# slash        | 9    | 8  | SPADE
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 1  | SPADE <- equipped
# arson attack | 11   | 10 | CLUB
# dodge        | 12   | 11 | HEART
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'equip',
                           'use': [1],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq('rattan armor', event['equip']['name'])
    assert_eq(2, event['equip']['rank'])
    assert_eq(card.SPADE, event['equip']['suit'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['player'])
    assert_eq('rattan armor', event['equip']['name'])
    assert_eq(2, event['equip']['rank'])
    assert_eq(card.SPADE, event['equip']['suit'])
    assert_eq(1, event['equip']['id'])

# cards:
# name         | rank | id | suit

# slash        | 3    | 2  | HEART <- show this
# slash        | 4    | 3  | HEART
# slash        | 9    | 8  | SPADE
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 1  | SPADE <- equipped
# arson attack | 11   | 10 | CLUB <- use this
# dodge        | 12   | 11 | HEART <- discard this
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'arson attack',
                           'targets': [players[0].player_id],
                           'use': [10],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [2],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until show a card

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'discard',
                           'discard': [11],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(1, len(event['discard']))
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(12, event['discard'][0]['rank'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
    event = p0_events[1]
    assert_eq(players[0].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('fire', event['category'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(1, len(event['discard']))
    assert_eq('dodge', event['discard'][0]['name'])
    assert_eq(12, event['discard'][0]['rank'])
    assert_eq(card.HEART, event['discard'][0]['suit'])
    assert_eq(11, event['discard'][0]['id'])
    assert_eq(p0_events[1], p1_events[1])

# immune to slash

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
    test_data.CardInfo('slash', 1, card.CLUB),
    test_data.CardInfo('rattan armor', 2, card.SPADE),
    test_data.CardInfo('slash', 3, card.HEART),
    test_data.CardInfo('slash', 4, card.HEART),

    test_data.CardInfo('slash', 5, card.HEART),
    test_data.CardInfo('sabotage', 6, card.CLUB),
    test_data.CardInfo('dodge', 7, card.HEART),
    test_data.CardInfo('thunder slash', 8, card.SPADE),

    test_data.CardInfo('slash', 9, card.SPADE),
    test_data.CardInfo('slash', 10, card.CLUB),

    test_data.CardInfo('slash', 11, card.CLUB),
    test_data.CardInfo('dodge', 12, card.HEART),
])), pc, ActionStack())
players = [Player(91, 8), Player(1729, 8)]
map(lambda p: pc.add_player(p), players)
gc.start()

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

last_event_id = len(gc.get_events(players[0].token, 0)) # about to slash

result = gc.player_act({
    'token': players[1].token,
    'action': 'card',
    'targets': [players[0].player_id],
    'use': [4],
})
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['user'])
    assert_eq([players[0].player_id], event['targets'])
    assert_eq(1, len(event['use']))
    assert_eq('slash', event['use'][0]['name'])
    assert_eq(5, event['use'][0]['rank'])
    assert_eq(card.HEART, event['use'][0]['suit'])
    event = p0_events[1]
    assert_eq('Invocation', event['type'])
    assert_eq(players[0].player_id, event['player'])
    assert_eq('rattan armor', event['invoke'])

p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['user'])
    assert_eq([players[0].player_id], event['targets'])
    assert_eq(1, len(event['use']))
    assert_eq('slash', event['use'][0]['name'])
    assert_eq(5, event['use'][0]['rank'])
    assert_eq(card.HEART, event['use'][0]['suit'])
    assert_eq(4, event['use'][0]['id'])
    assert_eq(p0_events[1], p1_events[1])

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'players': [players[1].player_id],
}, gc.hint(players[0].token))
assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        5: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [0],
        },
        6: { 'require': ['forbid'] },
        7: { 'require': ['forbid'] },
        10: { 'require': ['forbid'] },
        11: { 'require': ['forbid'] },
    },
    'abort': 'allow',
    'players': [players[1].player_id],
}, gc.hint(players[1].token))

# use thunder slash

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
    test_data.CardInfo('slash', 1, card.CLUB),
    test_data.CardInfo('rattan armor', 2, card.SPADE),
    test_data.CardInfo('slash', 3, card.HEART),
    test_data.CardInfo('slash', 4, card.HEART),

    test_data.CardInfo('slash', 5, card.HEART),
    test_data.CardInfo('sabotage', 6, card.CLUB),
    test_data.CardInfo('dodge', 7, card.HEART),
    test_data.CardInfo('thunder slash', 8, card.SPADE),

    test_data.CardInfo('slash', 9, card.SPADE),
    test_data.CardInfo('slash', 10, card.CLUB),

    test_data.CardInfo('slash', 11, card.CLUB),
    test_data.CardInfo('dodge', 12, card.HEART),
])), pc, ActionStack())
players = [Player(91, 8), Player(1729, 8)]
map(lambda p: pc.add_player(p), players)
gc.start()

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

result = gc.player_act({
    'token': players[1].token,
    'action': 'card',
    'targets': [players[0].player_id],
    'use': [7],
})
assert_eq(ret_code.OK, result['code'])

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'dodge': {
            'require': ['fix card count'],
            'cards': [],
            'card count': 1,
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

# sabotage

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
    test_data.CardInfo('slash', 1, card.CLUB),
    test_data.CardInfo('rattan armor', 2, card.SPADE),
    test_data.CardInfo('slash', 3, card.HEART),
    test_data.CardInfo('slash', 4, card.HEART),

    test_data.CardInfo('slash', 5, card.HEART),
    test_data.CardInfo('sabotage', 6, card.CLUB),
    test_data.CardInfo('dodge', 7, card.HEART),
    test_data.CardInfo('thunder slash', 8, card.SPADE),

    test_data.CardInfo('slash', 9, card.SPADE),
    test_data.CardInfo('slash', 10, card.CLUB),

    test_data.CardInfo('slash', 11, card.CLUB),
    test_data.CardInfo('dodge', 12, card.HEART),
])), pc, ActionStack())
players = [Player(91, 8), Player(1729, 8)]
map(lambda p: pc.add_player(p), players)
gc.start()

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

result = gc.player_act({
    'token': players[1].token,
    'action': 'card',
    'targets': [players[0].player_id],
    'use': [5],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'region': 'armor',
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'action': 'card',
    'targets': [players[0].player_id],
    'use': [4],
})
assert_eq(ret_code.OK, result['code'])

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'dodge': {
            'require': ['fix card count'],
            'cards': [],
            'card count': 1,
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
