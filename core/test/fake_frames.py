import core.src.ret_code

#FIX there is no giving up yet...

class UsingCard:
    game_control = None
    player = None
    interface_map = {}

    def __init__(self, game_control, player):
        self.game_control = game_control
        self.player = player
        interface_map = {
                    'fire attact': self.fire_attack,
                    'duel': self.duel,
                }

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
            self.interface_map[args['action']](args)
        except KeyError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_MISSING_ARG % str(e),
                   }

    def fire_attack(self, args):
        targets = args['targets']
        cards = args['cards']
        if 1 != len(targets):
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.WRONG_ARG,
                   }
        if 1 != len(cards) and 'fire attack' != cards[0].name:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.WRONG_ARG,
                   }
        # FIX: there should have been other checks
        self.game_control.cards_used(user_token, targets, args['action'], cards)
        shown = self.game_control.push_frame(
                        ShowCard(self.game_control, targets[0]))

    def duel(self, args):
        pass

class ShowCard:
    game_control = None
    player_id = 0
    player_token = 0

    def __init__(self, game_control, player_id):
        self.game_control = game_control
        self.player_id = player_id
        self.player_token = game_control.query_token_by_id(player_id)

    def react(self, args):
        pass

class DiscardCard:
    game_control = None
    player_token = 0
    cards_filter = None

    def __init__(self, game_control, player_token, cards_filter):
        self.game_control = game_control
        self.player_token = player_token
        self.cards_filter = cards_filter

    def react(self, args):
        pass
