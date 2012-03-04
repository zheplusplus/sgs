from core.src import card

def add_to(player):
    def spade_to_heart(suit):
        if suit == card.SPADE:
            return card.HEART
        return suit
    player.triggers['card:suit'] = spade_to_heart
