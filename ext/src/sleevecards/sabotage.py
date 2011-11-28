import ext.src.target_checking_common as checking

def as_target(source, target, game_control):
    checking.forbid_target_no_card(target, game_control)
    checking.forbid_target_self(source, target)
    pass

def sabotage():
    pass
