from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player
import ext.src.skills.intellect_gathering as intellect_gathering

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
    test_data.CardInfo('duel', 1, card.SPADE),
    test_data.CardInfo('arson attack', 2, card.DIAMOND),
    test_data.CardInfo('sabotage', 3, card.CLUB),
    test_data.CardInfo('slash', 4, card.HEART),

    test_data.CardInfo('slash', 5, card.CLUB),
    test_data.CardInfo('slash', 6, card.HEART),
    test_data.CardInfo('slash', 7, card.HEART),
    test_data.CardInfo('slash', 8, card.HEART),

    test_data.CardInfo('slash', 9, card.SPADE),
    test_data.CardInfo('slash', 10, card.CLUB),

    test_data.CardInfo('slash', 11, card.CLUB),
    test_data.CardInfo('slash', 12, card.HEART),
    test_data.CardInfo('steal', 13, card.CLUB),
    test_data.CardInfo('slash', 2, card.CLUB),
])), pc, ActionStack())
players = [Player(91, 3), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
intellect_gathering.add_to(players[0])
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until start

result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'use': [0],
    'targets': [players[1].player_id],
})
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(1, len(event['use']))
    assert_eq('duel', event['use'][0]['name'])
    assert_eq(1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    assert_eq(0, event['use'][0]['id'])
    event = p0_events[1]
    assert_eq(1, len(event['draw']))
    assert_eq('slash', event['draw'][0]['name'])
    assert_eq(11, event['draw'][0]['rank'])
    assert_eq(card.CLUB, event['draw'][0]['suit'])
    assert_eq(10, event['draw'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(1, len(event['use']))
    assert_eq('duel', event['use'][0]['name'])
    assert_eq(1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
    event = p1_events[1]
    assert_eq(1, event['draw'])

result = gc.player_act({
    'token': players[1].token,
    'method': 'slash',
    'discard': [4],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'method': 'slash',
    'discard': [10],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[1].token,
    'method': 'abort',
})
assert_eq(ret_code.OK, result['code'])

# cards:
# name         | rank | id | suit

# arson attack | 2    | 1  | DIAMOND <- use this
# sabotage     | 3    | 2  | CLUB
# slash        | 4    | 3  | HEART
# slash (draw) | 12   | 11 | HEART

# slash        | 6    | 5  | HEART
# slash        | 7    | 6  | HEART
# slash        | 8    | 7  | HEART
result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'use': [1],
    'targets': [players[0].player_id],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'method': 'show',
    'discard': [11],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'method': 'discard',
    'discard': [11],
})
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until using cards

# cards:
# name         | rank | id | suit

# sabotage     | 3    | 2  | CLUB <- use this
# slash        | 4    | 3  | HEART

# slash        | 6    | 5  | HEART
# slash        | 7    | 6  | HEART
# slash        | 8    | 7  | HEART
result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'use': [2],
    'targets': [players[1].player_id],
})
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(3, event['use'][0]['rank'])
    assert_eq(card.CLUB, event['use'][0]['suit'])
    assert_eq(2, event['use'][0]['id'])
    event = p0_events[1]
    assert_eq(1, len(event['draw']))
    assert_eq('steal', event['draw'][0]['name'])
    assert_eq(13, event['draw'][0]['rank'])
    assert_eq(card.CLUB, event['draw'][0]['suit'])
    assert_eq(12, event['draw'][0]['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(3, event['use'][0]['rank'])
    assert_eq(card.CLUB, event['use'][0]['suit'])
    event = p1_events[1]
    assert_eq(1, event['draw'])

result = gc.player_act({
    'token': players[0].token,
    'region': 'onhand',
})
assert_eq(ret_code.OK, result['code'])

# cards:
# name         | rank | id | suit

# slash        | 4    | 3  | HEART
# steal        | 13   | 12 | CLUB <- use this

# slash        | 6    | 5  | HEART
# slash        | 7    | 6  | HEART
# slash        | 8    | 7  | HEART
result = gc.player_act({
    'token': players[0].token,
    'action': 'card',
    'use': [12],
    'targets': [players[1].player_id],
})
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
    'token': players[0].token,
    'region': 'onhand',
})
assert_eq(ret_code.OK, result['code'])
