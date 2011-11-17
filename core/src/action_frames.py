import ret_code

class FrameBase:
    game_control = None
    on_result = None

    def __init__(self, game_control, on_result):
        self.game_control = game_control
        self.on_result = on_result

    def done(self, result):
        self.game_control.pop_frame()
        self.on_result(game_control, result)
        return { 'code': ret_code.OK }

class UseCards(FrameBase):
    player = None
    interface_map = {}

    def __init__(self, game_control, player, interface_map, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player
        self.interface_map = interface_map
        self.interface_map['give up'] = lambda gc, p, a, args: self.done({})

    def react(self, args):
        try:
            token = args['token']
            if token != self.player.token:
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.PLAYER_FORBID,
                       }
            if not args['action'] in self.interface_map:
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.INCORRECT_INTERFACE,
                       }
            return self.interface_map[args['action']](self.game_control,
                                                      self.player, args)
        except KeyError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_MISSING_ARG % str(e),
                   }

class ShowCards(FrameBase):
    player = None
    cards_filter = None

    def __init__(self, game_control, player_id, cards_filter, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = game_control.query_player_by_id(player_id)
        self.cards_filter = cards_filter

    def react(self, args):
        try:
            token = args['token']
            if token != self.player.token:
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.PLAYER_FORBID,
                       }
            cards = args['cards']
            if not cards_filter(cards):
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.WRONG_ARG,
                       }
            self.game_control.show_cards(self.player, cards)
            return self.done(cards)
        except KeyError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_MISSING_ARG % str(e),
                   }

class DiscardCards(FrameBase):
    player = None
    cards_filter = None

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
                           'reason': ret_code.PLAYER_FORBID,
                       }
            cards = args['cards']
            if not cards_filter(cards):
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.WRONG_ARG,
                       }
            self.game_control.discard_cards(self.player, cards)
            return self.done(cards)
        except KeyError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_MISSING_ARG % str(e),
                   }
