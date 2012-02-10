class ActionStack:
    def __init__(self):
        class DummyFrame:
            def resume(self):
                pass
        self.frames = [DummyFrame()]

    def push(self, frame):
        self.frames.append(frame)

    def call(self, args):
        return self.frames[-1].react(args)

    def pop(self):
        self.frames.pop()
        self.frames[-1].resume()

    def allowed_players(self):
        return self.frames[-1].allowed_players()

    def hint(self):
        return self.frames[-1].hint()
