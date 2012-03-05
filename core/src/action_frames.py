import ret_code
import card

class FrameBase:
    def __init__(self, game_control, on_result):
        self.game_control = game_control
        self.on_result = on_result

    def done(self, result):
        self.game_control.pop_frame(result)
        return { 'code': ret_code.OK }

    def resume(self, result):
        pass

    def activated(self):
        pass

    def hint(self, token):
        return dict({
            'code': ret_code.OK,
            'players': map(lambda p: p.player_id, self.allowed_players()),
            'action': self._hint_action(token),
        }.items() + self._hint(token).items())

def check_owner(owner, cards):
    for c in cards:
        if owner != c.owner_or_nil:
            raise ValueError('not own this card')

class OnePlayerFrame(FrameBase):
    def __init__(self, game_control, player, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.player = player

    def allowed_players(self):
        return [self.player]

class CardsTargetFrame(OnePlayerFrame):
    def __init__(self, game_control, player, on_result):
        OnePlayerFrame.__init__(self, game_control, player, on_result)
        self._hint_cache = dict()

    def clear_hint(self):
        self._hint_cache = dict()

    def add_hint_forbidden(self, category, card):
        self.add_hint(category, card, { 'type': 'forbid' })

    def add_hint_fix_target(self, category, card, count, candidates):
        self.add_hint(category, card, {
            'type': 'fix target',
            'count': count,
            'candidates': candidates,
        })

    def add_hint(self, category, card, target_info):
        if not category in self._hint_cache:
            self._hint_cache[category] = dict()
        self._hint_cache[category][card.card_id] = target_info

    def set_hint_category(self, category, hint_info):
        self._hint_cache[category] = hint_info

    def add_abort(self):
        self._hint_cache['abort'] = 'allow'

    def _hint(self, token):
        return self._hint_cache if self.player.token == token else dict()

class UseCards(CardsTargetFrame):
    def __init__(self, game_control, player, interface_map, on_result):
        CardsTargetFrame.__init__(self, game_control, player, on_result)
        self.interface_map = interface_map
        self.interface_map['abort'] = lambda gc, a: self.done(None)

    def react(self, args):
        cards = []
        if 'use' in args:
            cards = self.game_control.cards_by_ids(args['use'])
            check_owner(self.player, cards)

        if not args['action'] in self.interface_map:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_INCORRECT_INTERFACE,
                   }

        with card.InUseStatusRestore(cards):
            return self.interface_map[args['action']](self.game_control, args)

    def resume(self, result):
        if not self.player.alive:
            self.done(None)

    def _hint_action(self, token):
        return 'use'

class ShowCards(OnePlayerFrame):
    def __init__(self, game_control, player, cards_check, on_result):
        OnePlayerFrame.__init__(self, game_control, player, on_result)
        self.cards_check = cards_check

    def react(self, args):
        cards = args['discard']
        check_owner(self.player, self.game_control.cards_by_ids(cards))
        self.cards_check(cards)
        self.game_control.show_cards(self.player, cards)
        return self.done(args)

    def _hint(self, token):
        return self._hint_detail() if self.player.token == token else dict()

    def _hint_action(self, token):
        return 'discard'

class DiscardCards(OnePlayerFrame):
    def __init__(self, game_control, player, cards_check, on_result):
        OnePlayerFrame.__init__(self, game_control, player, on_result)
        self.cards_check = cards_check

    def react(self, args):
        cards_ids = args['discard']
        check_owner(self.player, self.game_control.cards_by_ids(cards_ids))
        self.cards_check(cards_ids)
        self.game_control.discard_cards_by_ids(self.player, cards_ids)
        return self.done(args)

    def _hint(self, token):
        return self._hint_detail() if self.player.token == token else dict()

    def _hint_action(self, token):
        return 'discard'

class PlayCards(OnePlayerFrame):
    def __init__(self, game_control, player, methods, on_result):
        OnePlayerFrame.__init__(self, game_control, player, on_result)
        self.methods = methods

    def allowed_players(self):
        return [self.player]

    def react(self, args):
        if args['method'] == 'abort':
            return self.done(args)

        cards = []
        if 'discard' in args:
            cards = self.game_control.cards_by_ids(args['discard'])
            check_owner(self.player, cards)
        method = args['method']
        if not method in self.methods:
            raise ValueError('no such method')
        self.methods[method](cards)
        self.game_control.play_cards(self.player, cards)
        return self.done(args)

    def _hint(self, token):
        return self._hint_detail() if self.player.token == token else dict()

    def _hint_action(self, token):
        return 'discard'

class AcceptMessage(FrameBase):
    def __init__(self, game_control, players, action, hint, on_message,
                 on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.frame_action = action
        self.frame_hint = hint
        self.players = players
        self.on_message = on_message

    def allowed_players(self):
        return self.players

    def react(self, args):
        self.on_message(args)
        return self.done(args)

    def _hint_action(self, token):
        return self.frame_action

    def _hint(self, token):
        if token in map(lambda p: p.token, self.players):
            return self.frame_hint
        return dict()
