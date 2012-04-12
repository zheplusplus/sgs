def range_filter(gc, user, action, players):
    return filter(lambda p: gc.distance_between(user, p) <= user.range(action),
                  players)

def target_filter(action, user, players):
    return filter(lambda p: p.targeted(user, action), players)

def fix_target_action(targets):
    if 0 < len(targets):
        return fixed_target_count(targets, 1)
    return forbid()

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

def fixed_card_count(cards, count):
    return {
        'require': ['fix card count'],
        'cards': map(lambda c: c.card_id, cards),
        'card count': count,
    }

def min_card_count(cards, count):
    return {
        'require': ['min card count'],
        'cards': map(lambda c: c.card_id, cards),
        'card count': count,
    }

def fixed_target_count(targets, count):
    return {
        'require': ['fix target'],
        'targets': map(lambda p: p.player_id, targets),
        'target count': count,
    }

def implicit_target():
    return { 'require': ['implicit target'] }

def forbid():
    return { 'require': ['forbid'] }

def basic_cards_hint():
    return {
        'card': dict(),
        'methods': dict(),
        'abort': 'disallow',
    }

def join_req(lhs, rhs):
    both = dict(lhs.items() + rhs.items())
    both['require'] = lhs['require'] + rhs['require']
    return both

def add_method_to(hint, method, detail):
    hint['methods'][method] = detail
    return hint

def allow_abort(hint):
    hint['abort'] = 'allow'
    return hint

def filter_empty(hint):
    if len(hint['card']) == 0:
        del hint['card']
    if len(hint['methods']) == 0:
        del hint['methods']
    return hint
