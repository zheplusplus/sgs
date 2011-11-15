import core.src.card as card

class CardPool:
    discarded = []
    cards = []
    current_cid = 0

    def __init__(self):
        self.discarded = []
        self.cards = []
        self.current_cid = 0

        self.cards = [
            self.cardGen('slash', 1, card.SPADE),
            self.cardGen('slash', 2, card.SPADE),
            self.cardGen('slash', 3, card.SPADE),
            self.cardGen('slash', 4, card.SPADE),
            self.cardGen('slash', 5, card.SPADE),
            self.cardGen('slash', 6, card.SPADE),
            self.cardGen('slash', 7, card.SPADE),
            self.cardGen('slash', 8, card.SPADE),
            self.cardGen('slash', 9, card.SPADE),
            self.cardGen('slash', 10, card.SPADE),
            self.cardGen('slash', 11, card.SPADE),
            self.cardGen('slash', 12, card.SPADE),
            self.cardGen('slash', 13, card.SPADE),
            self.cardGen('dodge', 1, card.HEART),
            self.cardGen('dodge', 2, card.HEART),
            self.cardGen('dodge', 3, card.HEART),
            self.cardGen('dodge', 4, card.HEART),
            self.cardGen('dodge', 5, card.HEART),
            self.cardGen('dodge', 6, card.HEART),
            self.cardGen('dodge', 7, card.HEART),
            self.cardGen('dodge', 8, card.HEART),
            self.cardGen('peach', 9, card.HEART),
            self.cardGen('peach', 10, card.HEART),
            self.cardGen('peach', 11, card.HEART),
            self.cardGen('peach', 12, card.HEART),
            self.cardGen('dodge', 13, card.HEART),
            self.cardGen('slash', 1, card.CLUB),
            self.cardGen('slash', 2, card.CLUB),
            self.cardGen('slash', 3, card.CLUB),
            self.cardGen('slash', 4, card.CLUB),
            self.cardGen('slash', 5, card.CLUB),
            self.cardGen('slash', 6, card.CLUB),
            self.cardGen('slash', 7, card.CLUB),
            self.cardGen('slash', 8, card.CLUB),
            self.cardGen('slash', 9, card.CLUB),
            self.cardGen('slash', 10, card.CLUB),
            self.cardGen('slash', 11, card.CLUB),
            self.cardGen('slash', 12, card.CLUB),
            self.cardGen('slash', 13, card.CLUB),
            self.cardGen('dodge', 1, card.DIAMOND),
            self.cardGen('dodge', 2, card.DIAMOND),
            self.cardGen('dodge', 3, card.DIAMOND),
            self.cardGen('dodge', 4, card.DIAMOND),
            self.cardGen('dodge', 5, card.DIAMOND),
            self.cardGen('dodge', 6, card.DIAMOND),
            self.cardGen('dodge', 7, card.DIAMOND),
            self.cardGen('dodge', 8, card.DIAMOND),
            self.cardGen('dodge', 9, card.DIAMOND),
            self.cardGen('dodge', 10, card.DIAMOND),
            self.cardGen('dodge', 11, card.DIAMOND),
            self.cardGen('dodge', 12, card.DIAMOND),
            self.cardGen('dodge', 13, card.DIAMOND),
        ]

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
