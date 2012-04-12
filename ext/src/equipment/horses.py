import core.src.card as card
from equip_lib import Equipment

class PositiveHorse(Equipment):
    def __init__(self, player, card):
        Equipment.__init__(self, player, card)

    def on(self):
        self.player.cw_positive_dist_mod += 1
        self.player.ccw_positive_dist_mod += 1

    def off(self):
        self.player.cw_positive_dist_mod -= 1
        self.player.ccw_positive_dist_mod -= 1

def equip_positive_to(player, gc, horse_card):
    player.equip(gc, '-1 horse', PositiveHorse(player, horse_card))

class PassiveHorse(Equipment):
    def __init__(self, player, card):
        Equipment.__init__(self, player, card)

    def on(self):
        self.player.cw_passive_dist_mod += 1
        self.player.ccw_passive_dist_mod += 1

    def off(self):
        self.player.cw_passive_dist_mod -= 1
        self.player.ccw_passive_dist_mod -= 1

def equip_passive_to(player, gc, horse_card):
    player.equip(gc, '+1 horse', PassiveHorse(player, horse_card))

def imported(equip_dict):
    POSITIVE_HORSE_NAMES = (
        '-chitu',
        '-dawan',
        '-zixing',
    )
    for h in POSITIVE_HORSE_NAMES:
        equip_dict[h] = equip_positive_to

    PASSIVE_HORSE_NAMES = (
        '+dilu',
        '+hualiu',
        '+jueying',
        '+zhuahuangfeidian',
    )
    for h in PASSIVE_HORSE_NAMES:
        equip_dict[h] = equip_passive_to
