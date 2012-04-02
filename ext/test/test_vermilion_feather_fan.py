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
    test_data.CardInfo('vermilion feather fan', 1, card.DIAMOND),
    test_data.CardInfo('duel', 2, card.SPADE),
    test_data.CardInfo('slash', 3, card.DIAMOND),
    test_data.CardInfo('dodge', 4, card.DIAMOND),

    test_data.CardInfo('slash', 5, card.CLUB),
    test_data.CardInfo('slash', 6, card.HEART),
    test_data.CardInfo('dodge', 7, card.DIAMOND),
    test_data.CardInfo('slash', 8, card.DIAMOND),

    test_data.CardInfo('duel', 9, card.SPADE),
    test_data.CardInfo('thunder slash', 10, card.HEART),
])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        0: { 'require': ['implicit target'] },
        1: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        2: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        3: { 'require': ['forbid'] },
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

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'use': [0],
})
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('vermilion feather fan', event['equip']['name'])
    assert_eq(1, event['equip']['rank'])
    assert_eq(card.DIAMOND, event['equip']['suit'])
    assert_eq(0, event['equip']['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('vermilion feather fan', event['equip']['name'])
    assert_eq(1, event['equip']['rank'])
    assert_eq(card.DIAMOND, event['equip']['suit'])
last_event_id += 1

# cards:
# name                  | rank (id = rank - 1) | suit

# vermilion feather fan | 1                    | DIAMOND -- equipped
# duel                  | 2                    | SPADE   <- use this
# slash                 | 3                    | DIAMOND
# dodge                 | 4                    | DIAMOND
# duel                  | 9                    | SPADE
# slash                 | 10                   | HEART

# slash                 | 5                    | CLUB
# sabotage              | 6                    | HEART
# dodge                 | 7                    | DIAMOND
# slash                 | 8                    | DIAMOND
result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[1].player_id],
    'use': [1],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'method': 'abort',
})
assert_eq(ret_code.OK, result['code'])

# cards:
# name                  | rank (id = rank - 1) | suit

# vermilion feather fan | 1                    | DIAMOND -- equipped
# slash                 | 3                    | DIAMOND
# dodge                 | 4                    | DIAMOND
# duel                  | 9                    | SPADE
# slash                 | 10                   | HEART

# slash                 | 5                    | CLUB
# sabotage              | 6                    | HEART
# dodge                 | 7                    | DIAMOND
# slash                 | 8                    | DIAMOND
result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[1].player_id],
    'use': [2],
})
assert_eq(ret_code.OK, result['code'])

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'vermilion feather fan': { 'require': ['forbid'] },
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
    'method': 'vermilion feather fan',
})
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # about to dodge

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
    assert_eq('fire', event['category'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)

# not fan

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
    test_data.CardInfo('vermilion feather fan', 1, card.DIAMOND),
    test_data.CardInfo('duel', 2, card.SPADE),
    test_data.CardInfo('slash', 3, card.DIAMOND),
    test_data.CardInfo('dodge', 4, card.DIAMOND),

    test_data.CardInfo('slash', 5, card.CLUB),
    test_data.CardInfo('slash', 6, card.HEART),
    test_data.CardInfo('dodge', 7, card.DIAMOND),
    test_data.CardInfo('slash', 8, card.DIAMOND),

    test_data.CardInfo('duel', 9, card.SPADE),
    test_data.CardInfo('thunder slash', 10, card.HEART),
])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
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
    'targets': [players[1].player_id],
    'use': [2],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'method': 'abort',
})
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # about to dodge

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

# thunder slash & unequip

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
    test_data.CardInfo('vermilion feather fan', 1, card.DIAMOND),
    test_data.CardInfo('duel', 2, card.SPADE),
    test_data.CardInfo('thunder slash', 3, card.SPADE),
    test_data.CardInfo('dodge', 4, card.DIAMOND),

    test_data.CardInfo('slash', 5, card.CLUB),
    test_data.CardInfo('slash', 6, card.HEART),
    test_data.CardInfo('dodge', 7, card.DIAMOND),
    test_data.CardInfo('slash', 8, card.DIAMOND),

    test_data.CardInfo('duel', 9, card.SPADE),
    test_data.CardInfo('thunder slash', 10, card.HEART),

    test_data.CardInfo('dodge', 11, card.HEART),
    test_data.CardInfo('sabotage', 12, card.HEART),

    test_data.CardInfo('slash', 13, card.SPADE),
    test_data.CardInfo('slash', 1, card.SPADE),
])), pc, ActionStack())
players = [Player(91, 8), Player(1729, 8)]
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
    'targets': [players[1].player_id],
    'use': [2],
})
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # about to dodge

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
    assert_eq('thunder', event['category'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)

result = gc.player_act({
    'token': players[0].token,
    'action': 'abort',
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'action': 'card',
    'targets': [players[0].player_id],
    'use': [11],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'region': 'weapon',
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'action': 'abort',
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[1].player_id],
    'use': [12],
})
assert_eq(ret_code.OK, result['code'])

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'players': [players[1].player_id],
}, gc.hint(players[0].token))
assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'dodge': {
            'require': ['fix card count'],
            'cards': [6, 10],
            'card count': 1,
        },
    },
    'abort': 'allow',
    'players': [players[1].player_id],
}, gc.hint(players[1].token))
