from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card

from test_common import *
import test_data
import fake_players_control
import fake_player

pc = fake_players_control.PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('slash', 1, card.SPADE),
            test_data.CardInfo('slash', 2, card.SPADE),
            test_data.CardInfo('slash', 3, card.SPADE),
            test_data.CardInfo('slash', 4, card.SPADE),
            test_data.CardInfo('slash', 5, card.SPADE),
            test_data.CardInfo('slash', 6, card.SPADE),
            test_data.CardInfo('slash', 7, card.SPADE),
            test_data.CardInfo('slash', 8, card.SPADE),
            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.SPADE),
            test_data.CardInfo('slash', 11, card.SPADE),
            test_data.CardInfo('slash', 12, card.SPADE),
            test_data.CardInfo('slash', 13, card.SPADE),
            test_data.CardInfo('dodge', 1, card.HEART),
            test_data.CardInfo('dodge', 2, card.HEART),
            test_data.CardInfo('dodge', 3, card.HEART),
            test_data.CardInfo('dodge', 4, card.HEART),
            test_data.CardInfo('dodge', 5, card.HEART),
     ])), pc, ActionStack())
players = [fake_player.Player(6, 0), fake_player.Player(24, 1),
           fake_player.Player(1729, 2)]
map(lambda p: pc.add_player(p), players)
gc.start()
assert_eq(200, gc.player_act({
                                 'token': players[0].token,
                                 'action': 'give up',
                             })['code'])
assert_eq(200, gc.player_act({
                                 'token': players[0].token,
                                 'discard': [0, 1],
                             })['code'])
assert_eq(200, gc.player_act({
                                 'token': players[1].token,
                                 'action': 'give up',
                             })['code'])
assert_eq(200, gc.player_act({
                                 'token': players[1].token,
                                 'discard': [4, 5],
                             })['code'])

events = gc.events.as_log()
assert_eq(8, len(events))

