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
