from card import Card
import ret_code
import event

class GameControl:
    def __init__(self, event_list, card_pool, players_control, action_stack):
        self.events = event_list
        self.players_control = players_control
        self.card_pool = card_pool
        self.action_stack = action_stack

    def start(self):
        for player in self.players_control.players:
            player.start(self)
        self.players_control.current_player().round(self)

    def next_round(self):
        self.players_control.next_player()
        self.players_control.current_player().round(self)

    def get_events(self, token, prev_event_id):
        return self.events.serialize(token, prev_event_id)

    def player_act(self, args):
        try:
            if not args['token'] in map(
                    lambda p: p.token, self.action_stack.allowed_players()):
                return {
                           'code': ret_code.BAD_REQUEST,
                           'reason': ret_code.BR_PLAYER_FORBID,
                       }
            return self.action_stack.call(args)
        except KeyError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_MISSING_ARG % e.message,
                   }
        except ValueError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_WRONG_ARG,
                   }

    def push_frame(self, frame):
        self.action_stack.push(frame)

    def pop_frame(self):
        self.action_stack.pop()

    def deal_cards(self, player, cnt):
        self.events.add(
                event.DealCards(player, self.card_pool.deal(player, cnt)))

    def discard_cards_by_ids(self, player, cards_ids):
        self.discard_cards(player, self.card_pool.cards_by_ids(cards_ids))

    def discard_cards(self, player, cards):
        self.events.add(event.DiscardCards(player, cards))
        self.card_pool.discard(cards)

    def use_cards_for_players(self, user, targets_ids, action, cards):
        self.events.add(event.UseCardsForPlayers(user, targets_ids, action,
                                                 cards))
        self.card_pool.discard(cards)

    def show_cards(self, player, cards_ids):
        self.events.add(
                event.ShowCards(player, self.card_pool.cards_by_ids(cards_ids)))

    def play_cards(self, player, cards_ids):
        cards = self.card_pool.cards_by_ids(cards_ids)
        self.events.add(event.PlayCards(player, cards))
        self.card_pool.discard(cards)

    def damage(self, victim, damage, category):
        self.events.add(event.Damage(victim, damage, category))

    def cards_by_ids(self, cards_ids):
        return self.card_pool.cards_by_ids(cards_ids)

    def player_by_id(self, player_id):
        return self.players_control.get_by_id(player_id)

    def player_by_token(self, player_token):
        return self.players_control.get_by_token(player_token)

    def player_has_cards(self, player):
        return self.card_pool.player_has_cards(player)

    def get_all_players(self):
        return self.players_control.players

    def random_pick_cards(self, player, count):
        return self.card_pool.random_pick_cards(player, count)
