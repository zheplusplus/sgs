from card import Card

STARTDEAL = 4
ROUNDDEAL = 2

class Player:
    token = 0
    player_id = 0
    cards = []

    def __init__(self, token, pid):
        self.token = token
        self.player_id = pid
        self.cards = []

    def start(self, game_control):
        self.deal(game_control, STARTDEAL)

    def round(self, game_control):
        self.deal(game_control, ROUNDDEAL)
        self.discard(game_control)

    def deal(self, game_control, cnt):
        cards = game_control.deal_event(self, cnt)
        self.cards.extend(cards)

    def discard(self, game_control):
        cards = self.cards[:2]
        self.cards = self.cards[len(cards):]
        game_control.discard_event(self, cards)
