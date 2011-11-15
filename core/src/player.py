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
        self.get_cards(game_control, STARTDEAL)

    def round(self, game_control):
        self.get_cards(game_control, ROUNDDEAL)
        self.discard_cards(game_control)

    def get_cards(self, game_control, cnt):
        cards = game_control.deal_cards(self, cnt)
        self.cards.extend(cards)

    def discard_cards(self, game_control):
        cards = self.cards[:2]
        self.cards = self.cards[len(cards):]
        game_control.discard_cards(self, cards)
