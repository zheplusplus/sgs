import core.src.ret_code as ret_code
import ext.src.common_checking as checking
from ext.src.hint_common import forbid, implicit_target

def peach_action(gc, args):
    cards = gc.cards_by_ids(args['use'])
    checking.only_one_card_named_as(cards, 'peach')
    return peach_check(gc, args)

def peach_check(game_control, args):
    user = game_control.player_by_token(args['token'])
    cards = game_control.cards_by_ids(args['use'])
    checking.target_damaged(user)

    game_control.use_cards_for_players(user, [user.player_id], 'peach', cards)
    game_control.vigor_regain(user, 1)
    return { 'code': ret_code.OK }

def peach_h(gc, user, c):
    if user.vigor == user.max_vigor:
        return forbid()
    return implicit_target()
