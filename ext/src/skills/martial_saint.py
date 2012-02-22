import core.src.card as card
import ext.src.common_checking as checking
from ext.src import hint_common

def add_to(player):
    player.responses['slash'].add_method('martial saint', red_as_slash, hint)

def red_as_slash(cards):
    checking.only_one_card_of_color(cards, card.RED)

def hint(game_control, player):
    return hint_common.one_card_filter(game_control, player, 'martial saint',
                                       lambda c: c.color() == card.RED)
