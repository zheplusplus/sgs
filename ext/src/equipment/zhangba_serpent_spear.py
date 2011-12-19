import core.src.card as card
import ext.src.common_checking as checking

EQUIP_NAME = 'zhangba serpent spear'

def equip_to(player, game_control, spear_card):
    player.equip(game_control, 'weapon', spear_card,
                 lambda: remove_from(game_control, player, spear_card))
    player.responses['slash'].add_method(EQUIP_NAME, two_cards)

def remove_from(game_control, player, equipped_card):
    player.responses['slash'].remove_method(EQUIP_NAME)
    game_control.discard_cards(player, [equipped_card])

def two_cards(cards):
    checking.cards_region(cards, 'cards')
    if len(cards) != 2:
        raise ValueError('wrong cards')
