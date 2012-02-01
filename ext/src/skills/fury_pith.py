def add_to(player):
    def compute_distance(damage, game_control):
        damage.fury_pith_regain_vigor = game_control.distance_between(
                                            damage.source, damage.victim) <= 1
    player.actions_after_damaging['character']['trigger'] = regain_vigor
    player.computing_before_damaging.append(compute_distance)

def regain_vigor(damage, game_control):
    if damage.fury_pith_regain_vigor:
        game_control.vigor_regain(damage.source, damage.point)
