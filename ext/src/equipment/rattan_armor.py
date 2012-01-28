import core.src.card as card

def equip_to(player, game_control, rattan_armor_card):
    player.equip(game_control, rattan_armor_card, 'armor', remove_from)
    player.actions_before_damaged['equipment']['trigger'] = one_more_fire_damage

def remove_from(game_control, player, equipped_card):
    player.actions_before_damaged['equipment']['trigger'] = lambda d, gc: None

def one_more_fire_damage(damage, gc):
    if damage.category == 'fire':
        damage.point += 1

def imported(equip_dict):
    equip_dict['rattan armor'] = equip_to
