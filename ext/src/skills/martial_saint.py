import core.src.card as card
import ext.src.common_checking as checking
from ext.src import hint_common
from ext.src.basiccards import slash

SKILL = 'martial saint'

def add_to(player):
    player.responses['slash'].add_method(SKILL, red_as_slash_response, hint)
    player.using_hint_char.append(red_as_slash_using_hint)

def red_as_slash_response(cards):
    checking.only_one_card_of_color(cards, card.RED)

def red_as_slash_using_hint(hint, game_control, user):
    def to_slash(gc, args):
        checking.cards_region(cards, 'onhand')
        red_as_slash_response(gc.cards_by_ids(args['use']))
        return slash.slash(gc, args)
    if 'slash' in user.using_hint_dict:
        user.using_interfaces[SKILL] = to_slash
        cards = filter(lambda c: c.color() == card.RED,
                       game_control.player_cards_at(user, 'onhand'))
        targets = slash.slash_target(game_control, user, cards)
        if targets['type'] == 'forbid':
            return
        hint['methods'][SKILL] = {
            'require': ['fix card count', 'fix target'],
            'targets': targets['targets'],
            'target count': 1,
            'cards': map(lambda c: c.card_id, cards),
            'card count': 1,
        }
    elif SKILL in user.using_interfaces:
        del user.using_interfaces[SKILL]

def hint(game_control, player):
    return hint_common.one_card_filter(game_control, player, SKILL,
                                       lambda c: c.color() == card.RED)
