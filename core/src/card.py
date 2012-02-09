SUIT_NONE = 0
SPADE = 1
HEART = 2
CLUB = 3
DIAMOND = 4
BLACK = 1
RED = 2

NORMAL = 0
IN_USE = 1

class Card:
    def __init__(self, card_id, name, rank, suit):
        self.card_id = card_id
        self.base_name = name
        self.base_rank = rank
        self.base_suit = suit
        self.reset()

    def reset(self):
        self.owner_or_nil = None
        self.status = NORMAL
        self.region = 'cardpool'

    def name(self):
        if self.owner_or_nil == None:
            return self.base_name
        return self.owner_or_nil.card_name(self)

    def rank(self):
        return self.base_rank

    def suit(self):
        if self.owner_or_nil == None:
            return self.base_suit
        return self.owner_or_nil.card_suit(self)

    def set_owner(self, owner):
        self.owner_or_nil = owner

    def set_region(self, region):
        self.region = region

    def color(self):
        return BLACK if self.suit() == SPADE or self.suit() == CLUB else RED

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