# game started and 4 cards dealt to each player
assert_eq(0, events[0]['player'])
assert_eq(4, len(events[0]['get']))
if True:
    cards = events[0]['get']
    assert_eq(0, cards[0]['id'])
    assert_eq('slash', cards[0]['name'])
    assert_eq(1, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq(1, cards[1]['id'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(2, cards[1]['rank'])
    assert_eq(card.SPADE, cards[1]['suit'])
    assert_eq(2, cards[2]['id'])
    assert_eq('slash', cards[2]['name'])
    assert_eq(3, cards[2]['rank'])
    assert_eq(card.SPADE, cards[2]['suit'])
    assert_eq(3, cards[3]['id'])
    assert_eq('slash', cards[3]['name'])
    assert_eq(4, cards[3]['rank'])
    assert_eq(card.SPADE, cards[3]['suit'])
assert_eq(1, events[1]['player'])
assert_eq(4, len(events[1]['get']))
if True:
    cards = events[1]['get']
    assert_eq(4, cards[0]['id'])
    assert_eq('slash', cards[0]['name'])
    assert_eq(5, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq(5, cards[1]['id'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(6, cards[1]['rank'])
    assert_eq(card.SPADE, cards[1]['suit'])
    assert_eq(6, cards[2]['id'])
    assert_eq('slash', cards[2]['name'])
    assert_eq(7, cards[2]['rank'])
    assert_eq(card.SPADE, cards[2]['suit'])
    assert_eq(7, cards[3]['id'])
    assert_eq('slash', cards[3]['name'])
    assert_eq(8, cards[3]['rank'])
    assert_eq(card.SPADE, cards[3]['suit'])
assert_eq(2, events[2]['player'])
assert_eq(4, len(events[2]['get']))
if True: # just indent for a nice appearance, card list verifying
    cards = events[2]['get']
    assert_eq(8, cards[0]['id'])
    assert_eq('slash', cards[0]['name'])
    assert_eq(9, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq(9, cards[1]['id'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(10, cards[1]['rank'])
    assert_eq(card.SPADE, cards[1]['suit'])
    assert_eq(10, cards[2]['id'])
    assert_eq('slash', cards[2]['name'])
    assert_eq(11, cards[2]['rank'])
    assert_eq(card.SPADE, cards[2]['suit'])
    assert_eq(11, cards[3]['id'])
    assert_eq('slash', cards[3]['name'])
    assert_eq(12, cards[3]['rank'])
    assert_eq(card.SPADE, cards[3]['suit'])
# player 0's round
assert_eq(0, events[3]['player'])
assert_eq(2, len(events[3]['get']))
if True: # just indent for a nice appearance, card list verifying
    cards = events[3]['get']
    assert_eq(12, cards[0]['id'])
    assert_eq('slash', cards[0]['name'])
    assert_eq(13, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq(13, cards[1]['id'])
    assert_eq('dodge', cards[1]['name'])
    assert_eq(1, cards[1]['rank'])
    assert_eq(card.HEART, cards[1]['suit'])
assert_eq(0, events[4]['player'])
assert_eq(2, len(events[4]['discard']))
if True: # just indent for a nice appearance, card list verifying
    cards = events[4]['discard']
    assert_eq('slash', cards[0]['name'])
    assert_eq(1, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq(0, cards[0]['id'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(2, cards[1]['rank'])
    assert_eq(card.SPADE, cards[1]['suit'])
    assert_eq(1, cards[1]['id'])
# player 1's round
assert_eq(1, events[5]['player'])
assert_eq(2, len(events[5]['get']))
if True: # just indent for a nice appearance, card list verifying
    cards = events[5]['get']
    assert_eq(14, cards[0]['id'])
    assert_eq('dodge', cards[0]['name'])
    assert_eq(2, cards[0]['rank'])
    assert_eq(card.HEART, cards[0]['suit'])
    assert_eq(15, cards[1]['id'])
    assert_eq('dodge', cards[1]['name'])
    assert_eq(3, cards[1]['rank'])
    assert_eq(card.HEART, cards[1]['suit'])
assert_eq(1, events[6]['player'])
assert_eq(2, len(events[6]['discard']))
if True: # just indent for a nice appearance, card list verifying
    cards = events[6]['discard']
    assert_eq('slash', cards[0]['name'])
    assert_eq(5, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq(4, cards[0]['id'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(6, cards[1]['rank'])
    assert_eq(5, cards[1]['id'])
    assert_eq(card.SPADE, cards[1]['suit'])
# player 2's round, beginning only
assert_eq(2, events[7]['player'])
assert_eq(2, len(events[7]['get']))
if True: # just indent for a nice appearance, card list verifying
    cards = events[7]['get']
    assert_eq(16, cards[0]['id'])
    assert_eq('dodge', cards[0]['name'])
    assert_eq(4, cards[0]['rank'])
    assert_eq(card.HEART, cards[0]['suit'])
    assert_eq(17, cards[1]['id'])
    assert_eq('dodge', cards[1]['name'])
    assert_eq(5, cards[1]['rank'])
    assert_eq(card.HEART, cards[1]['suit'])

player0_events = gc.get_events(players[0].token, 0)
assert_eq(8, len(player0_events))
# game started
assert_eq(events[0]['player'], player0_events[0]['player'])
assert_eq(events[0]['get'], player0_events[0]['get'])
assert_eq(events[1]['player'], player0_events[1]['player'])
assert_eq(4, player0_events[1]['get'])
assert_eq(events[2]['player'], player0_events[2]['player'])
assert_eq(4, player0_events[2]['get'])
# player 0's round
assert_eq(events[3]['player'], player0_events[3]['player'])
assert_eq(events[3]['get'], player0_events[3]['get'])
assert_eq(events[4]['player'], player0_events[4]['player'])
assert_eq(events[4]['discard'], player0_events[4]['discard'])
# player 1's round
assert_eq(events[5]['player'], player0_events[5]['player'])
assert_eq(2, player0_events[5]['get'])
assert_eq(events[6]['player'], player0_events[6]['player'])
if True: # just indent for a nice appearance, card list verifying
    cards = player0_events[6]['discard']
    assert_eq('slash', cards[0]['name'])
    assert_eq(5, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(6, cards[1]['rank'])
    assert_eq(card.SPADE, cards[1]['suit'])
# player 2's round
assert_eq(events[7]['player'], player0_events[7]['player'])
assert_eq(2, player0_events[5]['get'])

player1_events = gc.get_events(players[1].token, 0)
assert_eq(8, len(player1_events))
# game started
assert_eq(events[0]['player'], player1_events[0]['player'])
assert_eq(4, player1_events[0]['get'])
assert_eq(events[1]['player'], player1_events[1]['player'])
assert_eq(events[1]['get'], player1_events[1]['get'])
assert_eq(events[2]['player'], player1_events[2]['player'])
assert_eq(4, player1_events[2]['get'])
# player 0's round
assert_eq(events[3]['player'], player1_events[3]['player'])
assert_eq(2, player1_events[3]['get'])
assert_eq(events[4]['player'], player1_events[4]['player'])
if True: # just indent for a nice appearance, card list verifying
    cards = player1_events[4]['discard']
    assert_eq('slash', cards[0]['name'])
    assert_eq(1, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(2, cards[1]['rank'])
    assert_eq(card.SPADE, cards[1]['suit'])
# player 1's round
assert_eq(events[5]['player'], player1_events[5]['player'])
assert_eq(events[5]['get'], player1_events[5]['get'])
assert_eq(events[6]['player'], player1_events[6]['player'])
assert_eq(events[6]['discard'], player1_events[6]['discard'])
# player 2's round
assert_eq(events[7]['player'], player1_events[7]['player'])
assert_eq(2, player1_events[7]['get'])

player2_events = gc.get_events(players[2].token, 0)
assert_eq(8, len(player2_events))
# game started
assert_eq(events[0]['player'], player2_events[0]['player'])
assert_eq(4, player2_events[0]['get'])
assert_eq(events[1]['player'], player2_events[1]['player'])
assert_eq(4, player2_events[1]['get'])
assert_eq(events[2]['player'], player2_events[2]['player'])
assert_eq(events[2]['get'], player2_events[2]['get'])
# player 0's round
assert_eq(events[3]['player'], player2_events[3]['player'])
assert_eq(2, player2_events[3]['get'])
assert_eq(events[4]['player'], player2_events[4]['player'])
if True: # just indent for a nice appearance, card list verifying
    cards = player2_events[4]['discard']
    assert_eq('slash', cards[0]['name'])
    assert_eq(1, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(2, cards[1]['rank'])
    assert_eq(card.SPADE, cards[1]['suit'])
# player 1's round
assert_eq(events[5]['player'], player2_events[5]['player'])
assert_eq(2, player2_events[5]['get'])
assert_eq(events[6]['player'], player2_events[6]['player'])
if True: # just indent for a nice appearance, card list verifying
    cards = player2_events[6]['discard']
    assert_eq('slash', cards[0]['name'])
    assert_eq(5, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(6, cards[1]['rank'])
    assert_eq(card.SPADE, cards[1]['suit'])
# player 2's round
assert_eq(events[7]['player'], player2_events[7]['player'])
assert_eq(events[7]['get'], player2_events[7]['get'])

player2_events_after_2 = gc.get_events(players[2].token, 2)
assert_eq(6, len(player2_events_after_2))
# game started
assert_eq(events[2]['player'], player2_events_after_2[0]['player'])
assert_eq(events[2]['get'], player2_events_after_2[0]['get'])
# player 0's round
assert_eq(events[3]['player'], player2_events_after_2[1]['player'])
assert_eq(2, player2_events_after_2[1]['get'])
assert_eq(events[4]['player'], player2_events_after_2[2]['player'])
if True: # just indent for a nice appearance, card list verifying
    cards = player2_events_after_2[2]['discard']
    assert_eq('slash', cards[0]['name'])
    assert_eq(1, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(2, cards[1]['rank'])
    assert_eq(card.SPADE, cards[1]['suit'])
# player 1's round
assert_eq(events[5]['player'], player2_events_after_2[3]['player'])
assert_eq(2, player2_events_after_2[3]['get'])
assert_eq(events[6]['player'], player2_events_after_2[4]['player'])
if True: # just indent for a nice appearance, card list verifying
    cards = player2_events_after_2[4]['discard']
    assert_eq('slash', cards[0]['name'])
    assert_eq(5, cards[0]['rank'])
    assert_eq(card.SPADE, cards[0]['suit'])
    assert_eq('slash', cards[1]['name'])
    assert_eq(6, cards[1]['rank'])
    assert_eq(card.SPADE, cards[1]['suit'])
# player 2's round
assert_eq(events[7]['player'], player2_events_after_2[5]['player'])
assert_eq(events[7]['get'], player2_events_after_2[5]['get'])
