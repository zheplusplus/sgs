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
        player = self.players_control.get_current_player()
        player.round(self)

    def get_events(self, token, prev_event_id):
        return self.events.serialize(token, prev_event_id)

    def deal_event(self, player, cnt):
        cards = self.card_pool.deal(cnt)
        e = event.DealCard(player, cards)
        self.events.add(e)
        return cards

    def discard_event(self, player, cards):
        self.card_pool.discard(cards)
        e = event.DiscardCard(player, cards)
        self.events.add(e)
