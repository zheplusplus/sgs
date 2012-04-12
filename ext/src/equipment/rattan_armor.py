import core.src.card as card
import ext.src.wrappers as wrappers
from equip_lib import Equipment

EQUIP_NAME = 'rattan armor'

class RattanArmor(Equipment):
    def __init__(self, player, card):
        Equipment.__init__(self, player, card)

    def on(self):
        self.player.before_damaged_equip = one_more_fire_damage
        self.player.slashed_equip = _immunity_to_slash

    def off(self):
        self.player.before_damaged_equip = lambda p, d, gc: None
        self.player.slashed_equip = lambda player, slash, gc: None

def equip_to(player, gc, rattan_armor_card):
    player.equip(gc, 'armor', RattanArmor(player, rattan_armor_card))

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
