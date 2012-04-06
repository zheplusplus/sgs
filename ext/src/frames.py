import core.src.action_frames as core
import common_checking as checking
import hint_common as hints
from category_hierarchy import is_slash
from basiccards.slash import slash_targets_h, slash_action
from basiccards.peach import peach_h, peach_action
from equipment import equip
from sleevecards.arson_attack import arson_attack_target, arson_attack_action
from sleevecards.duel import duel_target, duel_action
from sleevecards.sabotage import sabotage_targets_h, sabotage_action
from sleevecards.steal import steal_target, steal_action

def _using_cards_map():
    return {
        'slash': slash_action,
        'thunder slash': slash_action,
        'fire slash': slash_action,
        'peach': peach_action,
        'arson attack': arson_attack_action,
        'duel': duel_action,
        'sabotage': sabotage_action,
        'steal': steal_action,
        'equip': equip.interface,
    }

def _hint_dict():
    return {
        'slash': slash_targets_h,
        'thunder slash': slash_targets_h,
        'fire slash': slash_targets_h,
        'peach': peach_h,
        'arson attack': arson_attack_target,
        'duel': duel_target,
        'sabotage': sabotage_targets_h,
        'steal': steal_target,
    }

class UseCards(core.UseCards):
    def __init__(self, game_control, player):
        core.UseCards.__init__(self, game_control, player, _using_cards_map())
        self.hint_dict = _hint_dict()
        self.hint_cache = hints.basic_cards_hint()
        self._update_hint()

    def event(self, action, **kwargs):
        if is_slash(action) and kwargs['user'] == self.player:
            del self.interface_map['slash']
            del self.hint_dict['slash']
            del self.interface_map['thunder slash']
            del self.hint_dict['thunder slash']
            del self.interface_map['fire slash']
            del self.hint_dict['fire slash']
            return True
        return False

    def react(self, args):
        if args['action'] == 'card':
            cards = self.game_control.cards_by_ids(args['use'])
            if len(cards) != 1:
                raise ValueError('wrong cards')
            if equip.is_equipment(cards[0].name()):
                args['action'] = 'equip'
            else:
                args['action'] = cards[0].name()
        r = core.UseCards.react(self, args)
        self._update_hint()
        return r

    def resume(self, result):
        self._update_hint()
        core.UseCards.resume(self, result)

    def destructed(self):
        self.player.discarding_cards_stage(self.game_control)

    def _update_hint(self):
        self.hint_cache = hints.allow_abort(hints.basic_cards_hint())
        self._build_card_hint()
        for h in self.player.using_hint():
            h(self.hint_cache, self.game_control, self.player,
              self.interface_map)
        if len(self.hint_cache['methods']) == 0:
            del self.hint_cache['methods']

    def _build_card_hint(self):
        cards = self.game_control.player_cards_at(self.player, 'onhand')
        equips = equip.hint(cards)
        for c in cards:
            if c.card_id in equips:
                self.add_card_hint(c, hints.implicit_target())
                continue
            self.add_card_hint(c, self._card_target_info(c))

    def _card_target_info(self, c):
        card_name = c.name()
        if card_name in self.hint_dict:
            return self.hint_dict[card_name](self.game_control, self.player, c)
        return hints.forbid()

    def add_card_hint(self, card, target_info):
        self.hint_cache['card'][card.card_id] = target_info

    def _hint_detail(self):
        return self.hint_cache

class DiscardCards(core.DiscardCards):
    def __init__(self, game_control, player):
        core.DiscardCards.__init__(self, game_control, player, self._check)
        self.need_discard = self.player.discard_count(game_control)

    def destructed(self):
        self.game_control.next_round()

    def _hint_detail(self):
        cards = self.game_control.player_cards_at(self.player, 'onhand')
        return {
            'methods': {
                'discard': {
                    'require': ['fix card count'],
                    'card count': self.need_discard,
                    'cards': map(lambda c: c.card_id, cards),
                }
            }
        }

    def _check(self, cards_ids):
        if len(cards_ids) != self.need_discard:
            raise ValueError('must discard %d cards' % self.need_discard)
        checking.cards_region(self.game_control.cards_by_ids(cards_ids),
                              'onhand')
