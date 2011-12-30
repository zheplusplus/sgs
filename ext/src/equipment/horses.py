import core.src.card as card

def equip_positive_to(player, game_control, horse_card):
    player.equip(game_control, horse_card, '-1 horse', remove_positive_from)
    player.cw_positive_dist_mod += 1
    player.ccw_positive_dist_mod += 1

def remove_positive_from(game_control, player, equipped_card):
    player.cw_positive_dist_mod -= 1
    player.ccw_positive_dist_mod -= 1

def equip_passive_to(player, game_control, horse_card):
    player.equip(game_control, horse_card, '+1 horse', remove_passive_from)
    player.cw_passive_dist_mod += 1
    player.ccw_passive_dist_mod += 1

def remove_passive_from(game_control, player, equipped_card):
    player.cw_passive_dist_mod -= 1
    player.ccw_passive_dist_mod -= 1

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
