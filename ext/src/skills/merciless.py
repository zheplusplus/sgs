import ext.src.wrappers as wrappers

def add_to(player):
    player.before_damaging_char = to_vigor_lost

@wrappers.alive
@wrappers.as_damage_source
def to_vigor_lost(player, damage, gc):
    damage.clean()
    damage.interrupt(lambda: gc.vigor_lost(damage.victim, damage.point))
