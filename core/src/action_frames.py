import ret_code

class FrameBase:
    def __init__(self, game_control, on_result):
        self.game_control = game_control
        self.on_result = on_result

    def done(self, result):
        self.game_control.pop_frame()
        self.on_result(self.game_control, result)
        return { 'code': ret_code.OK }

def check_owner(owner, cards):
    for c in cards:
        if owner != c.owner_or_nil:
            raise ValueError('not own this card')

class UseCards(FrameBase):
    def __init__(self, game_control, player, interface_map, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player
        self.interface_map = interface_map
        self.interface_map['give up'] = lambda gc, a: self.done({})

    def allowed_players(self):
        return [self.player]

    def react(self, args):
            if not args['action'] in self.interface_map:
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.BR_INCORRECT_INTERFACE,
                       }
            if 'cards' in args:
                check_owner(self.player,
                            self.game_control.cards_by_ids(args['cards']))
            return self.interface_map[args['action']](self.game_control, args)

class ShowCards(FrameBase):
    def __init__(self, game_control, player, cards_filter, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player
        self.cards_filter = cards_filter

    def allowed_players(self):
        return [self.player]

    def react(self, args):
            cards = args['show']
            if not self.cards_filter(cards):
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.BR_WRONG_ARG,
                       }
            check_owner(self.player,
                        self.game_control.cards_by_ids(args['show']))
            self.game_control.show_cards(self.player, cards)
            return self.done(args)

class DiscardCards(FrameBase):
    def __init__(self, game_control, player, cards_filter, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.game_control = game_control
        self.player = player
        self.cards_filter = cards_filter

    def allowed_players(self):
        return [self.player]

    def react(self, args):
            if not self.cards_filter(args['discard']):
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.BR_WRONG_ARG,
                       }
            check_owner(self.player,
                        self.game_control.cards_by_ids(args['discard']))
            return self.done(args)

class PlayCards(FrameBase):
    def __init__(self, game_control, player, cards_filter, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player
        self.game_control = game_control
        self.cards_filter = cards_filter

    def allowed_players(self):
        return [self.player]

    def react(self, args):
            cards = args['play']
            if not self.cards_filter(args['play']):
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.BR_WRONG_ARG,
                       }
            check_owner(self.player,
                        self.game_control.cards_by_ids(args['play']))
            if len(cards) > 0:
                self.game_control.play_cards(self.player, cards)
            return self.done(args)
