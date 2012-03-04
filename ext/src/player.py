from core.src.player import Player as CorePlayer
import core.src.action_frames as frames
from player_using_cards import get_using_cards_interface_map
from player_as_target import player_as_target
from equipment import equip
import common_checking as checking
import player_response as response
import characters

START_DRAW = 4
ROUND_DRAW = 2

class Player(CorePlayer):
    def __init__(self, token):
        CorePlayer.__init__(self, token,
                            {
                                'slash': response.ToCertainCard('slash'),
                                'peach': response.ToCertainCard('peach'),
                            })
        self.ranges = { 'steal': 1 }
        self.as_target_filters = []
        self.actions_before_damaging = Player._damage_actions_dict()
        self.actions_before_damaged = Player._damage_actions_dict()
        self.computing_before_damaging = []
        self.computing_before_damaged = []
        self.actions_after_damaging = Player._damage_actions_dict()
        self.actions_after_damaged = Player._damage_actions_dict()

    @staticmethod
    def _damage_actions_dict():
        inaction = lambda d, gc: None
        return {
                   'status': [],
                   'character': { 'trigger': inaction, 'ability': inaction },
                   'equipment': { 'trigger': inaction, 'ability': inaction },
               }

    def start(self, game_control):
        self.draw_cards(game_control, START_DRAW)

    def round(self, game_control):
        self.drawing_cards_stage(game_control)
        self.using_cards_stage(game_control)

    def drawing_cards_stage(self, game_control):
        self.draw_cards(game_control, ROUND_DRAW)

    def target_filter(self, source, action, card):
        for f in self.as_target_filters:
            if f(self, source, action, card):
                return False
        return True

    def _build_using_card_hint(self, game_control, frame):
        cards = game_control.player_cards_at(self, 'cards')
        equips = equip.hint(cards)
        for c in cards:
            if c.card_id in equips:
                frame.add_hint('card', c, { 'type': 'implicit target' })
                continue
            frame.add_hint('card', c,
                           player_as_target(c.name)(game_control, self, c))

    def using_cards_stage(self, game_control):
        on_result = lambda gc, _: self.discarding_cards_stage(gc)
        me = self
        class UseCards(frames.UseCards):
            def __init__(self):
                frames.UseCards.__init__(self, game_control, me,
                                         get_using_cards_interface_map(),
                                         on_result)
                self._update_hint()

            def react(self, args):
                if args['action'] == 'card':
                    cards = self.game_control.cards_by_ids(args['use'])
                    if 0 == len(cards):
                        raise ValueError('wrong cards')
                    if equip.is_equipment(cards[0].name):
                        args['action'] = 'equip'
                    else:
                        args['action'] = cards[0].name
                r = frames.UseCards.react(self, args)
                self._update_hint()
                return r

            def resume(self, result):
                self._update_hint()
                frames.UseCards.resume(self, result)

            def _update_hint(self):
                self.clear_hint()
                self.add_abort()
                me._build_using_card_hint(game_control, self)

        game_control.push_frame(UseCards())

    def discard_count(self, game_control):
        return game_control.player_cards_count_at(self, 'cards') - self.vigor

    def discarding_cards_stage(self, game_control):
        need_discard = self.discard_count(game_control)
        class DiscardCards(frames.DiscardCards):
            def __init__(self, player, on_result):
                frames.DiscardCards.__init__(self, game_control, player,
                                             self.discard_check, on_result)

            def _hint_detail(self):
                candidates = game_control.player_cards_at(self.player, 'cards')
                return {
                    'methods': {
                        'discard': {
                            'require': ['count', 'candidates'],
                            'count': need_discard,
                            'candidates': map(lambda c: c.card_id, candidates),
                        }
                    }
                }

            def discard_check(self, cards_ids):
                if len(cards_ids) != need_discard:
                    raise ValueError('must discard %d cards' % need_discard)
                checking.cards_region(game_control.cards_by_ids(cards_ids),
                                      'cards')
        if self.alive and 0 < need_discard:
            game_control.push_frame(DiscardCards(self, self.cards_discarded))
        else:
            game_control.next_round()

    def cards_discarded(self, game_control, args):
        game_control.next_round()

    def before_damaging_actions(self):
        return (self.actions_before_damaging['status'] +
                [
                    self.actions_before_damaging['character']['trigger'],
                    self.actions_before_damaging['character']['ability'],
                    self.actions_before_damaging['equipment']['trigger'],
                    self.actions_before_damaging['equipment']['ability'],
                ])

    def after_damaging_actions(self):
        return (self.actions_after_damaging['status'] +
                [
                    self.actions_after_damaging['character']['trigger'],
                    self.actions_after_damaging['character']['ability'],
                    self.actions_after_damaging['equipment']['trigger'],
                    self.actions_after_damaging['equipment']['ability'],
                ])

    def before_damaged_actions(self):
        return (self.actions_before_damaged['status'] +
                [
                    self.actions_before_damaged['character']['trigger'],
                    self.actions_before_damaged['character']['ability'],
                    self.actions_before_damaged['equipment']['trigger'],
                    self.actions_before_damaged['equipment']['ability'],
                ])

    def after_damaged_actions(self):
        return (self.actions_after_damaged['status'] +
                [
                    self.actions_after_damaged['character']['trigger'],
                    self.actions_after_damaged['character']['ability'],
                    self.actions_after_damaged['equipment']['trigger'],
                    self.actions_after_damaged['equipment']['ability'],
                ])
