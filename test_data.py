import core.src.card as card
from ext.src.card_pool import CardPool as ExtCardPool

class CardInfo:
    def __init__(self, name, rank, suit):
        self.name = name
        self.rank = rank
        self.suit = suit

def gen_cards(cards_info):
    class IdGen:
        i = 0

        def __init__(self):
            self.i = 0

        def next(self):
            r = self.i
            self.i += 1
            return r
    id_gen = IdGen()
    def card_gen(info):
        return card.Card(id_gen.next(), info.name, info.rank, info.suit)
    return map(card_gen, cards_info)

class CardPool(ExtCardPool):
    def __init__(self, cards):
        ExtCardPool.__init__(self, cards)

    def deal(self, player, cnt):
        self.check_player_recorded(player)
        result = self.cards[:cnt]
        self.cards = self.cards[cnt:]
        [c.set_owner(player) for c in result]
        [c.set_region('onhand') for c in result]
        self.player_id_to_owning_cards[player.player_id].extend(result)
        return result

    def random_pick_cards(self, player, count):
        cards = filter(lambda c: c.region == 'onhand',
                       self.player_id_to_owning_cards[player.player_id])
        return cards[:count]
