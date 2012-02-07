import core.src.action_frames as frames
import core.src.ret_code as ret_code
import ext.src.damage as damage
import ext.src.common_checking as checking

def duel(game_control, args):
    targets_ids = args['targets']
    user = game_control.player_by_token(args['token'])
    cards = game_control.cards_by_ids(args['use'])
    checking.only_one_target(targets_ids)
    target = game_control.player_by_id(targets_ids[0])
    checking.forbid_target_self(user, target)
    checking.only_one_card_named_as(cards, 'duel')

    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    game_control.push_frame(play_slash_frame(game_control, target, user, cards))
    return { 'code': ret_code.OK }

def play_slash_frame(game_control, player, next_player, duel_cards):
    on_result = lambda gc, a: play_slash(gc, a, player, next_player, duel_cards)
    return player.response_frame('slash', game_control, on_result)

def play_slash(game_control, args, player, target, duel_cards):
    if args['method'] == 'give up':
        done(game_control, target, player, duel_cards)
    else:
        game_control.push_frame(play_slash_frame(game_control, target, player,
                                duel_cards))

def done(game_control, source, target, duel_cards):
    damage.Damage(source, target, 'duel', duel_cards, 'normal', 1
                  ).operate(game_control)
