from core.src.action_frames import AcceptMessage
import ext.src.wrappers as wrappers
import ext.src.hint_common as hints
from equip_lib import change_slash_range, Equipment

EQUIP_NAME = 'vermilion feather fan'

class VermilionFeatherFan(Equipment):
    def __init__(self, player, card):
        Equipment.__init__(self, player, card)

    def on(self):
        self.player.range_equip = change_slash_range(self.player.range_equip, 4)
        self.player.slashing_equip = _ask_fan

    def off(self):
        self.player.range_equip = lambda action: self.player.base_ranges[action]
        self.player.slashing_equip = lambda player, slash, gc: None

def equip_to(player, game_control, card):
    player.equip(game_control, 'weapon', VermilionFeatherFan(player, card))

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
