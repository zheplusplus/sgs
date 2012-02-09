from core.src.damage import Damage as CoreDamage

def _zip_actions(f, players):
    return reduce(lambda actions, p: actions + f(p), players, [])

def _map_action(f, players):
    return map(lambda p: lambda d, gc: f(p)(p, d, gc), players)

class Damage(CoreDamage):
    def __init__(self, gc, source, target, action, cards, category, point):
        players = gc.players_from_current()
        CoreDamage.__init__(
                self, source, target, action, cards, category, point,
                _map_action(lambda p: p.before_damaging_char, players) +
                  _map_action(lambda p: p.before_damaging_equip, players) +
                  _map_action(lambda p: p.before_damaged_char, players) +
                  _map_action(lambda p: p.before_damaged_equip, players) +
                  _zip_actions(lambda p: p.computing_before_damaging, players) +
                  _zip_actions(lambda p: p.computing_before_damaged, players),
                _map_action(lambda p: p.after_damaging_char, players) +
                  _map_action(lambda p: p.after_damaging_equip, players) +
                  _map_action(lambda p: p.after_damaged_char, players) +
                  _map_action(lambda p: p.after_damaged_equip, players))
