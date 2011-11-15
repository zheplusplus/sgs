from core.src.game_control import GameControl
from core.src.player import Player
from core.src.event import EventList
import core.src.card as card
import core.src.ret_code as ret_code

from test_common import *
import cards_gen
import fake_card_pool
import fake_players_control

pc = fake_players_control.PlayersControl()
gc = GameControl(EventList(), fake_card_pool.CardPool(cards_gen.generate([
            cards_gen.CardInfo('slash', 1, card.SPADE),
            cards_gen.CardInfo('fire attack', 2, card.HEART),
            cards_gen.CardInfo('dodge', 3, card.DIAMOND),
            cards_gen.CardInfo('fire attack', 4, card.HEART),
            cards_gen.CardInfo('slash', 5, card.CLUB),
            cards_gen.CardInfo('fire attack', 6, card.HEART),
            cards_gen.CardInfo('dodge', 7, card.DIAMOND),
            cards_gen.CardInfo('dodge', 8, card.DIAMOND),
            cards_gen.CardInfo('slash', 9, card.SPADE),
            cards_gen.CardInfo('slash', 10, card.SPADE),
    ])), pc)
players = [Player(91, 0), Player(1729, 1)]
map(lambda p: pc.add_player(p), players)
gc.start()
gc.next_round()
pc.next_player()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

result = gc.player_act({
        'token': players[0].token,
        'action': 'fire attack',
        'targets': [players[1].player_id],
        'cards': [1],
    })
assert_eq(ret_code.OK, result['code'])
'''
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_event))
if True: # just indent for a nice appearance, card list verifying
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['target'][0])
    assert_eq('fire attack', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq(1, event['use'][0])
p1_events = gc.get_events(players[1].token, last_event_id)
last_event_id += 1
'''
result = gc.player_act({
        'token': players[1].token,
        'action': 'show',
        'cards': [6],
    })
assert_eq(ret_code.OK, result['code'])
'''
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_event))
if True: # just indent for a nice appearance, card list verifying
    event = p0_events[0]
    assert_eq(players[1].player_id, event['player_id'])
    assert_eq(1, len(event['show']))
    assert_eq(6, event['cards'][0])
p1_events = gc.get_events(players[1].token, last_event_id)
last_event_id += 1
'''
result = gc.player_act({
        'token': players[0].token,
        'action': 'discard',
        'cards': [2],
    })
assert_eq(ret_code.OK, result['code'])
'''
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_event))
if True: # just indent for a nice appearance, card list verifying
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player_id'])
    assert_eq(1, len(event['discard']))
    assert_eq(2, event['discard'][0])
if True: # just indent for a nice appearance, card list verifying
    event = p0_events[1]
    assert_eq(players[1].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('fire', event['category'])
p1_events = gc.get_events(players[1].token, last_event_id)
'''
