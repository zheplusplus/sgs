import core.src.ret_code as ret_code
import core.src.action_frames as frames
import core.src.damage as damage
import ext.src.common_checking as checking

def fire_attack(game_control, args):
    targets_ids = args['targets']
    cards = game_control.cards_by_ids(args['cards'])
    user = game_control.player_by_token(args['token'])
    checking.only_one_target(targets_ids)
    checking.only_one_card_named_as(cards, 'fire attack')
    target = game_control.player_by_id(targets_ids[0])
    checking.forbid_target_no_card_in_hand(target, game_control)

    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    on_result = lambda gc, a: discard_same_suit(gc, a, user, target, cards)
    def show_check(cards_ids):
        if len(cards_ids) != 1:
            raise ValueError('need exactly one card')
        if game_control.cards_by_ids(cards_ids)[0].region != 'cards':
            raise ValueError('bad region')
    game_control.push_frame(frames.ShowCards(game_control, target, show_check,
                                             on_result))
    return { 'code': ret_code.OK }

def discard_same_suit(game_control, args, player, target, fire_attack_cards):
    show_suit = game_control.cards_by_ids(args['show'])[0].suit
    def discard_check(cards_ids):
        cards = game_control.cards_by_ids(cards_ids)
        if len(cards) == 0:
            return
        if len(cards) == 1 and cards[0].suit == show_suit:
            return
        raise ValueError('need exactly one card of same suit')
    game_control.push_frame(frames.DiscardCards(
                game_control, player, discard_check,
                lambda gc, a: done(gc, a, player, target, fire_attack_cards)))

def done(game_control, args, source, target, fire_attack_cards):
    cards_ids = args['discard']
    if len(cards_ids) > 0:
        damage.Damage(source, target, 'fire attack', fire_attack_cards, 'fire',
                      1, source.before_damaging_actions() +
                         target.before_damaged_actions(),
                      source.after_damaging_actions() +
                      target.after_damaged_actions()).operate(game_control)
