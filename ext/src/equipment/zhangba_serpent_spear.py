import core.src.card as card
import ext.src.common_checking as checking
from equip_lib import change_slash_range
from ext.src.basiccards import slash

EQUIP_NAME = 'zhangba serpent spear'

def equip_to(player, game_control, spear_card):
    player.equip(game_control, spear_card, 'weapon', remove_from)
    player.responses['slash'].add_method(EQUIP_NAME, two_cards, response_hint)
    player.range_equip = change_slash_range(player.range_equip, 3)
    player.using_hint_equip.append(using_hint)

def remove_from(game_control, player, equipped_card):
    player.responses['slash'].remove_method(EQUIP_NAME)
    player.range_equip = lambda action: self.base_ranges[action]
    player.using_hint_equip.remove(using_hint)

def two_cards(cards):
    checking.cards_region(cards, 'onhand')
    if len(cards) != 2:
        raise ValueError('wrong cards')

def _cards_hint(gc, p):
    return {
        'require': ['fix card count'],
        'card count': 2,
        'cards': map(lambda c: c.card_id, gc.player_cards_at(p, 'onhand')),
    }

def _to_slash(gc, args):
    two_cards(gc.cards_by_ids(args['use']))
    return slash.slash(gc, args)

def using_hint(hint, game_control, user):
    if 'slash' in user.using_hint_dict:
        user.using_interfaces[EQUIP_NAME] = _to_slash
        targets = slash.slash_target(game_control, user, [])
        if targets['type'] == 'forbid':
            return
        cards_hint = _cards_hint(game_control, user)
        cards_hint['require'] = ['fix card count', 'fix target']
        cards_hint['targets'] = targets['targets']
        cards_hint['target count'] = targets['target count']
        hint['methods'][EQUIP_NAME] = cards_hint
    elif EQUIP_NAME in user.using_interfaces:
        del user.using_interfaces[EQUIP_NAME]

def response_hint(game_control, player):
    return { EQUIP_NAME: _cards_hint(game_control, player) }

def imported(equip_dict):
    equip_dict[EQUIP_NAME] = equip_to
