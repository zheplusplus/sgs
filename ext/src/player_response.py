import core.src.action_frames as frames
import ext.src.common_checking as checking

class Response:
    def add_method(self, method_name, method):
        self.methods[method_name] = method

    def remove_method(self, method_name):
        del self.methods[method_name]

    def response(self, game_control, player, on_result):
        return frames.PlayCards(game_control, player, self.methods, on_result)

    def allow_give_up(self, methods):
        methods['give up'] = self._give_up
        return methods

    def _give_up(self, cards):
        pass

class ToCertainCard(Response):
    def __init__(self, card_name):
        self.card_name = card_name
        self.methods = self.allow_give_up({ card_name: self._one_card })

    def _one_card(self, cards):
        checking.only_one_card_named_as(cards, self.card_name)
