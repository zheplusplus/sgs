from sleevecards.fire_attack import fire_attack
from sleevecards.duel import duel
from sleevecards.sabotage import sabotage
from equipment import equip

def get_using_cards_interface_map():
    return {
               'fire attack': fire_attack,
               'duel': duel,
               'sabotage': sabotage,
               'equip': equip.interface,
           }
