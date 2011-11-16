class PlayersControl:
    players = []
    current_pid = 0

    def __init__(self):
        self.players = []
        self.current_pid = 0

    def add_player(self, player):
        self.players.append(player)

    def next_player(self):
        self.current_pid = (self.current_pid + 1) % len(self.players)

    def current_player(self):
        return self.players[self.current_pid]
