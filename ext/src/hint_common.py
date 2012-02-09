def range_filter(gc, user, action, candidates):
    return filter(lambda p: gc.distance_between(user, p) <= user.range(action),
                  candidates)

def target_filter(action, user, all_players, card):
    return filter(lambda p: p.targeted(user, action, card), all_players)

def fix_target_action(targets):
    if 0 < len(targets):
        return {
            'type': 'fix target',
            'target count': 1,
            'targets': map(lambda p: p.player_id, targets),
        }
    return { 'type': 'forbid' }

def one_card_filter(game_control, player, name, card_filter):
    cards = game_control.player_cards_at(player, 'all')
    cards = filter(card_filter, cards)
    return {
        name: {
            'require': ['fix card count'],
            'card count': 1,
            'cards': map(lambda c: c.card_id, cards),
        }
    }
