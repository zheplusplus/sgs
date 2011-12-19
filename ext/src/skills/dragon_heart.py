import ext.src.common_checking as checking

def add_to(player):
    player.responses['slash'].add_method('dragon heart', dodge_as_slash)

def dodge_as_slash(cards):
    checking.only_one_card_named_as(cards, 'dodge')
