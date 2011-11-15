class Player:
    token = 0
    player_id = 0
    cards = []

    def __init__(self, token, pid):
        self.token = token
        self.player_id = pid
        self.cards = []

    def start(self, game_control):
        pass

    def round(self, game_control):
        self.getting_cards_stage(game_control)
        self.using_cards_stage(game_control)
        self.discarding_cards_stage(game_control)

    def getting_cards_stage(self, game_control):
        pass

    def using_cards_stage(self, game_control):
        pass

    def discarding_cards_stage(self, game_control):
        pass
