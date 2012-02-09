from core.src.player import Player as CorePlayer
import core.src.action_frames as frames

STARTDEAL = 4
ROUNDDEAL = 2

class UseCardsStage(frames.UseCards):
    def __init__(self, game_control, player, interface_map):
        frames.UseCards.__init__(self, game_control, player, interface_map)

    def destructed(self):
        self.player.discarding_cards_stage(self.game_control)

class DiscardCardsStage(frames.DiscardCards):
    def __init__(self, game_control, player, discard_filter):
        frames.DiscardCards.__init__(self, game_control, player, discard_filter)

    def destructed(self):
        self.game_control.next_round()

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
        game_control.push_frame(UseCardsStage(game_control, self, dict()))

    def discarding_cards_stage(self, game_control):
        def discard_filter(cards):
            if len(cards) != 2:
                raise ValueError('must discard 2 cards')
        game_control.push_frame(DiscardCardsStage(game_control, self,
                                                  discard_filter))
