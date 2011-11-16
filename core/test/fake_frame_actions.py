import core.src.ret_code
import core.src.action_frames as frames

def get_using_cards_interface_map():
    return {
               'fire attack': fire_attack,
               'duel': duel,
           }

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
    game_control.push_frame(frames.ShowCard(game_control, targets[0]))

def fire_attack_discard_same_suit(game_control, args):
    # FIX: the arguments map may not be like this
    game_control.push_frame(
        frames.DiscardCards(game_control, args['user'].token,
                            lambda c: len(c) == 1 and args['suit'] == c[0].suit,
                            True, fire_attack_done))

def fire_attack_done(game_control, args):
    # FIX: the arguments map may not be like this
    if len(args['cards']) > 0:
        game_control.discard_cards(args['user'], args['cards'])
        game_control.damage(args['target'], 1, 'fire')

def duel(game_control, args):
    pass
