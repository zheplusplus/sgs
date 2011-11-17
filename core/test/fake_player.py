import core.src.action_frames as frames
import fake_frame_actions as fake_actions

STARTDEAL = 4
ROUNDDEAL = 2

class Player:
    token = 0
    player_id = 0
    cards = []

    def __init__(self, token, pid):
        self.token = token
        self.player_id = pid
        self.cards = []

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
                                fake_actions.get_using_cards_interface_map(),
                                lambda gc, _: self.discarding_cards_stage(gc)))

    def discarding_cards_stage(self, game_control):
        def discard_filter(cards):
            return len(cards) == 2
        game_control.push_frame(
                frames.DiscardCards(game_control, self, discard_filter,
                                    self.cards_discarded))

    def cards_discarded(self, game_control, args):
        # FIX arguments map may not be like this
        discarded = args['cards']
        self.cards = filter(lambda c: not c.card_id in discarded, self.cards)
        game_control.discard_cards(self, discarded)
        game_control.next_round()

    def get_cards(self, game_control, cnt):
        cards = game_control.deal_cards(self, cnt)
        self.cards.extend(cards)