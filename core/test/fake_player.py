from core.src.player import Player as CorePlayer
import core.src.action_frames as frames

STARTDEAL = 4
ROUNDDEAL = 2

class Player(CorePlayer):
    def __init__(self, token):
        CorePlayer.__init__(self, token, dict())

    def start(self, game_control):
        self.draw_cards(game_control, STARTDEAL)

    def round(self, game_control):
        self.drawing_cards_stage(game_control)
        self.using_cards_stage(game_control)

    def drawing_cards_stage(self, game_control):
        self.draw_cards(game_control, ROUNDDEAL)

    def using_cards_stage(self, game_control):
        game_control.push_frame(
                frames.UseCards(game_control, self, {},
                                lambda gc, _: self.discarding_cards_stage(gc)))

    def discarding_cards_stage(self, game_control):
        def discard_filter(cards):
            if len(cards) != 2:
                raise ValueError('must discard 2 cards')
        game_control.push_frame(
                frames.DiscardCards(game_control, self, discard_filter,
                                    self.cards_discarded))

    def cards_discarded(self, game_control, args):
        game_control.next_round()
