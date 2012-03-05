import ext.src.common_checking as checking
from ext.src import hint_common

def add_to(player):
    player.responses['slash'].add_method('dragon heart', dodge_as_slash, hint_s)

def dodge_as_slash(cards):
    checking.only_one_card_named_as(cards, 'dodge')

def hint_s(game_control, player):
    return hint_common.one_card_filter(game_control, player, 'dragon heart',
                                       lambda c: c.name() == 'dodge')
