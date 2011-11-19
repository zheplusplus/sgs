class PlayersControl:
    def __init__(self):
        self.players = []
        self.current_pid = 0
        self.token_index = {}
        self.id_index = {}

    def add_player(self, player):
        self.players.append(player)
        self.token_index[player.token] = player
        self.id_index[player.player_id] = player

    def next_player(self):
        self.current_pid = (self.current_pid + 1) % len(self.players)

    def current_player(self):
        return self.players[self.current_pid]

    def get_by_id(self, i):
        return self.id_index[i]

    def get_by_token(self, t):
        return self.token_index[t]
