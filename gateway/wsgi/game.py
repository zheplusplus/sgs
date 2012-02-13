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
        self.host = ''
        self.handlers = {
                            '/ctrl/add': self.add_player,
                            '/ctrl/start': self.start,
                            '/info/status': self.game_status,
                            '/info/events': self.get_events,
                            '/info/hint': self.get_hint,
                            '/act': self.player_act,
                        }
        self.game_started = False

    def response(self, path, request_body):
        if not path in self.handlers:
            return { 'code': 404 }
        try:
            return self.handlers[path](request_body)
        except ValueError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': e.message,
                   }
        except KeyError, e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': ret_code.BR_MISSING_ARG % e.message,
                   }
        except (NameError, SyntaxError), e:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': e.message,
                   }

    def _check_game_not_started(self):
        if self.game_started:
            raise ValueError('Game started')

    def _check_game_started(self):
        if not self.game_started:
            raise ValueError('Game not started')

    def game_status(self, request_body):
        return {
                   'code': ret_code.OK,
                   'players': len(self.players_tokens),
                   'started': 1 if self.game_started else 0,
                   'host': 1 if self.host == request_body else 0,
               }

    def add_player(self, request_body):
        self._check_game_not_started()
        token = sha256(request_body + str(time.time())).hexdigest()
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
        self._check_game_not_started()
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
        self.game_started = True
        return { 'code': ret_code.OK }

    def get_hint(self, req):
        self._check_game_started()
        hint = self.gc.hint()
        hint['code'] = 200
        return hint

    def get_events(self, request_body):
        self._check_game_started()
        args = eval(request_body, dict(), dict())
        return {
                   'code': 200,
                   'events': self.gc.get_events(args['token'],
                                                args['previous event id']),
               }

    def player_act(self, request_body):
        return self.gc.player_act(eval(request_body, dict(), dict()))

game_room = GameRoom()
