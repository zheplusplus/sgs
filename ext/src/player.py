from core.src.player import Player as CorePlayer
import player_response as response
import frames
import characters
import category_hierarchy as category

START_DRAW = 4
ROUND_DRAW = 2

class Player(CorePlayer):
    def __init__(self, token):
        CorePlayer.__init__(self, token)
        self.responses = {
            'slash': response.ToCardCategory('slash', category.is_slash),
            'peach': response.ToCertainCard('peach'),
            'dodge': response.ToCertainCard('dodge'),
        }
        self.base_ranges = {
            'steal': 1,
            'slash': 1,
        }

        self.range_equip = lambda action: self.base_ranges[action]
        self.range_char = lambda action: self.range_equip(action)
        self.card_suit_equip = lambda card: card.base_suit
        self.card_suit_char = lambda card: self.card_suit_equip(card)
        self.card_name_equip = lambda card: card.base_name
        self.card_name_char = lambda card: self.card_name_equip(card)
        self.targeted_equip = lambda source, me, action: True
        self.targeted_char = lambda source, me, action: True

        self.using_hint_char = []
        self.using_hint_equip = []

        do_nothing = lambda player, flow, game_control: None

        self.cards_used_char = do_nothing
        self.cards_used_equip = do_nothing

        self.slashing_char = do_nothing
        self.slashing_equip = do_nothing
        self.slashed_char = do_nothing
        self.slashed_equip = do_nothing

        self.before_damaging_equip = do_nothing
        self.before_damaging_char = do_nothing
        self.after_damaging_equip = do_nothing
        self.after_damaging_char = do_nothing
        self.before_damaged_equip = do_nothing
        self.before_damaged_char = do_nothing
        self.after_damaged_equip = do_nothing
        self.after_damaged_char = do_nothing
        self.computing_before_damaging = []
        self.computing_before_damaged = []

    def start(self, game_control):
        game_control.deal_cards(self, START_DRAW)

    def round(self, game_control):
        self.drawing_cards_stage(game_control)
        self.using_cards_stage(game_control)

    def drawing_cards_stage(self, game_control):
        game_control.deal_cards(self, ROUND_DRAW)

    def using_cards_stage(self, game_control):
        game_control.push_frame(frames.UseCards(game_control, self))

    def discard_count(self, game_control):
        return game_control.player_cards_count_at(self, 'onhand') - self.vigor

    def discarding_cards_stage(self, game_control):
        if self.alive and 0 < self.discard_count(game_control):
            game_control.push_frame(frames.DiscardCards(game_control, self))
        else:
            game_control.next_round()

    def response_frame(self, action, game_control):
        return self.responses[action].response(game_control, self)

    def using_hint(self):
        return self.using_hint_char + self.using_hint_equip

    def range(self, action):
        return self.range_char(action)

    def card_suit(self, card):
        return self.card_suit_char(card)

    def card_name(self, card):
        return self.card_name_char(card)

    def targeted(self, source, action):
        return self.targeted_char(source, self, action)

    def add_computing_before_damaging(self, f):
        self.computing_before_damaging.append(lambda d, gc: f(self, d, gc))

    def add_computing_before_damaged(self, f):
        self.computing_before_damaged.append(lambda d, gc: f(self, d, gc))
