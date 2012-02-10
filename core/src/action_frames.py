import ret_code

class FrameBase:
    def __init__(self, game_control, on_result):
        self.game_control = game_control
        self.on_result = on_result

    def done(self, result):
        self.game_control.pop_frame()
        self.on_result(self.game_control, result)
        return { 'code': ret_code.OK }

    def resume(self):
        pass

    def hint(self):
        return self.__class__.__name__

def check_owner(owner, cards):
    for c in cards:
        if owner != c.owner_or_nil:
            raise ValueError('not own this card')

class UseCards(FrameBase):
    def __init__(self, game_control, player, interface_map, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player
        self.interface_map = interface_map
        self.interface_map['give up'] = lambda gc, a: self.done(None)

    def allowed_players(self):
        return [self.player]

    def react(self, args):
        if not args['action'] in self.interface_map:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_INCORRECT_INTERFACE,
                   }
        cards = []
        if 'use' in args:
            cards = self.game_control.cards_by_ids(args['use'])
            check_owner(self.player, cards)

        import card
        with card.InUseStatusRestore(cards):
            return self.interface_map[args['action']](self.game_control, args)

    def resume(self):
        if not self.player.alive:
            self.done(None)

class ShowCards(FrameBase):
    def __init__(self, game_control, player, cards_check, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player
        self.cards_check = cards_check

    def allowed_players(self):
        return [self.player]

    def react(self, args):
        cards = args['show']
        check_owner(self.player, self.game_control.cards_by_ids(cards))
        self.cards_check(cards)
        self.game_control.show_cards(self.player, cards)
        return self.done(args)

class DiscardCards(FrameBase):
    def __init__(self, game_control, player, cards_check, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player
        self.cards_check = cards_check

    def allowed_players(self):
        return [self.player]

    def react(self, args):
        cards_ids = args['discard']
        check_owner(self.player, self.game_control.cards_by_ids(cards_ids))
        self.cards_check(cards_ids)
        if len(cards_ids) > 0:
            self.game_control.discard_cards_by_ids(self.player, cards_ids)
        return self.done(args)

class PlayCards(FrameBase):
    def __init__(self, game_control, player, methods, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player
        self.methods = methods

    def allowed_players(self):
        return [self.player]

    def react(self, args):
        cards = []
        if 'play' in args:
            cards = self.game_control.cards_by_ids(args['play'])
            check_owner(self.player, cards)
        method = args['method']
        if not method in self.methods:
            raise ValueError('no such method')
        self.methods[method](cards)
        if len(cards) > 0:
            self.game_control.play_cards(self.player, cards)
        return self.done(args)

class AcceptMessage(FrameBase):
    def __init__(self, game_control, players, hint, on_message, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.frame_hint = hint
        self.players = players
        self.on_message = on_message

    def allowed_players(self):
        return self.players

    def react(self, args):
        self.on_message(args)
        return self.done(args)

    def hint(self):
        return self.frame_hint
