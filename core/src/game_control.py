from card import Card
import event

class GameControl:
    events = None
    players_control = None
    card_pool = None

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
        return self.action_stack.call(args)

    def push_frame(self, frame):
        self.action_stack.push(frame)

    def pop_frame(self):
        self.action_stack.pop()

    def deal_cards(self, player, cnt):
        self.events.add(
                event.DealCards(player, self.card_pool.deal(player, cnt)))

    def discard_cards(self, player, cards_ids):
        cards = self.card_pool.cards_by_ids(cards_ids)
        self.events.add(event.DiscardCards(player, cards))
        self.card_pool.discard(cards)

    def use_cards_for_player(self, user, targets_ids, action, cards_ids):
        cards = self.card_pool.cards_by_ids(cards_ids)
        self.events.add(event.UseCardsForPlayers(user, targets_ids, action,
                                                 cards))
        self.card_pool.discard(cards)

    def show_cards(self, player, cards_ids):
        self.events.add(
                event.ShowCards(player, self.card_pool.cards_by_ids(cards_ids)))

    def damage(self, victim, damage, category):
        self.events.add(event.Damage(victim, damage, category))

    def cards_by_ids(self, cards_ids):
        return self.card_pool.cards_by_ids(cards_ids)

    def player_by_id(self, player_id):
        return self.players_control.get_by_id(player_id)

    def player_by_token(self, player_token):
        return self.players_control.get_by_token(player_token)
