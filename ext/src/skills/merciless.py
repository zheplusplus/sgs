import ext.src.wrappers as wrappers

def add_to(player):
    player.before_damaging_char = to_vigor_lost

@wrappers.alive
@wrappers.as_damage_source
def to_vigor_lost(player, damage, game_control):
    damage.clean(game_control)
    damage.interrupt(lambda: game_control.vigor_lost(damage.victim,
                                                     damage.point))
