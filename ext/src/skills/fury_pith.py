import ext.src.wrappers as wrappers

def add_to(player):
    @wrappers.alive
    @wrappers.as_damage_source
    def compute_distance(player, damage, game_control):
        damage.fury_pith_regain_vigor = game_control.distance_between(
                                            damage.source, damage.victim) <= 1
    player.after_damaging_char = regain_vigor
    player.add_computing_before_damaging(compute_distance)

@wrappers.alive
@wrappers.as_damage_source
def regain_vigor(player, damage, game_control):
    if damage.fury_pith_regain_vigor:
        game_control.vigor_regain(damage.source, damage.point)
