import core.src.ret_code as ret_code
from core.src.action_frames import FrameBase, DiscardCards
import core.src.card as card
import ext.src.common_checking as checking
import ext.src.wrappers as wrappers

SKILL = 'heavenly scent'

class _Control(FrameBase):
    def __init__(self, gc, damage):
        FrameBase.__init__(self, gc)
        self.damage = damage

    def activated(self):
        self.game_control.push_frame(_Ask(self.game_control, self.damage))

    def resume(self, result):
        if result['action'] != 'abort':
            target = self.game_control.player_by_id(result['targets'][0])
            self.game_control.invoke(self.damage.victim, SKILL, [target])
            def draw_cards(d, gc):
                gc.deal_cards(target, target.max_vigor - target.vigor)
            self.damage.victim = target
            self.damage.push_tail_action(draw_cards)
        self.done(None)

    def destructed(self):
        self.damage.resume()

class _Ask(DiscardCards):
    def __init__(self, gc, damage):
        DiscardCards.__init__(
              self, gc, damage.victim,
              lambda cards_ids: _check_one_heart_card(gc, cards_ids))

    def react(self, args):
        if args['action'] == 'abort':
            return self.done(args)

        args['discard'] = args['use']
        if len(args['discard']) == 0:
            raise ValueError('wrong cards')
        targets_ids = args['targets']
        checking.only_one_target(targets_ids)
        checking.forbid_target_self(self.player.player_id, targets_ids[0])
        return DiscardCards.react(self, args)

    def _hint_detail(self):
        cards = self.game_control.player_cards_at(self.player, 'onhand')
        cards = filter(lambda c: c.suit() == card.HEART, cards)
        targets = self.game_control.players_from_current()
        targets.remove(self.player)
        import ext.src.hint_common as hints
        return hints.filter_empty(hints.allow_abort(hints.add_method_to(
                        hints.basic_cards_hint(), SKILL,
                        hints.join_req(hints.fixed_card_count(cards, 1),
                                       hints.fixed_target_count(targets, 1)))))

    def _hint_action(self, token):
        return 'use'

def _check_one_heart_card(gc, cards_ids):
    cards = gc.cards_by_ids(cards_ids)
    checking.only_one_card_of_suit(cards, card.HEART)
    checking.cards_region(cards, 'onhand')

def add_to(player):
    player.before_damaged_char = ask_damage_tranfer

@wrappers.alive
@wrappers.as_damage_victim
def ask_damage_tranfer(player, damage, gc):
    damage.interrupt(lambda: gc.push_frame(_Control(gc, damage)))
