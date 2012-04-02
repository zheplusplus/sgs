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
        self.methods = dict()

    def add_method(self, method_name, method, hint):
        self.methods[method_name] = Response.Method(method, hint)

    def remove_method(self, method_name):
        del self.methods[method_name]

    def response(self, game_control, player):
        methods = { k: v.method for k, v in self.methods.items() }
        hints = reduce(lambda h, pair: dict(h.items() +
                                            pair[1].hint(game_control, player)
                                                   .items()),
                       self.methods.items(), dict())
        return _PlayFrame(game_control, player, methods, hints, self.abort)

    def allow_aborting(self):
        self.abort = 'allow'

class _BaseResponse(Response):
    def __init__(self, name):
        Response.__init__(self)
        self.name = name
        self.add_method(name, self.check, self.hint)

class ToCertainCard(_BaseResponse):
    def __init__(self, card_name):
        _BaseResponse.__init__(self, card_name)
        self.allow_aborting()

    def check(self, cards):
        checking.only_one_card_named_as(cards, self.name)

    def hint(self, gc, player):
        return hint_common.one_card_filter(gc, player, self.name,
                                           lambda c: c.name() == self.name)

class ToCardCategory(_BaseResponse):
    def __init__(self, name, category):
        _BaseResponse.__init__(self, name)
        self.category = category
        self.allow_aborting()

    def check(self, cards):
        checking.only_one_card_of_category(cards, self.category)

    def hint(self, gc, player):
        return hint_common.one_card_filter(gc, player, self.name,
                                           lambda c: self.category(c.name()))

class _PlayFrame(frames.PlayCards):
    def __init__(self, gc, player, methods, hints, abort):
        frames.PlayCards.__init__(self, gc, player, methods)
        self.hints = hints
        self.abort = abort

    def _hint_detail(self):
        return {
            'methods': self.hints,
            'abort': self.abort,
        }
