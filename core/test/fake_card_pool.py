class CardPool:
    discarded = []
    cards = []
    current_cid = 0

    def __init__(self, cards):
        self.discarded = []
        self.cards = cards
        self.current_cid = 0

    def deal(self, cnt):
        if len(self.cards) < cnt:
            self.reshuffle()
        if len(self.cards) < cnt:
            cnt = len(self.cards)
        result = self.cards[:cnt]
        self.cards = self.cards[cnt:]
        return result

    def discard(self, cards_ids):
        # FIX: takes ids of cards
        #      returns cards
        pass

    def reshuffle(self):
        self.cards.extend(self.discarded)
