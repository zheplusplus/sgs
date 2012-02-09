from core.src import card

def add_to(player):
    def youth_beauty(f):
        return lambda c: card.HEART if c.base_suit == card.SPADE else f(c)
    player.card_suit_char = youth_beauty(player.card_suit_char)
