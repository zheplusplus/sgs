from card import Card
import event

class GameControl:
    events = None
    players_control = None
    card_pool = None

    def __init__(self, event_list, card_pool, players_control):
        self.events = event_list
        self.players_control = players_control
        self.card_pool = card_pool

    def start(self):
        for player in self.players_control.players:
            player.start(self)

    def next_round(self):
        self.players_control.current_player().round(self)

    def get_events(self, token, prev_event_id):
        return self.events.serialize(token, prev_event_id)

    def deal_cards(self, player, cnt):
        cards = self.card_pool.deal(cnt)
        self.events.add(event.DealCards(player, cards))
        return cards

    def discard_cards(self, player, cards):
        self.events.add(
                event.DiscardCards(player, self.card_pool.discard(cards)))

    def use_cards_for_player(self, user, targets, action, cards):
        pass

    def damage(self, victim, damage, category):
        pass

    def player_act(self, args):
        pass

    def push_frame(self, frame):
        pass

    def pop_frame(self):
        pass

    def query_player_by_id(self, player_id):
        pass

    def query_player_by_token(self, player_token):
        pass
