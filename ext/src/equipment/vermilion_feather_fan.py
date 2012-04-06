from core.src.action_frames import AcceptMessage
import ext.src.wrappers as wrappers
import ext.src.hint_common as hints
from equip_lib import change_slash_range

EQUIP_NAME = 'vermilion feather fan'

def equip_to(player, game_control, card):
    player.equip(game_control, card, 'weapon', remove_from)
    player.range_equip = change_slash_range(player.range_equip, 4)
    player.slashing_equip = _ask_fan

def remove_from(game_control, player, equipped_card):
    player.slashing_equip = lambda player, slash, gc: None

@wrappers.as_user
def _ask_fan(player, slashing, gc):
    if slashing.action == 'slash':
        slashing.interrupt(lambda: gc.push_frame(_AskFan(gc, slashing)))

class _AskFan(AcceptMessage):
    def __init__(self, game_control, slashing):
        hint = hints.filter_empty(hints.allow_abort(hints.add_method_to(
                        hints.basic_cards_hint(), EQUIP_NAME, hints.forbid())))
        AcceptMessage.__init__(self, game_control, [slashing.user], 'discard',
                               hint, self.on_message)
        self.slashing = slashing

    def on_message(self, args):
        if args['method'] != 'abort':
            self.game_control.invoke(self.players[0], EQUIP_NAME)
            self.slashing.action = 'fire slash'

    def destructed(self):
        self.slashing.resume()

def imported(equip_dict):
    equip_dict[EQUIP_NAME] = equip_to
