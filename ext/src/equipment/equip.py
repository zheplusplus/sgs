import core.src.ret_code as ret_code
import ext.src.common_checking as checking

equipment_dict = dict()

def is_equipment(card_name):
    return card_name in equipment_dict

def equip(player, game_control, card):
    if not card.name() in equipment_dict:
        raise ValueError('invalid equipment')
    equipment_dict[card.name()](player, game_control, card)

def interface(game_control, args):
    cards = game_control.cards_by_ids(args['use'])
    checking.cards_region(cards, 'cards')
    if len(cards) != 1:
        raise ValueError('wrong cards')
    player = game_control.player_by_token(args['token'])
    equip(player, game_control, cards[0])
    return { 'code': ret_code.OK }

def hint(cards):
    return map(lambda c: c.card_id,
               filter(lambda c: c.name() in equipment_dict, cards))

import zhangba_serpent_spear as serpent_spear
serpent_spear.imported(equipment_dict)
import horses
horses.imported(equipment_dict)
import rattan_armor
rattan_armor.imported(equipment_dict)
