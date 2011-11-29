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
    targets = game_control.get_all_players()
    on_result = lambda gc, a: flawless_defense(game_control, user, targets, a)
    def play_filter(cards_ids):
        cards = game_control.cards_by_ids(cards_ids)
        if len(cards) == 0:
            return True
        return len(cards) == 1 and cards[0].name == 'flawless defense'
    game_control.push_frame(frames.PlayCards(game_control, target, play_filter, on_result))
    return { 'code': ret_code.OK }

def flawless_defense(game_control, player, target, args):
    cards_ids = args['play']
    if len(cards_ids) > 1:
        raise ValueError('wrong card')
    def play_filter(cards_ids):
        cards = game_control.cards_by_ids(args['cards'])
        if len(cards) == 0:
            return True
        return len(cards) == 1 and cards[0].name == 'flawless defense'
    if len(cards_ids) == 0:
        done(game_control, target, args)
    else:
        targets = game_control.get_all_players()
        game_control.push_frame(
            frames.PlayCards(game_control, player, player_filter,
                             lambda gc, a: flawless_defense(gc, player, targets, a)))

def done(game_control, target, args):
    if args.has_key('discard'):
        cards_ids = args['discard']
        game_control.discard_cards(game_control.player_by_token(args['token']), cards_ids)
