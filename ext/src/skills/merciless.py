def add_to(player):
    player.actions_before_damaging['character']['trigger'] = to_vigor_lost

def to_vigor_lost(damage, game_control):
    damage.interrupt(lambda:
            game_control.vigor_lost(damage.victim, damage.point))
