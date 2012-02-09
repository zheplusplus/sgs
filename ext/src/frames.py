import core.src.action_frames as core
from equipment import equip
import common_checking as checking
from basiccards.slash import slash_target, slash
from sleevecards.arson_attack import arson_attack_target, arson_attack
from sleevecards.duel import duel_target, duel
from sleevecards.sabotage import sabotage_target, sabotage
from sleevecards.steal import steal_target, steal
from equipment import equip

def _using_cards_map():
    return {
        'slash': slash,
        'arson attack': arson_attack,
        'duel': duel,
        'sabotage': sabotage,
        'steal': steal,
        'equip': equip.interface,
    }

def _hint_dict():
    return {
        'slash': slash_target,
        'arson attack': arson_attack_target,
        'duel': duel_target,
        'sabotage': sabotage_target,
        'steal': steal_target,
    }

class UseCards(core.UseCards):
    def __init__(self, game_control, player):
        core.UseCards.__init__(self, game_control, player, _using_cards_map())
        self.player.using_interfaces = self.interface_map
        self.hint_dict = _hint_dict()
        self.player.using_hint_dict = self.hint_dict
        self._update_hint()

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
        self.player.using_hint_dict = dict()
        self.player.using_interfaces = dict()
        self.player.discarding_cards_stage(self.game_control)

    def _target_info(self, c):
        card_name = c.name()
        if card_name in self.hint_dict:
            return self.hint_dict[card_name](self.game_control, self.player, c)
        return { 'type': 'forbid' }

    def _update_hint(self):
        self.clear_hint()
        self.add_abort()
        self._build_using_card_hint()
        self._hint_cache['methods'] = dict()
        self.player.on_using_hint_built(self._hint_cache, self.game_control)
        if len(self._hint_cache['methods']) == 0:
            del self._hint_cache['methods']

    def _build_using_card_hint(self):
        cards = self.game_control.player_cards_at(self.player, 'all')
        equips = equip.hint(self.game_control.player_cards_at(self.player,
                                                              'onhand'))
        for c in cards:
            if c.card_id in equips:
                self.add_hint('card', c, { 'type': 'implicit target' })
                continue
            self.add_hint('card', c, self._target_info(c))

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
