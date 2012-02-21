from sleevecards.fire_attack import fire_attack_target
from sleevecards.duel import duel_target
from sleevecards.sabotage import sabotage_target
from sleevecards.steal import steal_target

def player_as_target(card_name):
    DICT = {
               'fire attack': fire_attack_target,
               'duel': duel_target,
               'sabotage': sabotage_target,
               'steal': steal_target,
           }
    if card_name in DICT:
        return DICT[card_name]
    return lambda gc, u, c: { 'type': 'forbid' }
