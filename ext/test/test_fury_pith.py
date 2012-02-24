from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player
import ext.src.skills.fury_pith as fury_pith

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('+jueying', 5, card.SPADE),
            test_data.CardInfo('duel', 2, card.HEART),
            test_data.CardInfo('duel', 3, card.HEART),
            test_data.CardInfo('duel', 4, card.HEART),

            test_data.CardInfo('dodge', 5, card.DIAMOND),
            test_data.CardInfo('slash', 6, card.HEART),
            test_data.CardInfo('slash', 7, card.HEART),
            test_data.CardInfo('slash', 8, card.HEART),

            test_data.CardInfo('duel', 9, card.HEART),
            test_data.CardInfo('duel', 10, card.HEART),
     ])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
fury_pith.add_to(players[1])
gc.start()

# cards:
# name     | rank | id | suit

# +jueying | 1    | 0  | SPADE
# duel     | 2    | 1  | HEART <- use this
# duel     | 3    | 2  | HEART
# duel     | 4    | 3  | HEART
# duel     | 9    | 8  | HEART
# duel     | 10   | 9  | HEART

# dodge    | 5    | 4  | DIAMOND
# slash    | 6    | 5  | HEART
# slash    | 7    | 6  | HEART
# slash    | 8    | 7  | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'duel',
                           'targets': [players[1].player_id],
                           'use': [1],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until duel

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'abort',
                           'play': [],
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

# cards:
# name     | rank | id | suit

# +jueying | 1    | 0  | SPADE
# duel     | 3    | 2  | HEART <- use this
# duel     | 4    | 3  | HEART
# duel     | 9    | 8  | HEART
# duel     | 10   | 9  | HEART

# dodge    | 5    | 4  | DIAMOND
# slash    | 6    | 5  | HEART <- play this
# slash    | 7    | 6  | HEART
# slash    | 8    | 7  | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'duel',
                           'targets': [players[1].player_id],
                           'use': [2],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'slash',
                           'play': [5],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until duel

result = gc.player_act({
                           'token': players[0].token,
                           'method': 'abort',
                           'play': [],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('normal', event['category'])
    event = p0_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq(1, event['point'])
    assert_eq('VigorRegain', event['type'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)

# cards:
# name     | rank | id | suit

# +jueying | 1    | 0  | SPADE
# duel     | 4    | 3  | HEART <- use this
# duel     | 9    | 8  | HEART
# duel     | 10   | 9  | HEART

# dodge    | 5    | 4  | DIAMOND
# slash    | 7    | 6  | HEART
# slash    | 8    | 7  | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'duel',
                           'targets': [players[1].player_id],
                           'use': [3],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until duel

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'abort',
                           'play': [],
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

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
                           'use': [0],
                       })
assert_eq(ret_code.OK, result['code'])

# cards:
# name     | rank | id | suit

# +jueying | 1    | 0  | SPADE <- equipped
# duel     | 9    | 8  | HEART <- use this
# duel     | 10   | 9  | HEART

# dodge    | 5    | 4  | DIAMOND
# slash    | 7    | 6  | HEART <- play this
# slash    | 8    | 7  | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'duel',
                           'targets': [players[1].player_id],
                           'use': [8],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'slash',
                           'play': [6],
                       })
assert_eq(ret_code.OK, result['code'])

last_event_id = len(gc.get_events(players[0].token, 0)) # until duel

result = gc.player_act({
                           'token': players[0].token,
                           'method': 'abort',
                           'play': [],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('normal', event['category'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(p0_events, p1_events)
