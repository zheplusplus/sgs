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

def cards_to_msg(cards):
    return reduce(lambda l, c: l + [{
                                       'name': c.name,
                                       'rank': c.rank,
                                       'suit': c.suit,
                                   }], cards, [])

def cards_to_msg_include_id(cards):
    return reduce(lambda l, c: l + [{
                                       'id': c.card_id,
                                       'name': c.name,
                                       'rank': c.rank,
                                       'suit': c.suit,
                                   }], cards, [])

class DealCards(Event):
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
            'get': cards_to_msg_include_id(self.cards),
        }]

class DiscardCards(Event):
    player = None
    cards = []

    def __init__(self, player, cards):
        self.player = player
        self.cards = cards

    def as_log(self):
        return [{
            'player_id': self.player.player_id,
            'discard': cards_to_msg(self.cards),
        }]

class UseCards(Event):
    user = None
    target = None
    action = ''
    cards = []

    def __init__(self, user, target, action, cards):
        self.user = user
        self.target = target
        self.action = action
        self.cards = cards

    def as_log(self):
        return [{
            'user': self.user.player_id,
            'target': self.target.player_id,
            'action': self.action,
            'use': cards_to_msg(self.cards),
        }]

class ShowCards(Event):
    player = None
    cards = []

    def __init__(self, player, cards):
        self.player = player
        self.cards = cards

    def as_log(self):
        return [{
            'player_id': self.player.player_id,
            'show': cards_to_msg(self.cards),
        }]

class Damage(Event):
    victim = None
    damage = 0
    category = ''

    def __init__(self, victim, damage, category='normal'):
        self.victim = victim
        self.damage = damage
        self.category = category

    def as_log(self):
        return [{
            'victim': self.victim.player_id,
            'damage': self.damage,
            'category': self.category,
        }]
