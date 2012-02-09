from ext.src.player import Player as ExtPlayer

class Player(ExtPlayer):
    def __init__(self, token, max_vigor):
        ExtPlayer.__init__(self, token)
        self.max_vigor = max_vigor
        self.vigor = max_vigor
