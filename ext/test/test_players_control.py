from ext.src.players_control import PlayersControl
from ext.src.player import Player

from test_common import *

pc = PlayersControl()
players = [Player(i, 1) for i in range(10000, 10008)]
for p in players: pc.add_player(p)

assert_eq(players[0], pc.current_player())
assert_eq([players[i] for i in range(1, 8)], pc.succeeding_players())

pc.next_player()
assert_eq(players[1], pc.current_player())
assert_eq([players[i] for i in range(2, 8)] + [players[0]],
          pc.succeeding_players())

players[3].alive = False
assert_eq(players[1], pc.current_player())
assert_eq([players[2]] + [players[i] for i in range(4, 8)] + [players[0]],
          pc.succeeding_players())

pc.next_player()
assert_eq(players[2], pc.current_player())
assert_eq([players[i] for i in range(4, 8)] + [players[0], players[1]],
          pc.succeeding_players())

pc.next_player()
assert_eq(players[4], pc.current_player())
assert_eq([players[i] for i in range(5, 8)] + [players[i] for i in range(0, 3)],
          pc.succeeding_players())

players[4].alive = False
assert_eq([players[i] for i in range(5, 8)] + [players[i] for i in range(0, 3)],
          pc.succeeding_players())
assert_eq(pc.succeeding_players(), pc.players_from_current())
