import core.src.card as card

class CardInfo:
    name = ''
    rank = 0
    suit = 0

    def __init__(self, name, rank, suit):
        self.name = name
        self.rank = rank
        self.suit = suit

def generate(cards_info):
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
