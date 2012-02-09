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

class GameInit(Event):
    def __init__(self, players):
        self.players_map = { p.token: p.player_id for p in players }

    def _as_log(self):
        return self.players_map.copy()

    def _serialize(self, token):
        s = { 'players': len(self.players_map) }
        if token in self.players_map:
            s['position'] = self.players_map[token]
        return s

class SelectCharacter(Event):
    def __init__(self, player, character):
        self.player = player
        self.character = character

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'character': self.character.name,
            'max vigor': self.player.max_vigor,
        }

def card_to_msg(c):
    return {
        'name': c.name,
        'rank': c.rank,
        'suit': c.suit,
        'region': c.region,
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

def add_region_formatter(formatter):
    def f(card):
        msg = formatter(card)
        msg['region'] = card.region
        return msg
    return f

class CardStub:
    @staticmethod
    def stub(cards):
        return map(CardStub, cards)

    def __init__(self, card):
        self.card_id = card.card_id
        self.name = card.base_name
        self.rank = card.base_rank
        self.suit = card.base_suit
        self.region = card.region

class DrawCards(Event):
    def __init__(self, player, cards):
        self.player = player
        self.cards = CardStub.stub(cards)

    def _serialize(self, player_token):
        if player_token == self.player.token:
            return self.as_log()
        return {
            'player': self.player.player_id,
            'draw': len(self.cards),
        }

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'draw': cards_to_msg_include_id(self.cards),
        }

class DiscardCards(Event):
    def __init__(self, player, cards):
        self.player = player
        self.cards = CardStub.stub(cards)

    def _serialize(self, player_token):
        if player_token == self.player.token:
            return self.as_log()
        return {
            'player': self.player.player_id,
            'discard': make_cards_msg(self.cards,
                                      add_region_formatter(card_to_msg)),
        }

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'discard': make_cards_msg(
                            self.cards,
                            add_region_formatter(card_to_msg_include_id)),
        }

class CardsTransferBase(Event):
    def _as_log(self):
        return {
            'source': self.source.player_id,
            'target': self.target.player_id,
            'transfer': make_cards_msg(
                                self.cards,
                                add_region_formatter(card_to_msg_include_id)),
        }

class PrivateCardsTransfer(CardsTransferBase):
    def __init__(self, source, target, cards):
        self.source = source
        self.target = target
        self.cards = CardStub.stub(cards)

    def _serialize(self, player_token):
        if player_token in (self.source.token, self.target.token):
            return self.as_log()
        return {
            'source': self.source.player_id,
            'target': self.target.player_id,
            'transfer': len(self.cards),
        }

class PublicCardsTransfer(CardsTransferBase):
    def __init__(self, source, target, cards):
        self.source = source
        self.target = target
        self.cards = CardStub.stub(cards)

    def _serialize(self, player_token):
        if player_token in (self.source.token, self.target.token):
            return self.as_log()
        return {
            'source': self.source.player_id,
            'target': self.target.player_id,
            'transfer': make_cards_msg(self.cards,
                                       add_region_formatter(card_to_msg)),
        }

class UseCardsForPlayers(Event):
    def __init__(self, user, targets_ids, action, cards):
        self.user = user
        self.targets_ids = targets_ids
        self.action = action
        self.cards = CardStub.stub(cards)

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
        self.cards = CardStub.stub(cards)

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
        self.cards = CardStub.stub(cards)

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

class VigorLost(Event):
    def __init__(self, player, point):
        self.player = player
        self.point = point

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'point': self.point,
        }

class VigorRegain(Event):
    def __init__(self, player, point):
        self.player = player
        self.point = point

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'point': self.point,
        }

class Equip(Event):
    def __init__(self, player, card, region):
        self.player = player
        self.card = CardStub(card)
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

class Unequip(Event):
    def __init__(self, player, card, region):
        self.player = player
        self.card = CardStub(card)
        self.region = region

    def _serialize(self, player_token):
        return {
            'player': self.player.player_id,
            'unequip': cards_to_msg([self.card])[0],
            'region': self.region,
        }

    def _as_log(self):
        return {
            'player': self.player.player_id,
            'unequip': cards_to_msg_include_id([self.card])[0],
            'region': self.region,
        }

class PlayerKilled(Event):
    def __init__(self, player):
        self.player = player

    def _as_log(self):
        return {
            'player': self.player.player_id,
        }
