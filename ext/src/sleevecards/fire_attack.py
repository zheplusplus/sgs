import core.src.ret_code as ret_code
import core.src.action_frames as frames
import ext.src.damage as damage
import ext.src.common_checking as checking
from ext.src.hint_common import fix_target_action, target_filter

def fire_attack(game_control, args):
    targets_ids = args['targets']
    cards = game_control.cards_by_ids(args['use'])
    user = game_control.player_by_token(args['token'])
    checking.only_one_target(targets_ids)
    checking.only_one_card_named_as(cards, 'fire attack')
    target = game_control.player_by_id(targets_ids[0])
    checking.forbid_target_no_card_in_hand(target, game_control)

    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    on_result = lambda gc, a: discard_same_suit(gc, a, user, target, cards)
    game_control.push_frame(_TargetShowCards(game_control, target, on_result))
    return { 'code': ret_code.OK }

def fire_attack_target(game_control, user, card):
    def check_has_card(target):
        count_cards = game_control.player_cards_count_at(target, 'cards')
        if user == target:
            return 1 < count_cards
        return 0 < count_cards
    all_players = game_control.players_from_current()
    all_players = filter(check_has_card, all_players)
    return fix_target_action(target_filter('fire attack', user, all_players,
                                           card))

def discard_same_suit(game_control, args, player, target, cards):
    show_suit = game_control.cards_by_ids(args['show'])[0].suit
    game_control.push_frame(_SourceDiscardCards(
                              game_control, player, show_suit,
                              lambda gc, a: done(gc, a, player, target, cards)))

def done(game_control, args, source, target, fire_attack_cards):
    cards_ids = args['discard']
    if len(cards_ids) > 0:
        damage.Damage(source, target, 'fire attack', fire_attack_cards, 'fire',
                      1).operate(game_control)

class _TargetShowCards(frames.ShowCards):
    def __init__(self, game_control, target, on_result):
        frames.ShowCards.__init__(self, game_control, target, self._show_check,
                                  on_result)

    def _show_check(self, cids):
        if len(cids) != 1:
            raise ValueError('need exactly one card')
        checking.cards_region(self.game_control.cards_by_ids(cids), 'cards')

    def _hint(self, token):
        if token != self.player.token:
            return dict()
        cards = self.game_control.player_cards_at(self.player, 'cards')
        return {
                   'count': 1,
                   'candidates': map(lambda c: c.card_id, cards),
               }

    def _hint_action(self, token):
        return 'ShowCards'

class _SourceDiscardCards(frames.DiscardCards):
    def __init__(self, game_control, player, suit, on_result):
        frames.DiscardCards.__init__(self, game_control, player, self._check,
                                     on_result)
        self.suit = suit

    def _hint(self, token):
        if self.player.token != token:
            return dict()
        candidates = self.game_control.player_cards_at(self.player, 'cards')
        candidates = filter(lambda c: c.suit == self.suit, candidates)
        return {
                   'require': ['allow count', 'candidates'],
                   'allow count': [0, 1],
                   'candidates': map(lambda c: c.card_id, candidates),
               }

    def _check(self, cards_ids):
        if len(cards_ids) == 0:
            return
        cards = self.game_control.cards_by_ids(cards_ids)
        checking.only_one_card_of_suit(cards, self.suit)

    def _hint_action(self, token):
        return 'DiscardCards'
