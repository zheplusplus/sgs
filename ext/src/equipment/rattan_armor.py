import core.src.card as card
import ext.src.wrappers as wrappers

def equip_to(player, game_control, rattan_armor_card):
    player.equip(game_control, rattan_armor_card, 'armor', remove_from)
    player.before_damaged_equip = one_more_fire_damage

def remove_from(game_control, player, equipped_card):
    player.before_damaged_equip = lambda p, d, gc: None

@wrappers.alive
@wrappers.as_damage_victim
def one_more_fire_damage(player, damage, game_control):
    if damage.category == 'fire':
        damage.point += 1

def imported(equip_dict):
    equip_dict['rattan armor'] = equip_to
