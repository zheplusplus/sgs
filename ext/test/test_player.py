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
            test_data.CardInfo('arson attack', 2, card.HEART),
            test_data.CardInfo('dodge', 3, card.DIAMOND),
            test_data.CardInfo('arson attack', 4, card.HEART),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('arson attack', 6, card.HEART),
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

# cards:
# name         | rank (id = rank - 1) | suit

# slash        | 1                    | SPADE
# arson attack | 2                    | HEART
# dodge        | 3                    | DIAMOND
# arson attack | 4                    | HEART
# slash        | 9                    | SPADE
# slash        | 10                   | SPADE

# slash        | 5                    | CLUB
# arson attack | 6                    | HEART
# dodge        | 7                    | DIAMOND
# dodge        | 8                    | DIAMOND
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
        2: { 'require': ['forbid'] },
        3: {
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

result = gc.player_act({
        'token': players[0].token,
        'action': 'abort',
    })

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'discard': {
            'require': ['fix card count'],
            'card count': 2,
            'cards': [0, 1, 2, 3, 8, 9],
        },
    },
    'players': [players[0].player_id],
}, gc.hint(players[0].token))
assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'players': [players[0].player_id],
}, gc.hint(players[1].token))
