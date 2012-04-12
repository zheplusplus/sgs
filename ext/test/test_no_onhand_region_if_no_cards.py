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
    test_data.CardInfo('rattan armor', 2, card.SPADE),
    test_data.CardInfo('sabotage', 3, card.SPADE),
    test_data.CardInfo('sabotage', 4, card.SPADE),

    test_data.CardInfo('sabotage', 5, card.SPADE),
    test_data.CardInfo('sabotage', 6, card.HEART),
    test_data.CardInfo('sabotage', 7, card.CLUB),
    test_data.CardInfo('sabotage', 8, card.DIAMOND),

    test_data.CardInfo('sabotage', 9, card.HEART),
    test_data.CardInfo('sabotage', 10, card.CLUB),

    test_data.CardInfo('sabotage', 11, card.HEART),
    test_data.CardInfo('sabotage', 12, card.CLUB),
])), pc, ActionStack())
players = [Player(91, 1), Player(1729, 4)]
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
    'token': players[0].token,
    'method': 'discard',
    'discard': [2, 3, 8, 9],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'action': 'card',
    'use': [4],
    'targets': [players[0].player_id],
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
    'regions': ['onhand', 'armor'],
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
    'use': [5],
    'targets': [players[0].player_id],
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
    'regions': ['armor'],
    'players': [players[1].player_id],
}, gc.hint(players[1].token))
