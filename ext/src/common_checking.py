def forbid_target_self(source, target):
    if source == target:
        raise ValueError('forbid target self')

def forbid_target_no_card(target, game_control):
    if not game_control.player_has_cards(target):
        raise ValueError('forbid target no card')

def only_one_target(targets):
    if len(targets) != 1:
        raise ValueError('wrong targets count')

def only_one_card_named_as(cards, expected_name):
    if len(cards) != 1 or expected_name != cards[0].name:
        raise ValueError('wrong cards')
