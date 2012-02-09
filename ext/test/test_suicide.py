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
            test_data.CardInfo('arson attack', 1, card.HEART),
            test_data.CardInfo('slash', 2, card.CLUB),
            test_data.CardInfo('slash', 3, card.HEART),
            test_data.CardInfo('slash', 4, card.HEART),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('slash', 6, card.CLUB),
            test_data.CardInfo('slash', 7, card.CLUB),
            test_data.CardInfo('slash', 8, card.CLUB),

            test_data.CardInfo('slash', 9, card.CLUB),
            test_data.CardInfo('slash', 10, card.CLUB),
            test_data.CardInfo('slash', 11, card.CLUB),
            test_data.CardInfo('slash', 12, card.CLUB),

            test_data.CardInfo('slash', 13, card.CLUB),
            test_data.CardInfo('slash', 1, card.SPADE),

            test_data.CardInfo('slash', 2, card.SPADE),
            test_data.CardInfo('slash', 3, card.SPADE),

            test_data.CardInfo('slash', 4, card.SPADE),
            test_data.CardInfo('slash', 5, card.SPADE),

            test_data.CardInfo('slash', 6, card.SPADE),
            test_data.CardInfo('slash', 7, card.SPADE),
     ])), pc, ActionStack())
players = [Player(19, 1), Player(91, 1), Player(1729, 1)]
map(lambda p: pc.add_player(p), players)
gc.start()

# cards:
# name         | rank | id | suit

# arson attack | 1    | 0  | HEART <- use this
# slash        | 2    | 1  | SPADE <- show and discard this
# slash        | 3    | 2  | HEART
# slash        | 4    | 3  | HEART
# slash        | 13   | 12 | CLUB
# slash        | 1    | 13 | CLUB
result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'targets': [players[0].player_id],
    'use': [0],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'discard': [1],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'method': 'discard',
    'discard': [1],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'method': 'abort',
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'method': 'abort',
})
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until player2

result = gc.player_act({
    'token': players[2].token,
    'method': 'abort',
})
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('PlayerKilled', event['type'])
    event = p0_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(2, event['draw'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    assert_eq(p0_events[0], p1_events[0])
    event = p1_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(2, len(event['draw']))
    assert_eq(2, event['draw'][0]['rank'])
    assert_eq(card.SPADE, event['draw'][0]['suit'])
    assert_eq('slash', event['draw'][0]['name'])
    assert_eq(14, event['draw'][0]['id'])
    assert_eq(3, event['draw'][1]['rank'])
    assert_eq(card.SPADE, event['draw'][1]['suit'])
    assert_eq('slash', event['draw'][1]['name'])
    assert_eq(15, event['draw'][1]['id'])
p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(p0_events, p2_events)

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'discard': [5, 6, 7, 14, 15],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[2].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[2].token,
                           'discard': [9, 10, 11, 16, 17],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'abort',
                       })
assert_eq(ret_code.OK, result['code'])
