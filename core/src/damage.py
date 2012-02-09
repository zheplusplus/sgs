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
        self.affix = []
        self.act_index = 0
        self.cleaners = []

    def add_affix(self, affix):
        self.affix.append(affix)
        return self

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
            self.upon_damage(game_control)
        except _DamageInterrupted, i:
            i.after_interrupted()

    def upon_damage(self, game_control):
        try:
            self.act_index = 0
            self.resume = lambda: self.after_damage(game_control)
            game_control.damage(self)
            self.resume()
        except _DamageInterrupted, i:
            i.after_interrupted()

    def after_damage(self, game_control):
        try:
            while self.act_index < len(self.after_damage_actions):
                act = self.after_damage_actions[self.act_index]
                self.act_index += 1
                act(self, game_control)
            self.resume = lambda: self.start_affix(game_control)
            self.resume()
        except _DamageInterrupted, i:
            i.after_interrupted()

    def start_affix(self, game_control):
        while 0 < len(self.affix):
            act = self.affix[-1]
            self.affix.pop()
            act(self, game_control)
        self.clean(game_control)

    def add_cleaner(self, c):
        self.cleaners.append(c)
        return self

    def clean(self, game_control):
        for c in self.cleaners:
            c(self, game_control)
