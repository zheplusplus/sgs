import core.src.action_frames as frames
import ext.src.common_checking as checking
from ext.src import hint_common

class Response:
    class Method:
        def __init__(self, method, hint):
            self.method = method
            self.hint = hint

    def __init__(self):
        self.abort = 'disallow'

    def add_method(self, method_name, method, hint):
        self.methods[method_name] = Response.Method(method, hint)

    def remove_method(self, method_name):
        del self.methods[method_name]

    def response(self, game_control, player, on_result):
        methods = dict()
        for k, v in self.methods.items(): methods[k] = v.method
        hints = dict()
        for k, v in self.methods.items():
            hints = dict(hints.items() + v.hint(game_control, player).items())
        return _PlayFrame(game_control, player, methods, hints, self.abort,
                          on_result)

    def allow_aborting(self):
        self.abort = 'allow'

class ToCertainCard(Response):
    def __init__(self, card_name):
        self.card_name = card_name
        self.allow_aborting()
        self.methods = dict()
        self.add_method(card_name, self._one_card_check, self._one_card_hint)

    def _one_card_check(self, cards):
        checking.only_one_card_named_as(cards, self.card_name)

    def _one_card_hint(self, game_control, player):
        return hint_common.one_card_filter(game_control, player, self.card_name,
                                           lambda c: c.name == self.card_name)

class _PlayFrame(frames.PlayCards):
    def __init__(self, gc, player, methods, hints, abort, on_result):
        frames.PlayCards.__init__(self, gc, player, methods, on_result)
        self.hints = hints
        self.abort = abort

    def _hint_detail(self):
        return {
                   'methods': self.hints,
                   'abort': self.abort,
               }
