from core.src.player import Player as CorePlayer
import core.src.action_frames as frames
from player_using_cards import get_using_cards_interface_map
import common_checking as checking
import player_response as response
import characters

STARTDEAL = 4
ROUNDDEAL = 2

class Player(CorePlayer):
    def __init__(self, token):
        CorePlayer.__init__(self, token,
                            {
                                'slash': response.ToCertainCard('slash'),
                                'peach': response.ToCertainCard('peach'),
                            })
        self.ranges = { 'steal': 1 }
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
        self.draw_cards(game_control, STARTDEAL)

    def round(self, game_control):
        self.drawing_cards_stage(game_control)
        self.using_cards_stage(game_control)

    def drawing_cards_stage(self, game_control):
        self.draw_cards(game_control, ROUNDDEAL)

    def using_cards_stage(self, game_control):
        game_control.push_frame(
                frames.UseCards(game_control, self,
                                get_using_cards_interface_map(),
                                lambda gc, _: self.discarding_cards_stage(gc)))

    def discard_count(self, game_control):
        return game_control.player_cards_count_at(self, 'cards') - self.vigor

    def discarding_cards_stage(self, game_control):
        need_discard = self.discard_count(game_control)
        class DiscardCards(frames.DiscardCards):
            def __init__(self, player, on_result):
                frames.DiscardCards.__init__(self, game_control, player,
                                             self.discard_check, on_result)

            def _hint(self, token):
                return {
                           'require': ['count', 'region'],
                           'count': need_discard,
                           'region': 'cards',
                           'give up': 'disallow',
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
