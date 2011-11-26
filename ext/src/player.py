import core.src.action_frames as frames
from player_using_cards import get_using_cards_interface_map

STARTDEAL = 4
ROUNDDEAL = 2

class Player:
    def __init__(self, token, pid):
        self.token = token
        self.player_id = pid

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
        def discard_filter(cards):
            return len(cards) == 2
        game_control.push_frame(
                frames.DiscardCards(game_control, self, discard_filter,
                                    self.cards_discarded))

    def cards_discarded(self, game_control, args):
        game_control.discard_cards(self, args['discard'])
        game_control.next_round()

    def get_cards(self, game_control, cnt):
        game_control.deal_cards(self, cnt)