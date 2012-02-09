from core.src.action_frames import DiscardCards
from core.src.damage import Damage
import core.src.card as card
import ext.src.common_checking as checking
import ext.src.wrappers as wrappers

class _AskHeavenlyScent(DiscardCards):
    def __init__(self, game_control, damage):
        DiscardCards.__init__(
              self, game_control, damage.victim,
              lambda cards_ids: _check_one_heart_card(game_control, cards_ids))
        self.damage = damage
        self.destructed = damage.resume

    def react(self, args):
        if args['action'] == 'abort':
            return self.done(args)

        args['discard'] = args['use']
        if len(args['discard']) == 0:
            raise ValueError('wrong cards')
        targets_ids = args['targets']
        checking.only_one_target(targets_ids)
        checking.forbid_target_self(self.player.player_id, targets_ids[0])
        self.destructed = lambda: _transfer_damage(self.game_control, args,
                                                   self.damage)
        return DiscardCards.react(self, args)

    def _hint_detail(self):
        cards = self.game_control.player_cards_at(self.player, 'onhand')
        cards = filter(lambda c: c.suit() == card.HEART, cards)
        targets = self.game_control.players_from_current()
        targets.remove(self.player)
        return {
            'card': {
                c.card_id: {
                  'type': 'fix target',
                  'target count': 1,
                  'targets': map(lambda p: p.player_id, targets),
                } for c in cards
            },
            'abort': 'allow',
        }

    def _hint_action(self, token):
        return 'use'

def _check_one_heart_card(game_control, cards_ids):
    cards = game_control.cards_by_ids(cards_ids)
    checking.only_one_card_of_suit(cards, card.HEART)
    checking.cards_region(cards, 'onhand')

def _transfer_damage(game_control, args, damage):
    target = game_control.player_by_id(args['targets'][0])
    def draw_cards(d, game_control):
        game_control.deal_cards(target, target.max_vigor - target.vigor)
    damage.victim = target
    damage.add_affix(draw_cards).resume()

def add_to(player):
    player.before_damaged_char = ask_damage_tranfer

@wrappers.alive
@wrappers.as_damage_victim
def ask_damage_tranfer(player, damage, game_control):
    damage.interrupt(lambda:
            game_control.push_frame(_AskHeavenlyScent(game_control, damage)))
