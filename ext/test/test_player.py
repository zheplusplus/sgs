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
            test_data.CardInfo('fire attack', 2, card.HEART),
            test_data.CardInfo('dodge', 3, card.DIAMOND),
            test_data.CardInfo('fire attack', 4, card.HEART),

            test_data.CardInfo('slash', 5, card.CLUB),
            test_data.CardInfo('fire attack', 6, card.HEART),
            test_data.CardInfo('dodge', 7, card.DIAMOND),
            test_data.CardInfo('dodge', 8, card.DIAMOND),

            test_data.CardInfo('slash', 9, card.SPADE),
            test_data.CardInfo('slash', 10, card.SPADE),

            test_data.CardInfo('dodge', 11, card.HEART),
            test_data.CardInfo('dodge', 12, card.DIAMOND),
     ])), pc, ActionStack())
players = [Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

# cards:
# name        | rank (id = rank - 1) | suit

# slash       | 1                    | SPADE
# fire attack | 2                    | HEART
# dodge       | 3                    | DIAMOND
# fire attack | 4                    | HEART
# slash       | 9                    | SPADE
# slash       | 10                   | SPADE

# slash       | 5                    | CLUB
# fire attack | 6                    | HEART
# dodge       | 7                    | DIAMOND
# dodge       | 8                    | DIAMOND
assert_eq({
              'code': ret_code.OK,
              'action': 'UseCards',
              'card': {
                          0: { 'type': 'forbid' },
                          1: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [0, 1],
                             },
                          2: { 'type': 'forbid' },
                          3: {
                                 'type': 'fix target',
                                 'count': 1,
                                 'candidates': [0, 1],
                             },
                          8: { 'type': 'forbid' },
                          9: { 'type': 'forbid' },
                      },
              'players': [players[0].player_id],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'UseCards',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))

result = gc.player_act({
        'token': players[0].token,
        'action': 'give up',
    })

assert_eq({
              'code': ret_code.OK,
              'action': 'DiscardCards',
              'players': [players[0].player_id],
              'require': ['count', 'candidates'],
              'count': 2,
              'candidates': [0, 1, 2, 3, 8, 9],
          }, gc.hint(players[0].token))
assert_eq({
              'code': ret_code.OK,
              'action': 'DiscardCards',
              'players': [players[0].player_id],
          }, gc.hint(players[1].token))
