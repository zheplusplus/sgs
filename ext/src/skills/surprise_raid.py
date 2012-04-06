import core.src.card as card
import ext.src.common_checking as checking
import ext.src.hint_common as hints
from ext.src.sleevecards import sabotage
from ext.src.wrappers import invoke_on_success

SKILL = 'surprise raid'

def add_to(player):
    player.using_hint_char.append(black_as_sabotage_using_hint)

def black_as_sabotage_using_hint(hint, game_control, user, interfaces):
    @invoke_on_success(user, SKILL)
    def to_sabotage(gc, args):
        checking.only_one_card_of_color(gc.cards_by_ids(args['use']),
                                        card.BLACK)
        return sabotage.sabotage_check(gc, args)
    interfaces[SKILL] = to_sabotage
    cards = filter(lambda c: c.color() == card.BLACK,
                   game_control.player_cards_at(user, 'all'))
    targets = sabotage.sabotage_targets(game_control, user)
    if len(targets) == 0:
        return
    hints.add_method_to(hint, SKILL,
                        hints.join_req(hints.fixed_card_count(cards, 1),
                                       hints.fixed_target_count(targets, 1)))
