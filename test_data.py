import core.src.card as card

class CardInfo:
    def __init__(self, name, rank, suit):
        self.name = name
        self.rank = rank
        self.suit = suit

def gen_cards(cards_info):
    class Id:
        i = 0

        def __init__(self):
            self.i = 0

        def next(self):
            r = self.i
            self.i += 1
            return r
    id_gen = Id()
    def card_gen(info):
        return card.Card(id_gen.next(), info.name, info.rank, info.suit)
    return map(card_gen, cards_info)

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
