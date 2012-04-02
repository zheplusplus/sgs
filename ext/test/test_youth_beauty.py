from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player
import ext.src.skills.heavenly_scent as heavenly_scent
import ext.src.skills.youth_beauty as youth_beauty

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('slash', 1, card.SPADE),
            test_data.CardInfo('rattan armor', 2, card.CLUB),
            test_data.CardInfo('slash', 3, card.HEART),
            test_data.CardInfo('slash', 4, card.HEART),

            test_data.CardInfo('rattan armor', 2, card.SPADE),
            test_data.CardInfo('arson attack', 6, card.HEART),
            test_data.CardInfo('arson attack', 7, card.HEART),
            test_data.CardInfo('duel', 8, card.HEART),

            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.CLUB),

            test_data.CardInfo('dodge', 11, card.HEART),
            test_data.CardInfo('dodge', 12, card.HEART),

            test_data.CardInfo('slash', 13, card.CLUB),
            test_data.CardInfo('dodge', 1, card.DIAMOND),
            test_data.CardInfo('dodge', 2, card.DIAMOND),
            test_data.CardInfo('dodge', 3, card.DIAMOND),
     ])), pc, ActionStack())
players = [Player(91, 3), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
heavenly_scent.add_to(players[0])
youth_beauty.add_to(players[0])
gc.start()

# cards:
# name         | rank | id | suit

# slash        | 1    | 0  | SPADE
# rattan armor | 2    | 1  | CLUB <- equip this
# slash        | 3    | 2  | HEART <- discard this
# slash        | 4    | 3  | HEART <- discard this
# slash        | 9    | 8  | SPADE
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 4  | SPADE
# arson attack | 6    | 5  | HEART
# arson attack | 7    | 6  | HEART
# duel         | 8    | 7  | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'equip',
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
                           'discard': [2, 3],
                       })
assert_eq(ret_code.OK, result['code'])

# cards:
# name         | rank | id | suit

# slash        | 1    | 0  | SPADE
# rattan armor | 2    | 1  | CLUB <- equipped
# slash        | 9    | 8  | SPADE
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 4  | SPADE
# arson attack | 6    | 5  | HEART <- use this
# arson attack | 7    | 6  | HEART
# duel         | 8    | 7  | HEART
# dodge        | 11   | 10 | HEART <- discard this
# dodge        | 12   | 11 | HEART
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'arson attack',
                           'targets': [players[0].player_id],
                           'use': [5],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'discard': [0],
                       })
assert_eq(ret_code.OK, result['code'])

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'players': [players[1].player_id],
}, gc.hint(players[0].token))

assert_eq({
    'code': ret_code.OK,
    'action': 'discard',
    'methods': {
        'discard': {
            'require': ['fix card count'],
            'card count': 1,
            'cards': [6, 7, 10, 11],
        },
    },
    'abort': 'allow',
    'players': [players[1].player_id],
}, gc.hint(players[1].token))

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'discard',
                           'discard': [10],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'action': 'arson attack',
                           'targets': [players[0].player_id],
                           'use': [5],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_PLAYER_FORBID,
          }, result)

assert_eq({
    'code': ret_code.OK,
    'action': 'use',
    'methods': {
        'heavenly scent': {
            'require': ['fix card count', 'fix target'],
            'target count': 1,
            'targets': [players[1].player_id],
            'cards': [0, 8],
            'card count': 1,
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
                           'targets': [players[0].player_id],
                           'action': 'use',
                           'use': [8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'forbid target self',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'targets': map(lambda p: p.player_id, players),
                           'action': 'use',
                           'use': [8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong targets count',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'targets': [players[1].player_id],
                           'action': 'use',
                           'use': [9],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'targets': [players[1].player_id],
                           'action': 'use',
                           'use': [0, 8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'wrong cards',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'targets': [players[1].player_id],
                           'use': [8],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_MISSING_ARG % 'action',
          }, result)

result = gc.player_act({
                           'token': players[0].token,
                           'targets': [players[1].player_id],
                           'action': 'use',
                           'use': [2],
                       })
assert_eq({
              'code': ret_code.BAD_REQUEST,
              'reason': ret_code.BR_WRONG_ARG % 'not own this card',
          }, result)

last_event_id = len(gc.get_events(players[0].token, 0)) # until discard a card

# cards:
# name         | rank | id | suit

# slash        | 1    | 0  | SPADE
# rattan armor | 2    | 1  | CLUB <- equipped
# slash        | 9    | 8  | SPADE <- use this
# slash        | 10   | 9  | CLUB

# rattan armor | 2    | 4  | SPADE
# arson attack | 7    | 6  | HEART
# duel         | 8    | 7  | HEART
# dodge        | 12   | 11 | HEART
result = gc.player_act({
                           'token': players[0].token,
                           'action': 'use',
                           'targets': [players[1].player_id],
                           'use': [8],
                       })
assert_eq(ret_code.OK, result['code'])

p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(4, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(1, len(event['discard']))
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(9, event['discard'][0]['rank'])
    assert_eq(card.SPADE, event['discard'][0]['suit'])
    assert_eq(8, event['discard'][0]['id'])
    event = p0_events[1]
    assert_eq('Invocation', event['type'])
    assert_eq(players[0].player_id, event['player'])
    assert_eq('heavenly scent', event['invoke'])
    assert_eq([players[1].player_id], event['targets'])
    event = p0_events[2]
    assert_eq(players[1].player_id, event['victim'])
    assert_eq(1, event['damage'])
    assert_eq('fire', event['category'])
    event = p0_events[3]
    assert_eq(1, event['draw'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(4, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(1, len(event['discard']))
    assert_eq('slash', event['discard'][0]['name'])
    assert_eq(9, event['discard'][0]['rank'])
    assert_eq(card.SPADE, event['discard'][0]['suit'])
    assert_eq(p0_events[1], p1_events[1])
    assert_eq(p0_events[2], p1_events[2])
    event = p1_events[3]
    assert_eq(1, len(event['draw']))
    assert_eq(13, event['draw'][0]['rank'])
    assert_eq(card.CLUB, event['draw'][0]['suit'])
    assert_eq('slash', event['draw'][0]['name'])
    assert_eq(12, event['draw'][0]['id'])

# cards:
# name         | rank | id | suit

# rattan armor | 2    | 1  | CLUB <- equipped
# slash        | 4    | 3  | HEART
# slash        | 10   | 9  | CLUB <- show this

# rattan armor | 2    | 4  | SPADE
# arson attack | 7    | 6  | HEART <- use this
# duel         | 8    | 7  | HEART
# dodge        | 12   | 11 | HEART
# slash        | 13   | 12 | CLUB
result = gc.player_act({
                           'token': players[1].token,
                           'action': 'card',
                           'targets': [players[0].player_id],
                           'use': [6],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[0].token,
                           'method': 'discard',
                           'discard': [9],
                       })
assert_eq(ret_code.OK, result['code'])

result = gc.player_act({
                           'token': players[1].token,
                           'method': 'discard',
                           'discard': [12],
                       })
assert_eq(ret_code.OK, result['code'])
