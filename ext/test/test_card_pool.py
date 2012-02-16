from ext.src import card_pool

for c in card_pool.all_cards():
    if c.rank < 0 or 13 <= c.rank:
        raise ValueError('Unexpected rank: %d of card suit=%d name=%s' % (
                            c.rank, c.suit, c.name))
    if c.suit <= 0 or 4 < c.suit:
        raise ValueError('Unexpected suit: %d of card rank=%d name=%s' % (
                            c.suit, c.rank, c.name))
