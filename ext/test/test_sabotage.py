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

            test_data.CardInfo('slash', 5, card.SPADE),
            test_data.CardInfo('dodge', 6, card.HEART),
            test_data.CardInfo('slash', 7, card.CLUB),
            test_data.CardInfo('dodge', 8, card.DIAMOND),

            test_data.CardInfo('sabotage', 9, card.HEART),
            test_data.CardInfo('sabotage', 10, card.CLUB),
     ])), pc, ActionStack())
players = [Player(91, 0), Player(1729, 1)]
map(lambda p: pc.add_player(p), players)
gc.start()

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

def check_random_sabotage_card(c, with_id):
    if c['rank'] == 5:
        assert_eq('slash', c['name'])
        assert_eq(card.SPADE, c['suit'])
    if c['rank'] == 6:
        assert_eq('dodge', c['name'])
        assert_eq(card.HEART, c['suit'])
    if c['rank'] == 7:
        assert_eq('slash', c['name'])
        assert_eq(card.CLUB, c['suit'])
    if c['rank'] == 8:
        assert_eq('dodge', c['name'])
        assert_eq(card.DIAMOND, c['suit'])
    if with_id:
        assert_eq(c['id'], c['rank'] - 1)
    else:
        assert not 'id' in c
sabotage_rank_accumulate = 0

for i in range(0, 3):
    result = gc.player_act({
                               'token': players[0].token,
                               'action': 'sabotage',
                               'targets': [players[1].player_id],
                               'cards': [i],
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
        assert_eq(i + 1, event['use'][0]['rank'])
        assert_eq(card.SPADE, event['use'][0]['suit'])
    p1_events = gc.get_events(players[1].token, last_event_id)
    assert_eq(p0_events, p1_events)
    last_event_id += 1

    result = gc.player_act({
                               'token': players[0].token,
                               'sabotage': 'cards',
                           })
    assert_eq(ret_code.OK, result['code'])
    p0_events = gc.get_events(players[0].token, last_event_id)
    assert_eq(1, len(p0_events))
    if True: # just indent for a nice appearance
        event = p0_events[0]
        assert_eq(players[1].player_id, event['player'])
        assert_eq('cards', event['type'])
        assert_eq(1, len(event['cards']))
        check_random_sabotage_card(event['cards'][0], False)
    sabotage_rank_accumulate += event['cards'][0]['rank']

    p1_events = gc.get_events(players[1].token, last_event_id)
    assert_eq(1, len(p1_events))
    if True: # just indent for a nice appearance
        event = p0_events[0]
        assert_eq(players[1].player_id, event['player'])
        assert_eq('cards', event['type'])
        assert_eq(1, len(event['cards']))
        check_random_sabotage_card(event['cards'][0], True)
    last_event_id += 1

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [2],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'cards': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'targets',
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'sabotage',
                           'targets': [players[0].player_id],
                           'cards': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[0].player_id],
                           'cards': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [],
                           'cards': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [],
                           'cards': [3],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [3, 8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [3],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'sabotage',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'sabotage': 'undef',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'sabotage': 'undef',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)

result = gc.player_act({
                           'token': players[1].token,
                           'sabotage': 'cards',
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'sabotage': 'cards',
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p0_events))
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['user'])
    assert_eq(1, len(event['targets']))
    assert_eq(players[1].player_id, event['targets'][0])
    assert_eq('sabotage', event['action'])
    assert_eq(1, len(event['use']))
    assert_eq('sabotage', event['use'][0]['name'])
    assert_eq(i + 1, event['use'][0]['rank'])
    assert_eq(card.SPADE, event['use'][0]['suit'])
last_event_id += 1
assert_eq(p0_events[0], p1_events[0])

if True: # just indent for a nice appearance
    event = p0_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq('cards', event['type'])
    assert_eq(1, len(event['cards']))
    check_random_sabotage_card(event['cards'][0], False)
if True: # just indent for a nice appearance
    event = p0_events[1]
    assert_eq(players[1].player_id, event['player'])
    assert_eq('cards', event['type'])
    assert_eq(1, len(event['cards']))
    check_random_sabotage_card(event['cards'][0], True)
last_event_id += 1

sabotage_rank_accumulate += p0_events[1]['cards'][0]['rank']
assert_eq(5 + 6 + 7 + 8, sabotage_rank_accumulate)

result = gc.player_act({
                           'token': players[0].token,
                           'action': 'sabotage',
                           'targets': [players[1].player_id],
                           'cards': [8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG,
          }, result)
