import core.src.action_frames as frames
import core.src.ret_code as ret_code
import ext.src.common_checking as checking
from ext.src.hint_common import fix_target_action, target_filter, range_filter

def steal_action(gc, args):
    cards = gc.cards_by_ids(args['use'])
    checking.only_one_card_named_as(cards, 'steal')
    return steal_check(gc, args)

def steal_check(gc, args):
    targets_ids = args['targets']
    user = gc.player_by_token(args['token'])
    cards = gc.cards_by_ids(args['use'])
    checking.only_one_target(targets_ids)
    target = gc.player_by_id(targets_ids[0])
    checking.valid_target(user, target, 'steal')
    checking.forbid_target_self(user, target)
    checking.forbid_target_no_card(target, gc)
    checking.within_range(gc, user, target, 'steal')

    gc.use_cards_for_players(user, targets_ids, args['action'], cards)
    hint = { 'regions': target.all_regions(gc) }
    gc.push_frame(
              frames.AcceptMessage(gc, [user], 'region', hint,
                                   lambda a: on_region(gc, user, target, a)))
    return { 'code': ret_code.OK }

def steal_target(gc, user):
    players = filter(lambda p: gc.player_has_cards(p), gc.succeeding_players())
    players = range_filter(gc, user, 'steal', players)
    return fix_target_action(target_filter('steal', user, players))

def on_region(gc, user, target, args):
    region = args['region']
    if region == 'onhand':
        cards = gc.random_pick_cards(target, 1)
        if len(cards) == 0:
            raise ValueError('bad region')
        gc.private_cards_transfer(target, user, cards)
    else:
        gc.public_cards_transfer(target, user,
                                 [target.unequip_check(gc, region)])
