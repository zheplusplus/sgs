import core.src.card as card
import ext.src.common_checking as checking

EQUIP_NAME = 'zhangba serpent spear'

def equip_to(player, game_control, spear_card):
    player.equip(game_control, spear_card, 'weapon', remove_from)
    player.responses['slash'].add_method(EQUIP_NAME, two_cards, hint)

def remove_from(game_control, player, equipped_card):
    player.responses['slash'].remove_method(EQUIP_NAME)

def two_cards(cards):
    checking.cards_region(cards, 'cards')
    if len(cards) != 2:
        raise ValueError('wrong cards')

def hint(game_control, player):
    cards = game_control.player_cards_at(player, 'cards')
    return {
               EQUIP_NAME: {
                   'require': ['count', 'candidates'],
                   'count': 2,
                   'candidates': map(lambda c: c.card_id, cards),
               }
           }

def imported(equip_dict):
    equip_dict[EQUIP_NAME] = equip_to
