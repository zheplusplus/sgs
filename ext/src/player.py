import core.src.action_frames as frames
from player_using_cards import get_using_cards_interface_map
import common_checking as checking
import player_response as response
import core.src.event as event

STARTDEAL = 4
ROUNDDEAL = 2

class Player:
    def __init__(self, token, pid):
        self.token = token
        self.player_id = pid
        self.responses = { 'slash': response.ToCertainCard('slash') }
        self.equipment = dict()

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
        game_control.discard_cards_by_ids(self, args['discard'])
        game_control.next_round()

    def get_cards(self, game_control, cnt):
        game_control.deal_cards(self, cnt)

    def response_frame(self, action, game_control, on_result):
        return self.responses[action].response(game_control, self, on_result)

    def equip(self, game_control, region, card, on_remove):
        if region in self.equipment:
            self.equipment[region]()
        card.set_region(region)
        self.equipment[region] = on_remove
        game_control.add_event(event.Equip(self, card, region))

    def remove_equip(self, region):
        if not region in self.equipment:
            raise ValueError('no such equipment')
        self.equipment[region]()
