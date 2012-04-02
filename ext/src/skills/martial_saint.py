import core.src.card as card
import ext.src.common_checking as checking
import ext.src.hint_common as hints
from ext.src.basiccards import slash
from ext.src.wrappers import invoke_on_success
from ext.src.equipment.equip import ls_equipment_regions
from ext.src.equipment.equip_lib import EquipmentRestore

SKILL = 'martial saint'

def add_to(player):
    player.responses['slash'].add_method(SKILL, red_as_slash_response, hint_r)
    player.using_hint_char.append(red_as_slash_using_hint)

def red_as_slash_response(cards):
    checking.only_one_card_of_color(cards, card.RED)

def red_as_slash_using_hint(hint, gc, user, interfaces):
    if 'slash' in interfaces:
        _add_multi_regions(gc, user, interfaces, hint)
    else:
        _rm_regions(gc, user, interfaces, hint)

def _add_region(gc, user, region, interfaces, hint):
    @invoke_on_success(user, SKILL)
    def to_slash(gc, args):
        cards = gc.cards_by_ids(args['use'])
        checking.cards_region(cards, region)
        red_as_slash_response(cards)
        args['action'] = 'slash'
        with EquipmentRestore(user, region):
            return slash.slash_check(gc, args)
    interfaces[SKILL + ':' + region] = to_slash
    cards = filter(lambda c: c.color() == card.RED,
                   gc.player_cards_at(user, region))
    targets = slash.slash_targets(gc, user)
    if len(targets) == 0 or len(cards) == 0:
        return
    hints.add_method_to(hint, SKILL + ':' + region,
                        hints.join_req(hints.fixed_card_count(cards, 1),
                                       hints.fixed_target_count(targets, 1)))

def _add_multi_regions(gc, user, interfaces, hint):
    _add_region(gc, user, 'onhand', interfaces, hint)
    for r in ls_equipment_regions():
        if r in user.equipment:
            user.equipment[r].off()
            _add_region(gc, user, r, interfaces, hint)
            user.equipment[r].on()

def _rm_regions(gc, user, interfaces, hint):
    for e in ls_equipment_regions() + ['onhand']:
        if SKILL + ':' + e in interfaces:
            del interfaces[SKILL + ':' + e]

def hint_r(gc, player):
    return hints.one_card_filter(gc, player, SKILL,
                                 lambda c: c.color() == card.RED)
