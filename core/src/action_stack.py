class ActionStack:
    def __init__(self):
        class DummyFrame:
            def resume(self, result):
                pass
        self.frames = [DummyFrame()]

    def push(self, frame):
        self.frames.append(frame)
        frame.activated()

    def call(self, args):
        return self.frames[-1].react(args)

    def pop(self, result):
        stack_top = self.frames.pop()
        stack_top.on_result(stack_top.game_control, result)
        self.frames[-1].resume(result)

    def allowed_players(self):
        return self.frames[-1].allowed_players()

    def hint(self, token):
        return self.frames[-1].hint(token)
