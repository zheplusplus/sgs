import core.src.ret_code as ret_code
from core.src.action_frames import FrameBase, CardsTargetFrame
import ext.src.common_checking as checking
import ext.src.wrappers as wrappers

class _BequeathedStrategyAfterDamage(FrameBase):
    def __init__(self, game_control, damage):
        FrameBase.__init__(self, game_control)
        self.damage = damage
        self.times = damage.point

    def activated(self):
        if self.times == 0:
            return self.done(None)
        self.times -= 1
        self.game_control.push_frame(
                _BequeathedStrategyTransferCards(
                        self.game_control, self.damage.victim,
                        self.game_control.deal_cards(self.damage.victim, 2)))

    def resume(self, r):
        self.activated()

    def destructed(self):
        self.damage.resume()

class _BequeathedStrategyTransferCards(CardsTargetFrame):
    def __init__(self, game_control, source, cards):
        CardsTargetFrame.__init__(self, game_control, source)
        self.cards = cards
        for c in self.cards: c.set_region('bequeathed strategy')
        self._update_hint()

    def react(self, args):
        if args['action'] == 'abort':
            return self.done(None)
        cards = self.game_control.cards_by_ids(args['use'])
        if len(cards) == 0:
            raise ValueError('bad cards')
        targets_ids = args['targets']
        checking.only_one_target(targets_ids)
        target = self.game_control.player_by_id(targets_ids[0])
        checking.forbid_target_self(self.player, target)
        checking.cards_region(cards, 'bequeathed strategy')

        for c in cards: c.set_region('onhand')
        self.game_control.private_cards_transfer(self.player, target, cards)
        self.cards = [c for c in self.cards if c not in cards]
        self._update_hint()
        if len(self.cards) == 0:
            return self.done(None)
        return { 'code': ret_code.OK }

    def destructed(self):
        for c in self.cards: c.set_region('onhand')

    def _update_hint(self):
        self.clear_hint()
        targets = self.game_control.players_from_current()
        targets.remove(self.player)
        hint = {
            'bequeathed strategy': {
                'require': ['fix target', 'min card count'],
                'target count': 1,
                'targets': map(lambda p: p.player_id, targets),
                'cards': map(lambda c: c.card_id, self.cards),
                'card count': 1,
            }
        }
        self.set_hint_category('methods', hint)
        self.add_abort()

    def _hint_action(self, token):
        return 'use'

def add_to(player):
    player.after_damaged_char = bequeathed_strategy

@wrappers.alive
@wrappers.as_damage_victim
def bequeathed_strategy(player, damage, game_control):
    damage.interrupt(lambda: game_control.push_frame(
                        _BequeathedStrategyAfterDamage(game_control, damage)))
