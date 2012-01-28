import core.src.action_frames as frames
from player_using_cards import get_using_cards_interface_map
import common_checking as checking
import player_response as response
import core.src.event as event

STARTDEAL = 4
ROUNDDEAL = 2

class Player:
    def __init__(self, token):
        self.token = token
        self.responses = { 'slash': response.ToCertainCard('slash') }
        self.equipment = dict()
        self.cw_positive_dist_mod = 0
        self.ccw_positive_dist_mod = 0
        self.cw_passive_dist_mod = 0
        self.ccw_passive_dist_mod = 0
        self.ranges = { 'steal': 1 }
        self.actions_before_damaging = Player._damage_actions_dict()
        self.actions_before_damaged = Player._damage_actions_dict()
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
        self.get_cards(game_control, STARTDEAL)

    def round(self, game_control):
        self.getting_cards_stage(game_control)
        self.using_cards_stage(game_control)

    def getting_cards_stage(self, game_control):
        self.get_cards(game_control, ROUNDDEAL)

    def using_cards_stage(self, game_control):
        game_control.push_frame(
                frames.UseCards(game_control, self,
                                get_using_cards_interface_map(),
                                lambda gc, _: self.discarding_cards_stage(gc)))

    def discarding_cards_stage(self, game_control):
        def discard_check(cards_ids):
            checking.cards_region(game_control.cards_by_ids(cards_ids), 'cards')
            if len(cards_ids) != 2:
                raise ValueError('must discard 2 cards')
        game_control.push_frame(
                frames.DiscardCards(game_control, self, discard_check,
                                    self.cards_discarded))

    def cards_discarded(self, game_control, args):
        game_control.next_round()

    def get_cards(self, game_control, cnt):
        game_control.deal_cards(self, cnt)

    def response_frame(self, action, game_control, on_result):
        return self.responses[action].response(game_control, self, on_result)

    def equip(self, game_control, card, region, on_remove):
        if region in self.equipment:
            game_control.recycle_cards([self.unequip(game_control, region)])
        card.set_region(region)
        def rm_func():
            on_remove(game_control, self, card)
            return card
        self.equipment[region] = rm_func
        game_control.equip(self, card, region)

    def unequip_check(self, game_control, region):
        if not region in self.equipment:
            raise ValueError('no such equipment')
        return self.unequip(game_control, region)

    def unequip(self, game_control, region):
        return game_control.unequip(self, self.equipment[region](), region)

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
