import core.src.action_frames as frames
import core.src.ret_code as ret_code
import ext.src.common_checking as checking

def duel(game_control, args):
    targets_ids = args['targets']
    user = game_control.player_by_token(args['token'])
    cards = game_control.cards_by_ids(args['cards'])
    checking.only_one_target(targets_ids)
    target = game_control.player_by_id(targets_ids[0])
    checking.forbid_target_self(user, target)
    checking.only_one_card_named_as(cards, 'duel')

    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    game_control.push_frame(play_slash_frame(game_control, target, user))
    return { 'code': ret_code.OK }

def play_slash_frame(game_control, player, next_player):
    def check_slash(cards_ids):
        cards = game_control.cards_by_ids(cards_ids)
        if len(cards) == 0:
            return
        checking.only_one_card_named_as(cards, 'slash')
    on_result = lambda gc, a: play_slash(gc, player, next_player, a)
    return frames.PlayCards(game_control, player, check_slash, on_result)

def play_slash(game_control, player, target, args):
    if len(args['play']) == 0:
        done(game_control, player, args)
    else:
        game_control.push_frame(play_slash_frame(game_control, target, player))

def done(game_control, target, args):
    game_control.damage(target, 1, 'normal')
