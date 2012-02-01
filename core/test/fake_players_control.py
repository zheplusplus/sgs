from core.src.players_control import PlayersControl as CorePlayersControl

class PlayersControl(CorePlayersControl):
    def __init__(self):
        CorePlayersControl.__init__(self)

    def next_player(self):
        self.current_pid = (self.current_pid + 1) % len(self.players)
