class ActionStack:
    def __init__(self):
        self.frames = []

    def push(self, frame):
        self.frames.append(frame)

    def call(self, args):
        return self.frames[-1].react(args)

    def pop(self):
        self.frames.pop()
