import core.src.action_frames as frames
import core.src.ret_code as ret_code
import ext.src.common_checking as checking
from ext.src.hint_common import fix_target_action, target_filter

def steal(game_control, args):
    targets_ids = args['targets']
    user = game_control.player_by_token(args['token'])
    cards = game_control.cards_by_ids(args['use'])
    checking.only_one_target(targets_ids)
    target = game_control.player_by_id(targets_ids[0])
    checking.only_one_card_named_as(cards, 'steal')
    checking.forbid_target_self(user, target)
    checking.forbid_target_no_card(target, game_control)
    checking.within_range(game_control, user, target, 'steal')

    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    on_result = lambda gc, a: None
    hint = { 'regions': target.all_regions() }
    game_control.push_frame(
      frames.AcceptMessage(game_control, [user], 'region', hint,
                           lambda a: on_message(game_control, user, target, a),
                           on_result))
    return { 'code': ret_code.OK }

def steal_target(gc, user, card):
    all_players = gc.succeeding_players()
    all_players = filter(lambda p: gc.player_has_cards(p), all_players)
    all_players = filter(lambda p: gc.distance_between(user, p) <=
                                                        user.ranges['steal'],
                         all_players)
    return fix_target_action(target_filter('steal', user, all_players, card))

def on_message(game_control, user, target, args):
    region = args['region']
    if region == 'cards':
        cards = game_control.random_pick_cards(target, 1)
        if len(cards) == 0:
            raise ValueError('bad region')
        game_control.private_cards_transfer(target, user, cards)
    else:
        game_control.public_cards_transfer(
                    target, user, [target.unequip_check(game_control, region)])
