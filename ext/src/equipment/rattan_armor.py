import core.src.card as card
import ext.src.wrappers as wrappers

EQUIP_NAME = 'rattan armor'

def equip_to(player, game_control, rattan_armor_card):
    player.equip(game_control, rattan_armor_card, 'armor', remove_from)
    player.before_damaged_equip = one_more_fire_damage
    player.slashed_equip = _immunity_to_slash

def remove_from(game_control, player, equipped_card):
    player.before_damaged_equip = lambda p, d, gc: None
    player.slashed_equip = lambda player, slash, gc: None

@wrappers.alive
@wrappers.as_damage_victim
def one_more_fire_damage(player, damage, gc):
    if damage.category == 'fire':
        gc.invoke(player, EQUIP_NAME)
        damage.point += 1

@wrappers.as_target
def _immunity_to_slash(player, slashing, gc):
    if slashing.action == 'slash':
        gc.invoke(player, EQUIP_NAME)
        slashing.interrupt(lambda: None)

def imported(equip_dict):
    equip_dict[EQUIP_NAME] = equip_to
