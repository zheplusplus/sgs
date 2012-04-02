def is_slash(name):
    return name in ['slash', 'thunder slash', 'fire slash']

def is_sleevecards(name):
    return is_time_sleevecards(name) or is_imm_sleevecards(name)

def is_time_sleevecards(name):
    return False

def is_imm_sleevecards(name):
    return name in ['steal', 'sabotage', 'duel', 'arson attack']
