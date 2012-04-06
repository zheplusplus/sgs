import core.src.ret_code as ret_code
import core.src.action_frames as frames
import ext.src.damage as damage
import ext.src.common_checking as checking
from ext.src.hint_common import fix_target_action, target_filter

def arson_attack_action(gc, args):
    cards = gc.cards_by_ids(args['use'])
    checking.only_one_card_named_as(cards, 'arson attack')
    return arson_attack_check(gc, args)

def arson_attack_check(game_control, args):
    targets_ids = args['targets']
    cards = game_control.cards_by_ids(args['use'])
    user = game_control.player_by_token(args['token'])
    checking.only_one_target(targets_ids)
    target = game_control.player_by_id(targets_ids[0])
    checking.valid_target(user, target, 'arson attack', cards)
    checking.forbid_target_no_card_on_hand(target, game_control)

    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    game_control.push_frame(_ArsonAttack(game_control, user, target, cards))
    return { 'code': ret_code.OK }

def arson_attack_target(game_control, user, card):
    def check_has_card(target):
        count_cards = game_control.player_cards_count_at(target, 'onhand')
        if user == target:
            return 1 < count_cards
        return 0 < count_cards
    all_players = game_control.players_from_current()
    targets = filter(check_has_card, all_players)
    return fix_target_action(target_filter('arson attack', user, targets,
                                           [card]))

class _ArsonAttack(frames.FrameBase):
    def __init__(self, game_control, user, target, cards):
        frames.FrameBase.__init__(self, game_control)
        self.user = user
        self.target = target
        self.cards = cards

    def activated(self):
        self.resume = self.after_target_show_a_card
        self.game_control.push_frame(_TargetShowCard(self.game_control,
                                                     self.target))

    def after_target_show_a_card(self, args):
        show_suit = self.game_control.cards_by_ids(args['discard'])[0].suit()
        self.resume = self.user_discard_card
        self.game_control.push_frame(_UserDiscardSameSuit(self.game_control,
                                                          self.user, show_suit))

    def user_discard_card(self, args):
        if args['method'] != 'abort':
            damage.Damage(self.game_control, self.user, self.target,
                          'arson attack', self.cards, 'fire', 1
                         ).add_cleaner(lambda dmg, gc: self.done(None)
                         ).operate(self.game_control)
        else:
            self.done(None)

class _TargetShowCard(frames.ShowCards):
    def __init__(self, game_control, target):
        frames.ShowCards.__init__(self, game_control, target, self._show_check)

    def _show_check(self, cids):
        if len(cids) != 1:
            raise ValueError('need exactly one card')
        checking.cards_region(self.game_control.cards_by_ids(cids), 'onhand')

    def _hint_detail(self):
        cards = self.game_control.player_cards_at(self.player, 'onhand')
        return {
            'methods': {
                'show': {
                    'require': ['fix card count'],
                    'card count': 1,
                    'cards': map(lambda c: c.card_id, cards),
                }
            },
            'abort': 'disallow',
        }

class _UserDiscardSameSuit(frames.DiscardCards):
    def __init__(self, game_control, player, suit):
        frames.DiscardCards.__init__(self, game_control, player, self._check)
        self.suit = suit

    def _hint_detail(self):
        cards = self.game_control.player_cards_at(self.player, 'onhand')
        cards = filter(lambda c: c.suit() == self.suit, cards)
        return {
            'methods': {
                'discard': {
                    'require': ['fix card count'],
                    'card count': 1,
                    'cards': map(lambda c: c.card_id, cards),
                }
            },
            'abort': 'allow',
        }

    def react(self, args):
        if args['method'] == 'abort':
            return self.done(args)
        return frames.DiscardCards.react(self, args)

    def _check(self, cards_ids):
        cards = self.game_control.cards_by_ids(cards_ids)
        checking.only_one_card_of_suit(cards, self.suit)
