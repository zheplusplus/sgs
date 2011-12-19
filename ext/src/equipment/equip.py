import core.src.ret_code as ret_code
import ext.src.common_checking as checking
import zhangba_serpent_spear as serpent_spear

EQUIPMENT_DICT = {
                     serpent_spear.EQUIP_NAME: serpent_spear.equip_to,
                 }

def equip(player, game_control, card):
    if not card.name in EQUIPMENT_DICT:
        raise ValueError('invalid equipment')
    EQUIPMENT_DICT[card.name](player, game_control, card)

def interface(game_control, args):
    cards = game_control.cards_by_ids(args['cards'])
    checking.cards_region(cards, 'cards')
    if len(cards) != 1:
        raise ValueError('wrong cards')
    player = game_control.player_by_token(args['token'])
    equip(player, game_control, cards[0])
    return { 'code': ret_code.OK }
