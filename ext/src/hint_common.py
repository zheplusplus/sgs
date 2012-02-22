def target_filter(action, user, all_players, card):
    return filter(lambda p: p.target_filter(user, action, card), all_players)

def fix_target_action(candidates):
    if 0 < len(candidates):
        return {
                   'type': 'fix target',
                   'count': 1,
                   'candidates': map(lambda p: p.player_id, candidates),
               }
    return { 'type': 'forbid' }

def one_card_filter(game_control, player, name, card_traits):
    cards = game_control.player_cards_at(player, 'cards')
    cards = filter(card_traits, cards)
    return {
               name: {
                   'require': ['count', 'candidates'],
                   'count': 1,
                   'candidates': map(lambda c: c.card_id, cards),
               }
           }
