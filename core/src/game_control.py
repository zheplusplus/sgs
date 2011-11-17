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
        self.next_round()

    def next_round(self):
        self.players_control.current_player().round(self)

    def get_events(self, token, prev_event_id):
        return self.events.serialize(token, prev_event_id)

    def player_act(self, args):
        pass

    def push_frame(self, frame):
        pass

    def pop_frame(self):
        pass

    def deal_cards(self, player, cnt):
        self.events.add(
                event.DealCards(player, self.card_pool.deal(player, cnt)))

    def discard_cards(self, player, cards_ids):
        cards = self.card_pool.cards_by_ids(cards_ids)
        self.events.add(event.DiscardCards(player, cards))
        self.card_pool.discard(cards)

    def use_cards_for_player(self, user, targets, action, cards_ids):
        cards = self.card_pool.cards_by_ids(cards_ids)
        self.events.add(event.UseCardsForPlayers(user, targets, action, cards))
        self.card_pool.discard(cards)

    def show_cards(self, player, cards_ids):
        self.events.add(
                event.ShowCards(player, self.card_pool.cards_by_ids(cards_ids)))

    def damage(self, victim, damage, category):
        self.events.add(event.Damage(victim, damage, category))

    def query_player_by_id(self, player_id):
        pass

    def query_player_by_token(self, player_token):
        pass
