import core.src.card as card
import ext.src.common_checking as checking

def add_to(player):
    player.responses['slash'].add_method('martial saint', red_as_slash)

def red_as_slash(cards):
    checking.only_one_card_of_color(cards, card.RED)
