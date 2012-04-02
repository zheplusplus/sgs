from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player
import ext.src.skills.surprise_raid as surprise_raid

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('zhangba serpent spear', 12, card.SPADE),
            test_data.CardInfo('slash', 2, card.CLUB),
            test_data.CardInfo('slash', 3, card.CLUB),
            test_data.CardInfo('dodge', 4, card.DIAMOND),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('dodge', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('slash', 8, card.DIAMOND),

            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.SPADE),
     ])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
surprise_raid.add_to(players[0])
gc.start()

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
    'methods': {
        'surprise raid': {
            'require': ['fix card count', 'fix target'],
            'card count': 1,
            'cards': [0, 1, 2, 8, 9],
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

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
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
    'methods': {
        'surprise raid': {
            'require': ['fix card count', 'fix target'],
            'card count': 1,
            'cards': [0, 1, 2, 8, 9],
            'target count': 1,
            'targets': [1],
        },
        'zhangba serpent spear': {
            'require': ['fix card count', 'fix target'],
            'card count': 2,
            'cards': [1, 2, 3, 8, 9],
            'target count': 1,
            'targets': [1],
        },
    },
    'abort': 'allow',
    'players': [players[0].player_id],
}, gc.hint(players[0].token))

result = gc.player_act({
    'token': players[0].token,
    'action': 'surprise raid',
    'targets': [1],
    'use': [0],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'region': 'onhand',
})
assert_eq(ret_code.OK, result['code'])

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
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
    'methods': {
        'surprise raid': {
            'require': ['fix card count', 'fix target'],
            'card count': 1,
            'cards': [1, 2, 8, 9],
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
    'action': 'surprise raid',
    'targets': [1],
    'use': [0],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'not own this card',
}, result)

result = gc.player_act({
    'token': players[0].token,
    'action': 'surprise raid',
    'targets': [1],
    'use': [3],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
}, result)

result = gc.player_act({
    'token': players[0].token,
    'action': 'surprise raid',
    'targets': [1],
    'use': [1, 2],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
}, result)

result = gc.player_act({
    'token': players[0].token,
    'action': 'surprise raid',
    'targets': [1],
    'use': [1],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'region': 'onhand',
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'action': 'surprise raid',
    'targets': [1],
    'use': [2],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'region': 'onhand',
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'action': 'surprise raid',
    'targets': [1],
    'use': [8],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'region': 'onhand',
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'action': 'surprise raid',
    'targets': [1],
    'use': [9],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'forbid target no card',
}, result)

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        3: { 'require': ['forbid'] },
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
