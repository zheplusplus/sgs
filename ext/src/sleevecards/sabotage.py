import core.src.action_frames as frames
import core.src.ret_code as ret_code

def sabotage(game_control, args):
    targets_ids = args['targets']
    if 1 != len(targets_ids):
        raise ValueError('wrong target')
    player = game_control.player_by_token(args['token'])
    target = game_control.player_by_id(targets_ids[0])
    as_target(player, target, game_control)
    cards = game_control.cards_by_ids(args['cards'])
    if 1 != len(cards) or 'sabotage' != cards[0].name:
        raise ValueError('wrong card')
    game_control.use_cards_for_players(player, targets_ids, args['action'], cards)
    targets = game_control.get_all_players()
    on_result = lambda gc, a: flawless_defense(game_control, player, targets, a)
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
