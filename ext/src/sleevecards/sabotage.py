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
    on_result = lambda gc, a: done(gc, target, a)
    allowed_messages = { 'cards' }
    game_control.push_frame(frames.AcceptMessage(game_control, [user],
                                                 'sabotage', allowed_messages,
                                                 on_result))
    return { 'code': ret_code.OK }

def done(game_control, target, args):
    if args['sabotage'] == 'cards':
        game_control.discard_cards(target,
                                   game_control.random_pick_cards(target, 1))
