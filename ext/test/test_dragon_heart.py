from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player
import ext.src.skills.dragon_heart as dragon_heart

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

            test_data.CardInfo('dodge', 9, card.HEART),
            test_data.CardInfo('dodge', 10, card.HEART),
     ])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
dragon_heart.add_to(players[0])
dragon_heart.add_to(players[1])
gc.start()

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        0: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        1: { 'require': ['forbid'] },
        2: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [1],
        },
        3: { 'require': ['forbid'] },
        8: { 'require': ['forbid'] },
        9: { 'require': ['forbid'] },
    },
    'methods': {
        'dragon heart': {
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
    'action': 'dragon heart',
    'targets': [players[1].player_id],
    'use': [3],
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
            'cards': [5, 6],
        },
        'dragon heart': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [4, 7],
        },
    },
    'abort': 'allow',
    'players': [players[1].player_id],
}, gc.hint(players[1].token))

result = gc.player_act({
    'token': players[1].token,
    'method': 'dragon heart',
    'discard': [4],
})
assert_eq(ret_code.OK, result['code'])

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        0: { 'require': ['forbid'] },
        1: { 'require': ['forbid'] },
        2: { 'require': ['forbid'] },
        8: { 'require': ['forbid'] },
        9: { 'require': ['forbid'] },
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
    'action': 'dragon heart',
    'targets': [players[1].player_id],
    'use': [1],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_INCORRECT_INTERFACE,
}, result)
