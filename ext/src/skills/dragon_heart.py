import ext.src.common_checking as checking
import ext.src.hint_common as hints
from ext.src.basiccards import slash
from ext.src.wrappers import invoke_on_success

SKILL = 'dragon heart'

def add_to(player):
    player.responses['slash'].add_method(SKILL, dodge_as_slash_check, hint_s)
    player.responses['dodge'].add_method(SKILL, slash_as_dodge, hint_d)
    player.using_hint_char.append(dodge_as_slash_using_hint)

def dodge_as_slash_check(cards):
    checking.cards_region(cards, 'onhand')
    checking.only_one_card_named_as(cards, 'dodge')

def dodge_as_slash_using_hint(hint, game_control, user, interfaces):
    @invoke_on_success(user, SKILL)
    def to_slash(gc, args):
        dodge_as_slash_check(gc.cards_by_ids(args['use']))
        args['action'] = 'slash'
        return slash.slash_check(gc, args)
    if 'slash' in interfaces:
        interfaces[SKILL] = to_slash
        cards = filter(lambda c: c.name() == 'dodge',
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

def slash_as_dodge(cards):
    checking.cards_region(cards, 'onhand')
    checking.only_one_card_named_as(cards, 'slash')

def hint_s(game_control, player):
    return hints.one_card_filter(game_control, player, SKILL,
                                 lambda c: c.name() == 'dodge')

def hint_d(game_control, player):
    return hints.one_card_filter(game_control, player, SKILL,
                                 lambda c: c.name() == 'slash')
