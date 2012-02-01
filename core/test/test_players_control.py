import core.src.players_control as players_control

from test_common import *
import fake_player

pc = players_control.PlayersControl()
players = [fake_player.Player(token) for token in range(10000, 10008)]
for p in players: pc.add_player(p)

for d in range(0, 4):
    for i in range(0, 8):
        assert_eq(d, pc.distance_between(players[i], players[(i + d) % 8]))

for d in range(4, 8):
    for i in range(0, 8):
        assert_eq(8 - d, pc.distance_between(players[i], players[(i + d) % 8]))

assert_eq(players[0], pc.current_player())

players[0].alive = False
assert_eq(None, pc.current_player())

assert_eq(0, pc.distance_between(players[1], players[1]))
assert_eq(1, pc.distance_between(players[1], players[7]))
assert_eq(1, pc.distance_between(players[7], players[1]))
assert_eq(2, pc.distance_between(players[2], players[7]))
assert_eq(2, pc.distance_between(players[7], players[2]))

players[2].alive = False
assert_eq(2, pc.distance_between(players[7], players[3]))
assert_eq(1, pc.distance_between(players[7], players[1]))
assert_eq(2, pc.distance_between(players[3], players[7]))
assert_eq(1, pc.distance_between(players[1], players[7]))
