from ext.src import card_pool

for c in card_pool.all_cards():
    if c.base_rank < 0 or 13 <= c.base_rank:
        raise ValueError('Unexpected rank: %d of card suit=%d name=%s' % (
                            c.base_rank, c.base_suit, c.base_name))
    if c.base_suit <= 0 or 4 < c.base_suit:
        raise ValueError('Unexpected suit: %d of card rank=%d name=%s' % (
                            c.base_suit, c.base_rank, c.base_name))
