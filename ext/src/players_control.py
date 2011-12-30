class PlayersControl:
    def __init__(self):
        self.players = []
        self.current_pid = 0
        self.token_index = dict()
        self.id_index = dict()

    def add_player(self, player):
        player.player_id = len(self.players)
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

    def distance_between(self, source, target):
        return min(self._cw_basic_distance(source, target) -
                     source.cw_positive_dist_mod +
                     target.cw_passive_dist_mod,
                   self._ccw_basic_distance(source, target) -
                     source.ccw_positive_dist_mod +
                     target.ccw_passive_dist_mod)

    def _cw_basic_distance(self, source, target):
        return ((source.player_id - target.player_id + len(self.players)) %
                                                        len(self.players))

    def _ccw_basic_distance(self, source, target):
        return ((target.player_id - source.player_id + len(self.players)) %
                                                        len(self.players))
