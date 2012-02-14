import random

from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
from core.src.action_frames import FrameBase
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.src.player import Player
from ext.src import characters
from ext.src.card_pool import CardPool

class _SelectCharacter(FrameBase):
    def __init__(self, game_control, players, token_to_characters, on_result):
        FrameBase.__init__(self, game_control, on_result)
        self.token_to_players = { p.token: p for p in players }
        self.token_to_characters = token_to_characters
        self.selected = dict()

    def allowed_players(self):
        return self.token_to_players.values()

    def react(self, args):
        select = args['select']
        token = args['token']
        if not select in self.token_to_characters[token]:
            raise ValueError('select wrong character')
        character = self.token_to_characters[token][select]
        character.select(self.token_to_players[token])
        self.selected[token] = character
        del self.token_to_characters[token]
        del self.token_to_players[token]
        if len(self.token_to_characters) == 0:
            return self.done(self.selected)
        return { 'code': ret_code.OK }

    def hint(self, token):
        base_hint = FrameBase.hint(self, token)
        if token in self.token_to_characters:
            base_hint['candidate'] = self.token_to_characters[token].keys()
        return base_hint

def characters_select_dict(chars):
    return { c.name: c for c in chars }

def statuses_mode(players_tokens):
    if len(players_tokens) < 2:
        raise ValueError('too few players, need at least 2')
    if 8 < len(players_tokens):
        raise ValueError('too much players, need at most 8')
    random.shuffle(players_tokens)

    players = [Player(t) for t in players_tokens]
    pc = PlayersControl()
    for p in players: pc.add_player(p)

    gc = GameControl(EventList(), CardPool.create(), pc, ActionStack())
    gc.game_init(players)

    host = players[0]
    others = players[1:]
    def after_host_selected(gc, r):
        gc.select_character(host, r[host.token])
        gc.push_frame(_SelectCharacter(
                        gc, others,
                        { p.token: characters_select_dict([characters.GUO_JIA])
                                for p in others },
                        all_selected))
    def all_selected(gc, r):
        for p in others:
            gc.select_character(p, r[p.token])
        gc.start()
    gc.push_frame(_SelectCharacter(
                   gc, [host],
                   { host.token: characters_select_dict([characters.GUO_JIA]) },
                   after_host_selected))
    return gc
