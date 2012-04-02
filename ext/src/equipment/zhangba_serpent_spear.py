import core.src.card as card
import ext.src.common_checking as checking
import ext.src.hint_common as hints
from equip_lib import change_slash_range
from ext.src.basiccards import slash
from ext.src.wrappers import invoke_on_success

EQUIP_NAME = 'zhangba serpent spear'

def equip_to(player, game_control, spear_card):
    player.equip(game_control, spear_card, 'weapon', remove_from)
    player.responses['slash'].add_method(EQUIP_NAME, two_cards, response_hint)
    player.range_equip = change_slash_range(player.range_equip, 3)
    player.using_hint_equip.append(using_hint)

def remove_from(game_control, player, equipped_card):
    player.responses['slash'].remove_method(EQUIP_NAME)
    player.range_equip = lambda action: player.base_ranges[action]
    player.using_hint_equip.remove(using_hint)

def two_cards(cards):
    checking.cards_region(cards, 'onhand')
    if len(cards) != 2:
        raise ValueError('wrong cards')

def _cards_hint(gc, p):
    return hints.fixed_card_count(gc.player_cards_at(p, 'onhand'), 2)

def using_hint(hint, game_control, user, interfaces):
    @invoke_on_success(user, EQUIP_NAME)
    def to_slash(gc, args):
        two_cards(gc.cards_by_ids(args['use']))
        args['action'] = 'slash'
        return slash.slash_check(gc, args)
    if 'slash' in interfaces:
        interfaces[EQUIP_NAME] = to_slash
        cards = game_control.player_cards_at(user, 'onhand')
        targets = slash.slash_targets(game_control, user)
        if len(targets) == 0:
            return
        hints.add_method_to(
                hint, EQUIP_NAME,
                hints.join_req(hints.fixed_card_count(cards, 2),
                               hints.fixed_target_count(targets, 1)))
    elif EQUIP_NAME in interfaces:
        del interfaces[EQUIP_NAME]

def response_hint(game_control, player):
    return { EQUIP_NAME: _cards_hint(game_control, player) }

def imported(equip_dict):
    equip_dict[EQUIP_NAME] = equip_to
