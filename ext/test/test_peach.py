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
            test_data.CardInfo('dodge', 3, card.DIAMOND),
            test_data.CardInfo('slash', 4, card.HEART),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('peach', 6, card.HEART),
            test_data.CardInfo('peach', 7, card.DIAMOND),
            test_data.CardInfo('peach', 8, card.DIAMOND),

            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.SPADE),

            test_data.CardInfo('dodge', 11, card.HEART),
            test_data.CardInfo('dodge', 12, card.DIAMOND),
     ])), pc, ActionStack())
players = [Player(91, 5), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

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

result = gc.player_act({
    'token': players[0].token,
    'action': 'abort',
})
assert_eq(ret_code.OK, result['code'])

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'players': [players[1].player_id],
}, gc.hint(players[0].token))
assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'card': {
        4: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [players[0].player_id],
        },
        5: { 'require': ['implicit target'] },
        6: { 'require': ['implicit target'] },
        7: { 'require': ['implicit target'] },
        10: { 'require': ['forbid'] },
        11: { 'require': ['forbid'] },
    },
    'abort': 'allow',
    'players': [players[1].player_id],
}, gc.hint(players[1].token))

result = gc.player_act({
    'token': players[1].token,
    'action': 'peach',
    'use': [4],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
}, result)

last_event_id = len(gc.get_events(players[0].token, 0)) # about to use peach

result = gc.player_act({
    'token': players[1].token,
    'action': 'card',
    'use': [5],
})
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[1].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('peach', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('peach', event['use'][0]['name'])
    assert_eq(6, event['use'][0]['rank'])
    assert_eq(card.HEART, event['use'][0]['suit'])

    event = p0_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, event['point'])
    assert_eq('VigorRegain', event['type'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[1].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('peach', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('peach', event['use'][0]['name'])
    assert_eq(6, event['use'][0]['rank'])
    assert_eq(card.HEART, event['use'][0]['suit'])
    assert_eq(5, event['use'][0]['id'])

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
        4: {
            'require': ['fix target'],
            'target count': 1,
            'targets': [players[0].player_id],
        },
        6: { 'require': ['forbid'] },
        7: { 'require': ['forbid'] },
        10: { 'require': ['forbid'] },
        11: { 'require': ['forbid'] },
    },
    'abort': 'allow',
    'players': [players[1].player_id],
}, gc.hint(players[1].token))

result = gc.player_act({
    'token': players[1].token,
    'action': 'card',
    'use': [5],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'not own this card',
}, result)

result = gc.player_act({
    'token': players[1].token,
    'action': 'card',
    'use': [6],
})
assert_eq({
    'code': ret_code.BAD_REQUEST,
    'reason': ret_code.BR_WRONG_ARG % 'target not damaged',
}, result)
