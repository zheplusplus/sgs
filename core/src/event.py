class Event:
    def serialize(self, player_token):
        return self.as_log()

    def as_log(self):
        return []

class EventList:
    events = []

    def __init__(self):
        self.events = []

    def serialize(self, token, prev_event_id):
        return reduce(lambda l, e: l + e.serialize(token)
                    , self.events[prev_event_id:], [])

    def as_log(self):
        return reduce(lambda l, e: l + e.as_log(), self.events, [])

    def add(self, event):
        self.events.append(event)

def cards_to_msg(cards, to_msg):
    return reduce(lambda l, c: l + [to_msg(c)], cards, [])

class DealCard(Event):
    player = None
    cards = []

    def __init__(self, player, cards):
        self.player = player
        self.cards = cards

    def serialize(self, player_token):
        if player_token == self.player.token:
            return self.as_log()
        return [{
            'player_id': self.player.player_id,
            'get': len(self.cards),
        }]

    def as_log(self):
        return [{
            'player_id': self.player.player_id,
            'get': cards_to_msg(self.cards, lambda c: {
                                                'id': c.card_id,
                                                'name': c.name,
                                                'rank': c.rank,
                                                'suit': c.suit,
                                            }),
        }]

class DiscardCard(Event):
    player = None
    cards = []

    def __init__(self, player, cards):
        self.player = player
        self.cards = cards

    def as_log(self):
        return [{
            'player_id': self.player.player_id,
            'discard': cards_to_msg(self.cards, lambda c: {
                                                    'name': c.name,
                                                    'rank': c.rank,
                                                    'suit': c.suit,
                                                }),
        }]
