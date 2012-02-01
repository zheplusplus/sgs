class Player:
    def __init__(self, token, max_vigor, responses_dict):
        self.token = token
        self.alive = True
        self.max_vigor = max_vigor
        self.vigor = max_vigor
        self.responses = responses_dict
        self.equipment = dict()
        self.cw_positive_dist_mod = 0
        self.ccw_positive_dist_mod = 0
        self.cw_passive_dist_mod = 0
        self.ccw_passive_dist_mod = 0

    def draw_cards(self, game_control, cnt):
        game_control.deal_cards(self, cnt)

    def response_frame(self, action, game_control, on_result):
        return self.responses[action].response(game_control, self, on_result)

    def equip(self, game_control, card, region, on_remove):
        if region in self.equipment:
            game_control.recycle_cards([self.unequip(game_control, region)])
        card.set_region(region)
        def rm_func():
            on_remove(game_control, self, card)
            return card
        self.equipment[region] = rm_func
        game_control.equip(self, card, region)

    def unequip_check(self, game_control, region):
        if not region in self.equipment:
            raise ValueError('no such equipment')
        return self.unequip(game_control, region)

    def unequip(self, game_control, region):
        return game_control.unequip(self, self.equipment[region](), region)
