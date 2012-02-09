from ext.src.category_hierarchy import is_sleevecards

def add_to(player):
    def prodigy(f):
        return lambda action: 65535 if is_sleevecards(action) else f(action)
    player.range_char = prodigy(player.range_char)
