from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.src.player import Player

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('sabotage', 1, card.SPADE),
            test_data.CardInfo('sabotage', 2, card.SPADE),
            test_data.CardInfo('sabotage', 3, card.SPADE),
            test_data.CardInfo('sabotage', 4, card.SPADE),

            test_data.CardInfo('dodge', 5, card.DIAMOND),
            test_data.CardInfo('dodge', 6, card.DIAMOND),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('dodge', 8, card.DIAMOND),

            test_data.CardInfo('sabotage', 9, card.HEART),
            test_data.CardInfo('sabotage', 10, card.CLUB),
     ])), pc, ActionStack())
players = [Player(91, 0), Player(1729, 1)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards
result = gc.player_act({
        'token': players[0].token,
        'action': 'sabotage',
        'targets': [players[1].player_id],
        'cards': [0],
    })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('sabotage', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
p1_events = gc.get_events(players[1].token, last_event_id)
last_event_id += 1

result = gc.player_act({
        'token': players[0].token,
        'sabotage': 'cards',
    })
