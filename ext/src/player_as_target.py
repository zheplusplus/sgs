import sleevecards.fire_attack as fire_attack
import sleevecards.duel as duel
import sleevecards.sabotage as sabotage

def target_mapping():
    return {
               'fire attack': fire_attack.as_target,
               'duel': duel.as_target,
               'sabotage': sabotage.as_target,
           }
