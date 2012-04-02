class Player:
    def __init__(self, token):
        self.token = token
        self.alive = True
        self.equipment = dict()
        self.cw_positive_dist_mod = 0
        self.ccw_positive_dist_mod = 0
        self.cw_passive_dist_mod = 0
        self.ccw_passive_dist_mod = 0

    def equip(self, game_control, region, equipment):
        if region in self.equipment:
            unequipped = self.unequip(game_control, region)
            unequipped.set_region('unequipped')
            game_control.recycle_cards([unequipped])
        equipment.card.set_region(region)
        self.equipment[region] = equipment
        game_control.equip(self, equipment.card, region)
        equipment.on()

    def unequip_check(self, game_control, region):
        if not region in self.equipment:
            raise ValueError('no such equipment')
        return self.unequip(game_control, region)

    def unequip(self, game_control, region):
        card = game_control.unequip(self, self.equipment[region].lost(), region)
        del self.equipment[region]
        return card

    def all_regions(self, game_control):
        regions = []
        if game_control.player_has_cards_at(self, 'onhand'):
            regions = ['onhand']
        regions.extend(list(self.equipment))
        return regions
