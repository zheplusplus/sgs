import core.src.ret_code as ret_code
import core.src.action_frames as frames

def get_using_cards_interface_map():
    return { 'fire attack': fire_attack }

def fire_attack(game_control, args):
    targets_ids = args['targets']
    cards = args['cards']
    user = game_control.player_by_token(args['token'])
    if 1 != len(targets_ids):
        return {
                   'code': ret_code.BAD_REQUEST,
                   'reason': ret_code.WRONG_ARG,
               }
    if 1 != len(cards) and 'fire attack' != cards[0].name:
        return {
                   'code': ret_code.BAD_REQUEST,
                   'reason': ret_code.WRONG_ARG,
               }
    target = game_control.player_by_id(targets_ids[0])
    game_control.use_cards_for_player(user, targets_ids, args['action'], cards)
    on_result = lambda gc, a: fire_attack_discard_same_suit(gc, user, target, a)
    game_control.push_frame(frames.ShowCards(game_control, target,
                                             lambda c: len(c) == 1, on_result))
    return { 'code': ret_code.OK }

def fire_attack_discard_same_suit(game_control, player, target, args):
    show_suit = game_control.cards_by_ids(args['show'])[0].suit
    def discard_filter(cards_ids):
        cards = game_control.cards_by_ids(cards_ids)
        if len(cards) == 0:
            return True
        return len(cards) == 1 and cards[0].suit == show_suit
    game_control.push_frame(
            frames.DiscardCards(game_control, player, discard_filter,
                                lambda gc, a: fire_attack_done(gc, target, a)))

def fire_attack_done(game_control, target, args):
    cards_ids = args['discard']
    if len(cards_ids) > 0:
        game_control.discard_cards(game_control.player_by_token(args['token']),
                                   cards_ids)
        game_control.damage(target, 1, 'fire')
