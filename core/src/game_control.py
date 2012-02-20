from card import Card
import ret_code
import event

class GameControl:
    def __init__(self, event_list, card_pool, players_control, action_stack):
        self.events = event_list
        self.players_control = players_control
        self.card_pool = card_pool
        self.action_stack = action_stack

    def game_init(self, players):
        self._add_event(event.GameInit(players))

    def select_character(self, player, character):
        self._add_event(event.SelectCharacter(player, character))

    def start(self):
        self.players_control.start(self)
        self.players_control.current_player().round(self)

    def next_round(self):
        self.players_control.next_player()
        self.players_control.current_player().round(self)

    def get_events(self, token, prev_event_id):
        return self.events.serialize(token, prev_event_id)

    def _add_event(self, event):
        self.events.add(event)

    def player_act(self, args):
        try:
            if not args['token'] in map(lambda p: p.token,
                                        self.action_stack.allowed_players()):
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
                       'reason': ret_code.BR_WRONG_ARG % e.message,
                   }

    def hint(self, token):
        return self.action_stack.hint(token)

    def push_frame(self, frame):
        self.action_stack.push(frame)

    def pop_frame(self):
        self.action_stack.pop()

    def deal_cards(self, player, cnt):
        cards = self.card_pool.deal(player, cnt)
        self._add_event(event.DrawCards(player, cards))
        return cards

    def discard_cards_by_ids(self, player, cards_ids):
        self.discard_cards(player, self.card_pool.cards_by_ids(cards_ids))

    def discard_cards(self, player, cards):
        self._add_event(event.DiscardCards(player, cards))
        self.recycle_cards(cards)

    def recycle_cards(self, cards):
        self.card_pool.discard(cards)

    def use_cards_for_players(self, user, targets_ids, action, cards):
        self._add_event(event.UseCardsForPlayers(user, targets_ids, action,
                                                 cards))
        self.card_pool.discard(cards)

    def show_cards(self, player, cards_ids):
        self._add_event(event.ShowCards(player,
                                        self.card_pool.cards_by_ids(cards_ids)))

    def play_cards(self, player, cards):
        self._add_event(event.PlayCards(player, cards))
        self.card_pool.discard(cards)

    def equip(self, player, card, region):
        self._add_event(event.Equip(player, card, region))

    def unequip(self, player, card, region):
        self._add_event(event.Unequip(player, card, region))
        return card

    def private_cards_transfer(self, source, target, cards):
        self._add_event(event.PrivateCardsTransfer(source, target, cards))
        self.card_pool.cards_transfer(target, cards)

    def public_cards_transfer(self, source, target, cards):
        self._add_event(event.PublicCardsTransfer(source, target, cards))
        self.card_pool.cards_transfer(target, cards)

    def _decrease_player_vigor(self, player, point, on_brink_of_death,
                               after_brink_of_death):
        player.vigor -= point
        if player.vigor <= 0:
            on_brink_of_death(lambda: self.players_control.try_rescuing(
                                            self, player, after_brink_of_death))

    def damage(self, damage):
        self._add_event(event.Damage(damage.victim, damage.point,
                                     damage.category))
        self._decrease_player_vigor(damage.victim, damage.point,
                                    lambda f: damage.interrupt(f),
                                    damage.resume)

    def vigor_lost(self, player, point):
        self._add_event(event.VigorLost(player, point))
        self._decrease_player_vigor(player, point, lambda f: f(), lambda: None)

    def vigor_regain(self, player, point):
        if player.max_vigor < player.vigor + point:
            point = player.max_vigor - player.vigor
        if 0 < point:
            self._add_event(event.VigorRegain(player, point))
            player.vigor += point

    def kill(self, player):
        self._add_event(event.PlayerKilled(player))
        self.players_control.kill(player)
        self.card_pool.recycle_cards_of_player(player)

    def cards_by_ids(self, cards_ids):
        return self.card_pool.cards_by_ids(cards_ids)

    def player_by_id(self, player_id):
        return self.players_control.get_by_id(player_id)

    def player_by_token(self, player_token):
        return self.players_control.get_by_token(player_token)

    def distance_between(self, source, target):
        return self.players_control.distance_between(source, target)

    def player_has_cards(self, player):
        return self.card_pool.player_has_cards(player)

    def player_has_cards_at(self, player, region):
        return self.card_pool.player_has_cards_at(player, region)

    def player_cards_at(self, player, region):
        return self.card_pool.player_cards_at(player, region)

    def player_cards_count_at(self, player, region):
        return self.card_pool.player_cards_count_at(player, region)

    def random_pick_cards(self, player, count):
        return self.card_pool.random_pick_cards(player, count)
