def valid_target(source, target, action):
    if not target.targeted(source, action):
        raise ValueError('invalid target')

def forbid_target_self(source, target):
    if source == target:
        raise ValueError('forbid target self')

def forbid_target_no_card(target, game_control):
    if not game_control.player_has_cards(target):
        raise ValueError('forbid target no card')

def forbid_target_no_card_on_hand(target, game_control):
    if not game_control.player_has_cards_at(target, 'onhand'):
        raise ValueError('forbid target no card')

def target_damaged(target):
    if target.vigor == target.max_vigor:
        raise ValueError('target not damaged')

def only_one_target(targets):
    if len(targets) != 1:
        raise ValueError('wrong targets count')

def only_one_card_named_as(cards, expected_name):
    if len(cards) != 1 or expected_name != cards[0].name():
        raise ValueError('wrong cards')

def only_one_card_of_color(cards, expected_color):
    if len(cards) != 1 or expected_color != cards[0].color():
        raise ValueError('wrong cards')

def only_one_card_of_suit(cards, expected_suit):
    if len(cards) != 1 or expected_suit != cards[0].suit():
        raise ValueError('wrong cards')

def only_one_card_of_category(cards, category):
    if len(cards) != 1 or not category(cards[0].name()):
        raise ValueError('wrong cards')

def cards_region(cards, expected_region):
    for c in cards:
        if c.region != expected_region:
            raise ValueError('wrong region')

def within_range(game_control, source, target, action):
    if source.range(action) < game_control.distance_between(source, target):
        raise ValueError('out of range')
