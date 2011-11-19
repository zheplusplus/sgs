class CardPool:
    def __init__(self, cards):
        self.discarded = []
        self.cards = cards
        self.current_cid = 0
        self.id_to_card = { c.card_id: c for c in cards }

    def deal(self, player, cnt):
        if len(self.cards) < cnt:
            self.reshuffle()
        if len(self.cards) < cnt:
            cnt = len(self.cards)
        result = self.cards[:cnt]
        self.cards = self.cards[cnt:]
        [c.set_owner(player) for c in result]
        return result

    def discard(self, cards):
        self.discarded.extend(cards)
        [c.set_owner(None) for c in cards]

    def cards_by_ids(self, cards_ids):
        return map(lambda card_id: self.id_to_card[card_id], cards_ids)

    def reshuffle(self):
        self.cards.extend(self.discarded)
