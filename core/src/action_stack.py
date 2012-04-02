from action_frames import FrameBase

class ActionStack:
    def __init__(self):
        self.frames = [FrameBase(None)]

    def push(self, frame):
        self.frames.append(frame)
        frame.activated()

    def call(self, args):
        return self.frames[-1].react(args)

    def pop(self, result):
        stack_top = self.frames.pop()
        stack_top.destructed()
        self.frames[-1].resume(result)

    def event(self, action, **kwargs):
        for f in reversed(self.frames):
            f.event(action, **kwargs)

    def allowed_players(self):
        return self.frames[-1].allowed_players()

    def hint(self, token):
        return self.frames[-1].hint(token)
