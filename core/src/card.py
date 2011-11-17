SUIT_NONE = 0
SPADE = 1
HEART = 2
CLUB = 3
DIAMOND = 4

class Card:
    card_id = 0
    name = ''
    rank = 0
    suit = 0

    def __init__(self, card_id, name, rank, suit):
        self.card_id = card_id
        self.name = name
        self.rank = rank
        self.suit = suit
        self.owner_or_nil = None

    def set_owner(self, owner):
        self.owner_or_nil = owner
