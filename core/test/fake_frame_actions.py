import core.src.ret_code
import core.src.action_frames as frames

def get_using_cards_interface_map():
    return { 'fire attack': fire_attack }

def fire_attack(game_control, player, args):
    targets = args['targets']
    cards = args['cards']
    if 1 != len(targets):
        return {
                   'code': ret_code.BAD_REQUEST,
                   'reason': ret_code.WRONG_ARG,
               }
    if 1 != len(cards) and 'fire attack' != cards[0].name:
        return {
                   'code': ret_code.BAD_REQUEST,
                   'reason': ret_code.WRONG_ARG,
               }
    # FIX: there should have been other checks
    game_control.cards_used(user_token, targets, args['action'], cards)
    game_control.push_frame(frames.ShowCard(game_control, targets[0]),
                            fire_attack_discard_same_suit)
    return { 'code': ret_code.OK }

def fire_attack_discard_same_suit(game_control, args):
    def discard_filter(suit, cards):
        if len(cards) == 0:
            return True
        return len(cards) == 1 and suit == cards[0].suit
    # FIX: the arguments map may not be like this
    game_control.push_frame(
        frames.DiscardCards(game_control, args['user'].token,
                            lambda c: discard_filter(c.suit, args['cards']),
                            fire_attack_done))

def fire_attack_done(game_control, args):
    # FIX: the arguments map may not be like this
    if len(args['cards']) > 0:
        game_control.discard_cards(args['user'], args['cards'])
        game_control.damage(args['target'], 1, 'fire')
