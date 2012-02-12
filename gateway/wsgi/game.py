from hashlib import sha256
import time

from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.src.player import Player
import ext.src.card_pool as card_pool
import ext.src.skills.bequeathed_strategy as bequeathed_strategy
from gateway.wsgi import log

class GameRoom:
    def __init__(self):
        self.players_tokens = []
        self.response = self.before_game_start

    def game_status(self, path, request_body):
        if path == '/info/status':
            return {
                       'code': ret_code.OK,
                       'players': len(self.players_tokens),
                       'started': 0 if self.response == self.before_game_start
                                    else 1,
                   }
        return { 'code': 404 }

    def before_game_start(self, path, request_body):
        if path == '/ctrl/start':
            return self.start(request_body)
        if path == '/ctrl/add':
            return self.add_player(time.time(), request_body)
        return self.game_status(path, request_body)

    def after_game_start(self, path, request_body):
        try:
            if path == '/act':
                return self.player_act(eval(request_body, dict(), dict()))
            if path == '/info/events':
                return {
                           'code': 200,
                           'events': self.get_events(eval(request_body,
                                                     dict(), dict()))
                       }
            if path == '/info/hint':
                hint = self.gc.hint()
                hint['code'] = 200
                return hint
            return self.game_status(path, request_body)
        except (NameError, SyntaxError), e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': 'syntax error',
                   }

    def add_player(self, time, name):
        token = sha256(name + str(time)).hexdigest()
        log.i('Add player:token=' + token)
        if len(self.players_tokens) == 0:
            log.i('Be host:token=' + token)
            self.host = token
        self.players_tokens.append(token)
        return {
                   'code': ret_code.OK,
                   'token': token,
               }

    def start(self, token):
        if len(self.players_tokens) < 2:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': 'Need at least 2 players',
                   }
        log.i('Request start:token=' + token)
        if token != self.host:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': 'Not the host',
                   }
        pc = PlayersControl()
        self.gc = GameControl(EventList(),
                              card_pool.CardPool(card_pool.all_cards()),
                              pc, ActionStack())
        for token in self.players_tokens: pc.add_player(Player(token, 4))
        self.gc.start()
        self.response = self.after_game_start
        return { 'code': ret_code.OK }

    def get_events(self, args):
        try:
            return self.gc.get_events(args['token'], args['previous event id'])
        except KeyError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_MISSING_ARG % e.message,
                   }

    def player_act(self, args):
        return self.gc.player_act(args)

game_room = GameRoom()
