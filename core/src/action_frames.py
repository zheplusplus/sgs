import ret_code

class FrameBase:
    def __init__(self, game_control, on_result):
        self.game_control = game_control
        self.on_result = on_result

    def done(self, result):
        self.game_control.pop_frame()
        self.on_result(self.game_control, result)
        return { 'code': ret_code.OK }

class UseCards(FrameBase):
    def __init__(self, game_control, player, interface_map, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player
        self.interface_map = interface_map
        self.interface_map['give up'] = lambda gc, a: self.done({})

    def react(self, args):
        try:
            token = args['token']
            if token != self.player.token:
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.BR_PLAYER_FORBID,
                       }
            if not args['action'] in self.interface_map:
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.INCORRECT_INTERFACE,
                       }
            return self.interface_map[args['action']](self.game_control, args)
        except KeyError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_MISSING_ARG % str(e),
                   }

class ShowCards(FrameBase):
    def __init__(self, game_control, player, cards_filter, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player
        self.cards_filter = cards_filter

    def react(self, args):
        try:
            token = args['token']
            if token != self.player.token:
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.BR_PLAYER_FORBID,
                       }
            cards = args['cards']
            if not self.cards_filter(cards):
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.WRONG_ARG,
                       }
            self.game_control.show_cards(self.player, cards)
            return self.done(args)
        except KeyError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_MISSING_ARG % str(e),
                   }

class DiscardCards(FrameBase):
    def __init__(self, game_control, player, cards_filter, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.game_control = game_control
        self.player = player
        self.cards_filter = cards_filter

    def react(self, args):
        try:
            token = args['token']
            if token != self.player.token:
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.BR_PLAYER_FORBID,
                       }
            if not self.cards_filter(args['discard']):
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.WRONG_ARG,
                       }
            return self.done(args)
        except KeyError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_MISSING_ARG % str(e),
                   }
