import core.src.action_frames as frames
import core.src.action_flow as flow
import core.src.ret_code as ret_code
import ext.src.damage as damage
import ext.src.common_checking as checking
from ext.src.hint_common import fix_target_action, target_filter, range_filter

def slash_action(gc, args):
    cards = gc.cards_by_ids(args['use'])
    checking.only_one_card_named_as(cards, args['action'])
    return slash_check(gc, args)

def slash_check(game_control, args):
    targets_ids = args['targets']
    user = game_control.player_by_token(args['token'])
    cards = game_control.cards_by_ids(args['use'])
    checking.only_one_target(targets_ids)
    target = game_control.player_by_id(targets_ids[0])
    action = args['action']
    checking.valid_target(user, target, action)
    checking.forbid_target_self(user, target)
    checking.within_range(game_control, user, target, 'slash')

    game_control.use_cards_for_players(user, targets_ids, action, cards)
    _SlashFlow(game_control, user, target, cards, action).resume()
    return { 'code': ret_code.OK }

def slash_targets(gc, user):
    players = gc.players_from_current()
    players.remove(user)
    players = range_filter(gc, user, 'slash', players)
    return target_filter('slash', user, players)

def slash_targets_h(gc, user):
    return fix_target_action(slash_targets(gc, user))

DAMAGE_CATEGORY_MAP = {
    'slash': 'normal',
    'thunder slash': 'thunder',
    'fire slash': 'fire',
}

class _SlashResult(frames.FrameBase):
    def __init__(self, game_control, user, target, cards, category):
        frames.FrameBase.__init__(self, game_control)
        self.user = user
        self.target = target
        self.cards = cards
        self.category = category

    def resume(self, args):
        if args['method'] == 'abort':
            damage.Damage(self.game_control, self.user, self.target, 'slash',
                          self.cards, self.category, 1
                          ).add_cleaner(lambda d, gc: self.done(None)
                          ).resume()
        else:
            self.done(None)

class _SlashFlow(flow.ActionFlow):
    def __init__(self, game_control, user, target, cards, action):
        players = game_control.players_from_current()
        flow.ActionFlow.__init__(
                    self, game_control,
                    flow.map_action(lambda p: p.slashing_char, players) +
                      flow.map_action(lambda p: p.slashing_equip, players) +
                      flow.map_action(lambda p: p.slashed_char, players) +
                      flow.map_action(lambda p: p.slashed_equip, players))
        self.user = user
        self.target = target
        self.cards = cards
        self.action = action
        self.response_frame = target.response_frame('dodge', game_control)
        self.push_tail_action(self.tail_action)

    def tail_action(self, flow, gc):
        gc.push_frame(_SlashResult(gc, flow.user, flow.target, flow.cards,
                                   DAMAGE_CATEGORY_MAP[flow.action]))
        gc.push_frame(self.response_frame)
