import core.src.action_frames as frames
import core.src.ret_code as ret_code
import ext.src.common_checking as checking
from ext.src.hint_common import fix_target_action, target_filter

def sabotage_action(gc, args):
    cards = gc.cards_by_ids(args['use'])
    checking.only_one_card_named_as(cards, 'sabotage')
    return sabotage_check(gc, args)

def sabotage_check(gc, args):
    targets_ids = args['targets']
    user = gc.player_by_token(args['token'])
    cards = gc.cards_by_ids(args['use'])
    checking.only_one_target(targets_ids)
    target = gc.player_by_id(targets_ids[0])
    checking.valid_target(user, target, 'sabotage')
    checking.forbid_target_self(user, target)
    checking.forbid_target_no_card(target, gc)

    gc.use_cards_for_players(user, targets_ids, args['action'], cards)
    hint = { 'regions': target.all_regions(gc) }
    gc.push_frame(frames.AcceptMessage(gc, [user], 'region', hint,
                                       lambda a: on_region(gc, target, a)))
    return { 'code': ret_code.OK }

def sabotage_targets(gc, user):
    targets = filter(lambda p: gc.player_has_cards(p), gc.succeeding_players())
    return target_filter('sabotage', user, targets)

def sabotage_targets_h(gc, user):
    return fix_target_action(sabotage_targets(gc, user))

def on_region(gc, target, args):
    region = args['region']
    if region == 'onhand':
        cards = gc.random_pick_cards(target, 1)
        if len(cards) == 0:
            raise ValueError('bad region')
        gc.discard_cards(target, cards)
    else:
        unequipped = target.unequip_check(gc, region)
        unequipped.set_region('unequipped')
        gc.recycle_cards([unequipped])
