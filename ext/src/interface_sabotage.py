from core.src.action_frames as frames

def sabotage(game_control, args):
    targets_ids = args['target']
    if 1 != len(targets_ids):
        return {
                   'code': ret_code.BAD_REQUEST,
                   'reason': ret_code.BR_WRONG_ARG,
               }
    cards = game_control.cards_by_ids(args['cards'])
    if 1 != len(cards) or 'sabotage' != cards[0].name:
        return {
                   'code': ret_code.BAD_REQUEST,
                   'reason': ret_code.BR_WRONG_ARG,
               }
    user = game_control.player_by_token(args['token'])
    target = game_control.player_by_id(targets_ids[0])
    game_control.use_cards_for_players(user, targets_ids, args['action'], cards)
    on_result = lambda gc, a: sabotage_handout_slash(game_control, user, target, a)
    game_control.push_frame(frames.HandoutCards(game_control, target, 
                                                lambda c: len(c) == 1 and c.name == 'slash',
                                                on_result)
    
def sabotage_handout_slash(game_control, player, target, args):
    hanout_name = game_control.cards_by_ids(args['handout'])[0].name
    def handout_filter(cards_ids):
        cards = game_control.cards_by_ids(cards_ids)
        if len(cards) == 0:
            return True
        return len(cards) == 1 and cards[0].name == 'slash'
    game_control.push_frame(
            frames.HandoutCards(game_control, player, handout_filter,
                                lambda gc, a: fire_attack_done(gc, target, a)))
    
def sabotage_done(game_control, target, args):
    game_control.damage(target, 1, 'sabotage')