from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player
import ext.src.skills.martial_saint as martial_saint

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('slash', 1, card.SPADE),
            test_data.CardInfo('dodge', 2, card.HEART),
            test_data.CardInfo('slash', 3, card.CLUB),
            test_data.CardInfo('dodge', 4, card.DIAMOND),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('dodge', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('slash', 8, card.DIAMOND),

            test_data.CardInfo('arson attack', 9, card.HEART),
            test_data.CardInfo('arson attack', 10, card.HEART),
     ])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
martial_saint.add_to(players[0])
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
        1: { 'type': 'forbid' },
        2: {
            'type': 'fix target',
            'target count': 1,
            'targets': [1],
        },
        3: { 'type': 'forbid' },
        8: {
            'type': 'fix target',
            'target count': 1,
            'targets': [0, 1],
        },
        9: {
            'type': 'fix target',
            'target count': 1,
            'targets': [0, 1],
        },
    },
    'methods': {
        'martial saint': {
            'require': ['fix card count', 'fix target'],
            'cards': [1, 3, 8, 9],
            'card count': 1,
            'targets': [1],
            'target count': 1,
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
    'action': 'martial saint',
    'targets': [players[1].player_id],
    'use': [8],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'method': 'dodge',
    'discard': [5],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'action': 'martial saint',
    'targets': [players[1].player_id],
    'use': [9],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_INCORRECT_INTERFACE,
}, result)
