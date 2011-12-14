import core.src.ret_code as ret_code
import core.src.action_frames as frames
import ext.src.common_checking as checking

def fire_attack(game_control, args):
    targets_ids = args['targets']
    cards = game_control.cards_by_ids(args['cards'])
    user = game_control.player_by_token(args['token'])
    checking.only_one_target(targets_ids)
    checking.only_one_card_named_as(cards, 'fire attack')
    target = game_control.player_by_id(targets_ids[0])
    checking.forbid_target_no_card(target, game_control)

    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    on_result = lambda gc, a: discard_same_suit(gc, user, target, a)
    game_control.push_frame(frames.ShowCards(game_control, target,
                                             lambda c: len(c) == 1, on_result))
    return { 'code': ret_code.OK }

def discard_same_suit(game_control, player, target, args):
    show_suit = game_control.cards_by_ids(args['show'])[0].suit
    def discard_filter(cards_ids):
        cards = game_control.cards_by_ids(cards_ids)
        if len(cards) == 0:
            return True
        return len(cards) == 1 and cards[0].suit == show_suit
    game_control.push_frame(
            frames.DiscardCards(game_control, player, discard_filter,
                                lambda gc, a: done(gc, target, a)))

def done(game_control, target, args):
    cards_ids = args['discard']
    if len(cards_ids) > 0:
        game_control.discard_cards_by_ids(
                        game_control.player_by_token(args['token']), cards_ids)
        game_control.damage(target, 1, 'fire')
