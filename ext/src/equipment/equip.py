import core.src.ret_code as ret_code
import ext.src.common_checking as checking

equipment_dict = dict()

def is_equipment(card_name):
    return card_name in equipment_dict

def is_equipment_region(region):
    return region in ls_equipment_regions()

def ls_equipment_regions():
    return ['weapon', 'armor', '-1 horse', '+1 horse']

def equip(player, gc, card):
    if not card.name() in equipment_dict:
        raise ValueError('wrong cards')
    equipment_dict[card.name()](player, gc, card)

def interface(gc, args):
    cards = gc.cards_by_ids(args['use'])
    checking.cards_region(cards, 'onhand')
    player = gc.player_by_token(args['token'])
    equip(player, gc, cards[0])
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
import vermilion_feather_fan
vermilion_feather_fan.imported(equipment_dict)
