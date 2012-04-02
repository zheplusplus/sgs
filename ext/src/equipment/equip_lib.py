from ext.src.category_hierarchy import is_slash

def change_slash_range(f, r):
    return lambda action: r if is_slash(action) else f(action)

class Equipment:
    def __init__(self, player, card):
        self.player = player
        self.card = card

    def lost(self):
        self.off()
        return self.card

class EquipmentRestore:
    def __init__(self, player, region):
        self.__enter__ = lambda: None
        self.__exit__ = lambda etype, eobj, tb: None
        if region in player.equipment:
            e = player.equipment[region]
            self.__enter__ = lambda : e.off()
            self.__exit__ = lambda etype, eobj, tb: e.on()
