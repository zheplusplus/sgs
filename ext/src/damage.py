import core.src.action_flow as flow

class Damage(flow.ActionFlow):
    def __init__(self, gc, source, target, action, cards, category, point):
        players = gc.players_from_current()
        flow.ActionFlow.__init__(
            self, gc,
            flow.map_action(lambda p: p.before_damaging_char, players) +
              flow.map_action(lambda p: p.before_damaging_equip, players) +
              flow.map_action(lambda p: p.before_damaged_char, players) +
              flow.map_action(lambda p: p.before_damaged_equip, players) +
              flow.zip_actions(lambda p: p.computing_before_damaging, players) +
              flow.zip_actions(lambda p: p.computing_before_damaged, players) +
              [lambda d, gc: gc.damage(self)] +
              flow.map_action(lambda p: p.after_damaging_char, players) +
              flow.map_action(lambda p: p.after_damaging_equip, players) +
              flow.map_action(lambda p: p.after_damaged_char, players) +
              flow.map_action(lambda p: p.after_damaged_equip, players))
        self.source = source
        self.victim = target
        self.action = action
        self.cards = cards
        self.category = category
        self.point = point
