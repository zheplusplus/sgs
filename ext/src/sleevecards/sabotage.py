import core.src.action_frames as frames
import core.src.ret_code as ret_code
import ext.src.common_checking as checking

def sabotage(game_control, args):
    targets_ids = args['targets']
    user = game_control.player_by_token(args['token'])
    cards = game_control.cards_by_ids(args['cards'])
    checking.only_one_target(targets_ids)
    target = game_control.player_by_id(targets_ids[0])
    checking.only_one_card_named_as(cards, 'sabotage')
    checking.forbid_target_self(user, target)
    checking.forbid_target_no_card(target, game_control)

    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    on_result = lambda gc, a: None
    game_control.push_frame(
            frames.AcceptMessage(game_control, [user],
                                 lambda a: on_message(game_control, target, a),
                                 on_result))
    return { 'code': ret_code.OK }

def on_message(game_control, target, args):
    region = args['sabotage']
    if region == 'cards':
        cards = game_control.random_pick_cards(target, 1)
        if len(cards) == 0:
            raise ValueError('bad region')
        game_control.discard_cards(target, cards)
    else:
        game_control.recycle_cards([target.unequip_check(game_control, region)])
