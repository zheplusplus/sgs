class CardPool:
    discarded = []
    cards = []
    current_cid = 0

    def __init__(self, cards):
        self.discarded = []
        self.cards = cards
        self.current_cid = 0

    def cardGen(self, name, suit, rank):
        return card.Card(self.idGen(), name, suit, rank)

    def idGen(self):
        cid = self.current_cid
        self.current_cid += 1
        return cid

    def deal(self, cnt):
        if len(self.cards) < cnt:
            self.reshuffle()
        if len(self.cards) < cnt:
            cnt = len(self.cards)
        result = self.cards[:cnt]
        self.cards = self.cards[cnt:]
        return result

    def discard(self, cards):
        self.discarded.extend(cards)

    def reshuffle(self):
        self.cards.extend(self.discarded)
