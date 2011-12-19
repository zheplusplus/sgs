class Event:
    def _add_type(self, data):
        data['type'] = self.__class__.__name__
        return data

    def as_log(self):
        return self._add_type(self._as_log())

    def serialize(self, player_token):
        return self._add_type(self._serialize(player_token))

    def _serialize(self, player_token):
        return self._as_log()

class EventList:
    def __init__(self):
        self.events = []

    def serialize(self, token, prev_event_id):
        return reduce(lambda l, e: l + [e.serialize(token)]
                    , self.events[prev_event_id:], [])

    def as_log(self):
        return reduce(lambda l, e: l + [e.as_log()], self.events, [])

    def add(self, event):
        self.events.append(event)

def card_to_msg(c):
    return {
               'name': c.name,
               'rank': c.rank,
               'suit': c.suit,
           }

def card_to_msg_include_id(c):
    msg = card_to_msg(c)
    msg['id'] = c.card_id
    return msg

def make_cards_msg(cards, formatter):
    return reduce(lambda l, c: l + [formatter(c)], cards, [])

def cards_to_msg(cards):
    return make_cards_msg(cards, card_to_msg)

def cards_to_msg_include_id(cards):
    return make_cards_msg(cards, card_to_msg_include_id)

class DealCards(Event):
    def __init__(self, player, cards):
        self.player = player
        self.cards = cards

    def _serialize(self, player_token):
        if player_token == self.player.token:
            return self.as_log()
        return {
            'player': self.player.player_id,
            'get': len(self.cards),
        }

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'get': cards_to_msg_include_id(self.cards),
        }

class DiscardCards(Event):
    class CardInfo:
        def __init__(self, card_id, name, rank, suit, region):
            self.card_id = card_id
            self.name = name
            self.rank = rank
            self.suit = suit
            self.region = region

    def __init__(self, player, cards):
        self.player = player
        self.cards = [DiscardCards.CardInfo(c.card_id, c.name, c.rank, c.suit,
                                            c.region) for c in cards]

    def _serialize(self, player_token):
        if player_token == self.player.token:
            return self.as_log()
        return {
            'player': self.player.player_id,
            'discard': make_cards_msg(self.cards,
                                      self._add_region_formatter(card_to_msg)),
        }

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'discard': make_cards_msg(
                            self.cards,
                            self._add_region_formatter(card_to_msg_include_id)),
        }

    def _add_region_formatter(self, formatter):
        def f(card):
            msg = formatter(card)
            msg['region'] = card.region
            return msg
        return f

class UseCardsForPlayers(Event):
    def __init__(self, user, targets_ids, action, cards):
        self.user = user
        self.targets_ids = targets_ids
        self.action = action
        self.cards = cards

    def _serialize(self, player_token):
        if player_token == self.user.token:
            return self.as_log()
        return {
            'user': self.user.player_id,
            'targets': self.targets_ids,
            'action': self.action,
            'use': cards_to_msg(self.cards),
        }

    def _as_log(self):
        return {
            'user': self.user.player_id,
            'targets': self.targets_ids,
            'action': self.action,
            'use': cards_to_msg_include_id(self.cards),
        }

class PlayCards(Event):
    def __init__(self, player, cards):
        self.player = player
        self.cards = cards

    def _serialize(self, player_token):
        if player_token == self.player.token:
            return self.as_log()
        return {
            'player': self.player.player_id,
            'play': cards_to_msg(self.cards),
        }

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'play': cards_to_msg_include_id(self.cards),
        }

class ShowCards(Event):
    def __init__(self, player, cards):
        self.player = player
        self.cards = cards

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'show': cards_to_msg(self.cards),
        }

class Damage(Event):
    def __init__(self, victim, damage, category):
        self.victim = victim
        self.damage = damage
        self.category = category

    def _as_log(self):
        return {
            'victim': self.victim.player_id,
            'damage': self.damage,
            'category': self.category,
        }

class Equip(Event):
    def __init__(self, player, card, region):
        self.player = player
        self.card = card
        self.region = region

    def _serialize(self, player_token):
        if player_token == self.player.token:
            return self.as_log()
        return {
            'player': self.player.player_id,
            'equip': cards_to_msg([self.card])[0],
            'region': self.region,
        }

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'equip': cards_to_msg_include_id([self.card])[0],
            'region': self.region,
        }
