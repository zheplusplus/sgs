def forbid_target_self(source, target):
    if source == target:
        raise ValueError('forbid target self')

def forbid_target_no_card(target, game_control):
    if not game_control.player_has_cards(target):
        raise ValueError('forbid target no card')
