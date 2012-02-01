class PlayersControl:
    def __init__(self):
        self.players = []
        self.current_pid = 0
        self.token_index = dict()

    def add_player(self, player):
        player.player_id = len(self.players)
        self.players.append(player)
        self.token_index[player.token] = player

    def current_player(self):
        p = self.players[self.current_pid]
        return p if p.alive else None

    def get_by_id(self, i):
        return self.players[i]

    def get_by_token(self, t):
        return self.token_index[t]

    def distance_between(self, source, target):
        return min(self._cw_basic_distance(source, target) -
                     source.cw_positive_dist_mod +
                     target.cw_passive_dist_mod,
                   self._ccw_basic_distance(source, target) -
                     source.ccw_positive_dist_mod +
                     target.ccw_passive_dist_mod)

    def _compute_basic_distance(self, source_id, target_id, id_incr):
        distance = 0
        while source_id != target_id:
            source_id = id_incr(source_id) % len(self.players)
            if self.get_by_id(source_id).alive:
                distance += 1
        return distance

    def _cw_basic_distance(self, source, target):
        return self._compute_basic_distance(source.player_id, target.player_id,
                                            lambda i: i - 1)

    def _ccw_basic_distance(self, source, target):
        return self._compute_basic_distance(source.player_id, target.player_id,
                                            lambda i: i + 1)

    def kill(self, player):
        player.alive = False
