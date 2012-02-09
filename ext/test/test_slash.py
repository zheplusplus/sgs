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
    test_data.CardInfo('slash', 2, card.HEART),
    test_data.CardInfo('slash', 3, card.DIAMOND),
    test_data.CardInfo('slash', 4, card.SPADE),

    test_data.CardInfo('dodge', 5, card.HEART),
    test_data.CardInfo('dodge', 6, card.HEART),
    test_data.CardInfo('dodge', 7, card.DIAMOND),
    test_data.CardInfo('dodge', 8, card.DIAMOND),

    test_data.CardInfo('slash', 9, card.SPADE),
    test_data.CardInfo('slash', 10, card.SPADE),
])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

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

last_event_id = len(gc.get_events(players[0].token, 0)) # until player2

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[1].player_id],
    'use': [0],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'method': 'dodge',
    'discard': [4],
})
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('slash', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('slash', event['use'][0]['name'])
    assert_eq(1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    assert_eq(0, event['use'][0]['id'])
    event = p0_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('dodge', event['play'][0]['name'])
    assert_eq(5, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('slash', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('slash', event['use'][0]['name'])
    assert_eq(1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    event = p1_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, len(event['play']))
    assert_eq('dodge', event['play'][0]['name'])
    assert_eq(5, event['play'][0]['rank'])
    assert_eq(card.HEART, event['play'][0]['suit'])
    assert_eq(4, event['play'][0]['id'])

# not dodged

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
    test_data.CardInfo('slash', 1, card.SPADE),
    test_data.CardInfo('slash', 2, card.HEART),
    test_data.CardInfo('slash', 3, card.DIAMOND),
    test_data.CardInfo('slash', 4, card.SPADE),

    test_data.CardInfo('dodge', 5, card.HEART),
    test_data.CardInfo('dodge', 6, card.HEART),
    test_data.CardInfo('dodge', 7, card.DIAMOND),
    test_data.CardInfo('dodge', 8, card.DIAMOND),

    test_data.CardInfo('slash', 9, card.SPADE),
    test_data.CardInfo('slash', 10, card.SPADE),
])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

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

last_event_id = len(gc.get_events(players[0].token, 0)) # until player2

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'players': [players[0].player_id],
}, gc.hint(players[1].token))

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[1].player_id],
    'use': [0],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'method': 'abort',
})
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('slash', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('slash', event['use'][0]['name'])
    assert_eq(1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    assert_eq(0, event['use'][0]['id'])
    event = p0_events[1]
    assert_eq(players[1].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('normal', event['category'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('slash', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('slash', event['use'][0]['name'])
    assert_eq(1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    assert_eq(p0_events[1], p1_events[1])

# out of range and once again

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
    test_data.CardInfo('slash', 1, card.SPADE),
    test_data.CardInfo('slash', 2, card.HEART),
    test_data.CardInfo('slash', 3, card.DIAMOND),
    test_data.CardInfo('dodge', 4, card.SPADE),

    test_data.CardInfo('dodge', 5, card.HEART),
    test_data.CardInfo('dodge', 6, card.HEART),
    test_data.CardInfo('dodge', 7, card.DIAMOND),
    test_data.CardInfo('dodge', 8, card.DIAMOND),

    test_data.CardInfo('dodge', 9, card.HEART),
    test_data.CardInfo('dodge', 10, card.HEART),
    test_data.CardInfo('dodge', 11, card.DIAMOND),
    test_data.CardInfo('dodge', 12, card.DIAMOND),

    test_data.CardInfo('dodge', 13, card.HEART),
    test_data.CardInfo('dodge', 1, card.HEART),
    test_data.CardInfo('dodge', 2, card.DIAMOND),
    test_data.CardInfo('dodge', 3, card.DIAMOND),

    test_data.CardInfo('dodge', 4, card.HEART),
    test_data.CardInfo('dodge', 5, card.HEART),
])), pc, ActionStack())
players = [Player(2, 4), Player(19, 4), Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        0: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1, 3],
        },
        1: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1, 3],
        },
        2: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1, 3],
        },
        3: { 'type': 'forbid' },
        16: { 'type': 'forbid' },
        17: { 'type': 'forbid' },
    },
    'abort': 'allow',
    'players': [players[0].player_id],
}, gc.hint(players[0].token))

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[2].player_id],
    'use': [0],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'out of range',
}, result)

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[1].player_id],
    'use': [0],
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
            'card count': 1,
            'cards': [4, 5, 6, 7],
        },
    },
    'abort': 'allow',
    'players': [players[1].player_id],
}, gc.hint(players[1].token))

result = gc.player_act({
    'token': players[1].token,
    'method': 'dodge',
    'discard': [4],
})
assert_eq(ret_code.OK, result['code'])

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        1: { 'type': 'forbid' },
        2: { 'type': 'forbid' },
        3: { 'type': 'forbid' },
        16: { 'type': 'forbid' },
        17: { 'type': 'forbid' },
    },
    'abort': 'allow',
    'players': [players[0].player_id],
}, gc.hint(players[0].token))

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[1].player_id],
    'use': [1],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_INCORRECT_INTERFACE,
}, result)
