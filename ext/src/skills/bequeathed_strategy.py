import core.src.ret_code as ret_code
from core.src.action_frames import CardsTargetFrame, FrameBase
import ext.src.common_checking as checking

class _BequeathedStrategyAfterDamage(FrameBase):
    def __init__(self, game_control, damage):
        FrameBase.__init__(self, game_control, lambda gc, a: damage.resume())
        self.damage = damage
        self.times = damage.point

    def resume(self, r):
        self.activated()

    def activated(self):
        if self.times == 0:
            return self.done(None)
        self.times -= 1
        self.game_control.push_frame(
                _BequeathedStrategyTransferCards(
                        self.game_control, self.damage.victim,
                        self.game_control.deal_cards(self.damage.victim, 2)))

class _BequeathedStrategyTransferCards(CardsTargetFrame):
    def __init__(self, game_control, source, cards):
        CardsTargetFrame.__init__(self, game_control, source, self.finished)
        self.cards = cards
        for c in self.cards: c.set_region('bequeathed strategy')
        self.rest = len(cards)
        self._update_hint()

    def react(self, args):
        if args['action'] == 'give up':
            return self.done(None)
        cards = self.game_control.cards_by_ids(args['transfer'])
        if len(cards) == 0:
            raise ValueError('bad cards')
        target = self.game_control.player_by_id(args['target'])
        checking.forbid_target_self(self.player, target)
        checking.cards_region(cards, 'bequeathed strategy')
        self.game_control.private_cards_transfer(self.player, target, cards)
        self._update_hint()
        self.rest -= len(cards)
        if self.rest == 0:
            return self.done(None)
        return { 'code': ret_code.OK }

    def finished(self, gc, a):
        for c in self.cards: c.set_region('cards')

    def _update_hint(self):
        self.clear_hint()
        candidates = self.game_control.players_from_current()
        candidates.remove(self.player)
        candidates = map(lambda p: p.player_id, candidates)
        for c in self.cards:
            self.add_hint_fix_target('transfer', c, 1, candidates)
        self.add_quit()

def add_to(player):
    player.actions_after_damaged['character']['ability'] = bequeathed_strategy

def bequeathed_strategy(damage, game_control):
    damage.interrupt(lambda: _push_bequeathed_strategy(game_control, damage))

def _push_bequeathed_strategy(game_control, damage):
    frame = _BequeathedStrategyAfterDamage(game_control, damage)
    game_control.push_frame(frame)
