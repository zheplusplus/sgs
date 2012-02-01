from core.src.players_control import PlayersControl as CorePlayersControl
from core.src.action_frames import FrameBase

class _RescueFrame(FrameBase):
    def __init__(self, game_control, who, players, after_rescuing):
        FrameBase.__init__(self, game_control, lambda gc, r: after_rescuing())
        self.who = who
        self.players = players
        self.player_index = 0

    def allowed_players(self):
        return [self._current()]

    def _next(self):
        self.player_index += 1
        if self.player_index == len(self.players):
            self.game_control.kill(self.who)
            self.done(None)

    def _current(self):
        return self.players[self.player_index]

    def _push_player_frame(self):
        self.game_control.push_frame(self._current().response_frame(
                                  'peach', self.game_control, self._on_result))

    def _check_rescued(self):
        if 0 < self.who.vigor:
            self.done(None)
        else:
            self._push_player_frame()

    def _on_result(self, game_control, args):
        if args['method'] != 'give up':
            game_control.vigor_regain(self.who, 1)
            self._check_rescued()
        else:
            self._next()

    def react(self, args):
        self._push_player_frame()
        return self.game_control.player_act(args)

class PlayersControl(CorePlayersControl):
    def __init__(self):
        CorePlayersControl.__init__(self)

    def next_player(self):
        self.current_pid = (self.current_pid + 1) % len(self.players)
        if None == self.current_player():
            self.next_player()

    def players_from_current(self):
        current = self.current_player()
        if None == current:
            return self.succeeding_players()
        return [current] + self.succeeding_players()

    def succeeding_players(self):
        return filter(lambda p: p.alive, self.players[self.current_pid + 1:] +
                                         self.players[:self.current_pid])

    def try_rescuing(self, game_control, player, after_brink_of_death):
        game_control.push_frame(_RescueFrame(game_control, player,
                                             self.players_from_current(),
                                             after_brink_of_death))
