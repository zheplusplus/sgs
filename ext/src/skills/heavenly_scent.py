from core.src.action_frames import DiscardCards
from core.src.damage import Damage
import core.src.card as card
import ext.src.common_checking as checking

class _AskHeavenlyScent(DiscardCards):
    def __init__(self, game_control, damage):
        DiscardCards.__init__(
              self, game_control, damage.victim,
              lambda cards_ids: _check_one_heart_card(game_control, cards_ids),
              lambda gc, a: _damage_transfer(gc, a, damage))

    def react(self, args):
        cards = args['discard']
        if len(cards) > 0:
            targets_ids = args['targets']
            checking.only_one_target(targets_ids)
            checking.forbid_target_self(self.player.player_id, targets_ids[0])
        return DiscardCards.react(self, args)

    def _hint_detail(self):
        cards = self.game_control.player_cards_at(self.player, 'cards')
        cards = filter(lambda c: c.suit == card.HEART, cards)
        candidates = self.game_control.players_from_current()
        candidates.remove(self.player)
        return {
                   'discard': {
                       c.card_id: {
                         'type': 'fix target',
                         'count': 1,
                         'candidates': map(lambda p: p.player_id, candidates),
                       } for c in cards
                   },
                   'give up': 'allow',
               }

def _check_one_heart_card(game_control, cards_ids):
    if len(cards_ids) > 0:
        cards = game_control.cards_by_ids(cards_ids)
        checking.only_one_card_of_suit(cards, card.HEART)
        checking.cards_region(cards, 'cards')

def _damage_transfer(game_control, args, damage):
    if len(args['discard']) > 0:
        target = game_control.player_by_id(args['targets'][0])
        def draw_cards(d, game_control):
            game_control.deal_cards(target, target.max_vigor - target.vigor)
        Damage(damage.source, target, damage.action, damage.cards,
               damage.category, damage.point,
               [target.actions_before_damaged['equipment']['trigger'],
                target.actions_before_damaged['equipment']['ability']] +
                damage.source.computing_before_damaging +
                target.computing_before_damaged,
               damage.source.after_damaging_actions() +
               target.after_damaged_actions()
               ).add_affix(draw_cards).operate(game_control)
    else:
        damage.resume()

def add_to(player):
    player.actions_before_damaged['character']['ability'] = ask_damage_tranfer

def ask_damage_tranfer(damage, game_control):
    damage.interrupt(lambda:
            game_control.push_frame(_AskHeavenlyScent(game_control, damage)))
