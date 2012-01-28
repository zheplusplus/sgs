def add_to(player):
    player.actions_after_damaging['character']['trigger'] = regain_vigor

def regain_vigor(damage, game_control):
    if game_control.distance_between(damage.source, damage.victim) <= 1:
        game_control.vigor_regain(damage.source, damage.point)
