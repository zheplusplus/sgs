import core.src.action_frames as frames
import core.src.ret_code as ret_code
import ext.src.damage as damage
import ext.src.common_checking as checking
from ext.src.hint_common import fix_target_action, target_filter

def duel_action(gc, args):
    cards = gc.cards_by_ids(args['use'])
    checking.only_one_card_named_as(cards, 'duel')
    return duel_check(gc, args)

def duel_check(game_control, args):
    targets_ids = args['targets']
    user = game_control.player_by_token(args['token'])
    cards = game_control.cards_by_ids(args['use'])
    checking.only_one_target(targets_ids)
    target = game_control.player_by_id(targets_ids[0])
    checking.valid_target(user, target, 'duel', cards)
    checking.forbid_target_self(user, target)

    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    game_control.push_frame(_Duel(game_control, user, target, cards))
    return { 'code': ret_code.OK }

def duel_target(game_control, user, card):
    targets = game_control.succeeding_players()
    return fix_target_action(target_filter('duel', user, targets, [card]))

class _Duel(frames.FrameBase):
    def __init__(self, game_control, user, target, cards):
        frames.FrameBase.__init__(self, game_control)
        self.user = user
        self.target = target
        self.cards = cards

    def activated(self):
        self.resume = self.target_play_slash
        self.play_slash(self.target)

    def target_play_slash(self, args):
        if args['method'] == 'abort':
            self.damaging(self.user, self.target)
        else:
            self.play_slash(self.user)
        self.resume = self.user_play_slash

    def user_play_slash(self, args):
        if args['method'] == 'abort':
            self.damaging(self.target, self.user)
        else:
            self.play_slash(self.target)
        self.resume = self.target_play_slash

    def play_slash(self, player):
        self.game_control.push_frame(player.response_frame('slash',
                                                           self.game_control))

    def damaging(self, source, target):
        damage.Damage(self.game_control, source, target, 'duel', self.cards,
                      'normal', 1
                      ).add_cleaner(lambda d, gc: self.done(None)
                      ).operate(self.game_control)
