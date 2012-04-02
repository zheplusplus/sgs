class ActionFlow:
    class Interrupt(Exception):
        def __init__(self, after_interrupted):
            self.after_interrupted = after_interrupted

        def call(self):
            return self.after_interrupted()

    def __init__(self, game_control, actions):
        self.actions = actions
        self.game_control = game_control
        self.act_index = 0
        self.tail_actions = []
        self.cleaners = []

    def resume(self):
        try:
            while self.act_index < len(self.actions):
                act = self.actions[self.act_index]
                self.act_index += 1
                act(self, self.game_control)
            for act in reversed(self.tail_actions):
                act(self, self.game_control)
            self.clean()
        except ActionFlow.Interrupt, i:
            i.call()

    def interrupt(self, after_interrupt):
        raise ActionFlow.Interrupt(after_interrupt)

    def push_tail_action(self, action):
        self.tail_actions.append(action)
        return self

    def add_cleaner(self, cleaner):
        self.cleaners.append(cleaner)
        return self

    def clean(self):
        for c in self.cleaners:
            c(self, self.game_control)

def map_action(f, players):
    return map(lambda p: lambda s, gc: f(p)(p, s, gc), players)

def zip_actions(f, players):
    return reduce(lambda actions, p: actions + f(p), players, [])
