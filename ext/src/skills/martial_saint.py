import core.src.card as card
import ext.src.common_checking as checking
import ext.src.hint_common as hints
from ext.src.basiccards import slash
from ext.src.wrappers import invoke_on_success

SKILL = 'martial saint'

def add_to(player):
    player.responses['slash'].add_method(SKILL, red_as_slash_response, hint_r)
    player.using_hint_char.append(red_as_slash_using_hint)

def red_as_slash_response(cards):
    checking.only_one_card_of_color(cards, card.RED)

def red_as_slash_using_hint(hint, game_control, user, interfaces):
    @invoke_on_success(user, SKILL)
    def to_slash(gc, args):
        checking.cards_region(cards, 'onhand')
        red_as_slash_response(gc.cards_by_ids(args['use']))
        args['action'] = 'slash'
        return slash.slash_check(gc, args)
    if 'slash' in interfaces:
        interfaces[SKILL] = to_slash
        cards = filter(lambda c: c.color() == card.RED,
                       game_control.player_cards_at(user, 'onhand'))
        targets = slash.slash_targets(game_control, user)
        if len(targets) == 0:
            return
        hints.add_method_to(
                hint, SKILL,
                hints.join_req(hints.fixed_card_count(cards, 1),
                               hints.fixed_target_count(targets, 1)))
    elif SKILL in interfaces:
        del interfaces[SKILL]

def hint_r(game_control, player):
    return hints.one_card_filter(game_control, player, SKILL,
                                 lambda c: c.color() == card.RED)
