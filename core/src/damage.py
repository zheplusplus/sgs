class _DamageInterrupted(Exception):
    def __init__(self, after_interrupted):
        self.after_interrupted = after_interrupted

class Damage:
    def __init__(self, source, victim, action, cards, category, point,
                 before_damage_actions, after_damage_actions):
        self.source = source
        self.victim = victim
        self.action = action
        self.cards = cards
        self.category = category
        self.point = point
        self.before_damage_actions = before_damage_actions
        self.after_damage_actions = after_damage_actions
        self.act_index = 0

    def operate(self, game_control):
        self.resume = lambda: self.before_damage(game_control)
        self.resume()

    def interrupt(self, after_interrupted):
        raise _DamageInterrupted(after_interrupted)

    def before_damage(self, game_control):
        try:
            while self.act_index < len(self.before_damage_actions):
                act = self.before_damage_actions[self.act_index]
                self.act_index += 1
                act(self, game_control)
            game_control.damage(self.victim, self.point, self.category)
            self.act_index = 0
            self.resume = lambda: self.after_damage(game_control)
            self.resume()
        except _DamageInterrupted, c:
            c.after_interrupted()

    def after_damage(self, game_control):
        try:
            while self.act_index < len(self.after_damage_actions):
                act = self.after_damage_actions[self.act_index]
                self.act_index += 1
                act(self, game_control)
        except _DamageInterrupted, c:
            c.after_interrupted()
