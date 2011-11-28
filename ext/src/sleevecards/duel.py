import core.src.action_frames as frames
import core.src.ret_code as ret_code

def as_target(source, target, game_control):
    forbid_target_self(source, target)
    pass

def duel(game_control, args):
    targets_ids = args['targets']
    if 1 != len(targets_ids):
        return {
                   'code': ret_code.BAD_REQUEST,
                   'reason': ret_code.BR_WRONG_ARG,
               }
    player = game_control.player_by_token(args['token'])
    if targets_ids[0] == player.player_id:
        raise ValueError('wrong player')
    cards = game_control.cards_by_ids(args['cards'])
    if 1 != len(cards) or 'duel' != cards[0].name:
        raise ValueError('wrong card')
    user = game_control.player_by_token(args['token'])
    target = game_control.player_by_id(targets_ids[0])
    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    on_result = lambda gc, a: play_slash(game_control, user, target, a)
    def play_filter(cards_ids):
        cards = game_control.cards_by_ids(cards_ids)
        if len(cards) == 0:
            return True
        return len(cards) == 1 and cards[0].name == 'slash'
    game_control.push_frame(
            frames.PlayCards(game_control, target,
                             play_filter,
                             on_result))
    return { 'code': ret_code.OK }

def play_slash(game_control, player, target, args):
    cards_ids = args['play']
    if len(cards_ids) > 1:
        raise ValueError('wrong card')
    def play_filter(cards_ids):
        cards = game_control.cards_by_ids(cards_ids)
        if len(cards) == 0:
            return True
        return len(cards) == 1 and cards[0].name == 'slash'
    if len(cards_ids) == 0:
        done(game_control, target, args)
    else:
        game_control.push_frame(
              frames.PlayCards(game_control, player, play_filter,
                               lambda gc, a: play_slash(gc, target, player, a)))

def done(game_control, target, args):
    game_control.damage(target, 1, 'normal')
