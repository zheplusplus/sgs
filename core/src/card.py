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
        self.region = 'cardpool'

    def set_owner(self, owner):
        self.owner_or_nil = owner

    def set_region(self, region):
        self.region = region

    def using(self):
        self.status = IN_USE

    def restore(self):
        self.status = NORMAL

    def available(self):
        return self.status != IN_USE

class StatusRestore:
    def __init__(self, cards):
        self.cards = cards

    def __exit__(self, etype, eobj, tb):
        [c.restore() for c in self.cards]
        return False

class InUseStatusRestore(StatusRestore):
    def __init__(self, cards):
        StatusRestore.__init__(self, cards)

    def __enter__(self):
        [c.using() for c in self.cards]
