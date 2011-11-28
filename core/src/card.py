SUIT_NONE = 0
SPADE = 1
HEART = 2
CLUB = 3
DIAMOND = 4

NORMAL = 0
IN_USE = 1

class Card:
    def __init__(self, card_id, name, rank, suit):
        self.card_id = card_id
        self.name = name
        self.rank = rank
        self.suit = suit
        self.owner_or_nil = None
        self.status = NORMAL

    def set_owner(self, owner):
        self.owner_or_nil = owner

    def using(self):
        self.status = IN_USE

    def used(self):
        self.status = NORMAL

    def free(self):
        return self.status != IN_USE
