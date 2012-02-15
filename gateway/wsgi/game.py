from hashlib import sha256
import time

import core.src.ret_code as ret_code
from ext.src import game_init

class GameRoom:
    def __init__(self):
        self.players_tokens = []
        self.host = ''
        self.handlers = {
                            '/ctrl/add': self.add_player,
                            '/ctrl/exit': self.player_exit,
                            '/ctrl/start': self.start,
                            '/info/status': self.game_status,
                            '/info/events': self.get_events,
                            '/info/hint': self.get_hint,
                            '/info/checktoken': self.check_token,
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
                       'reason': 'Syntax error: %s' % e.message,
                   }

    def check_token(self, request_body):
        return {
                   'code': ret_code.OK,
                   'in': 1 if request_body in self.players_tokens else 0,
               }

    def player_exit(self, token):
        if not token in self.players_tokens:
            raise ValueError('Not joined in')
        self.players_tokens.remove(token)
        if token == self.host and 0 < len(self.players_tokens):
            self.host = self.players_tokens[0]
        return { 'code': 200 }

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
        if 8 == len(self.players_tokens):
            raise ValueError('room full')
        token = sha256(request_body + str(time.time())).hexdigest()
        if len(self.players_tokens) == 0:
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
        if token != self.host:
            return {
                       'code': ret_code.BAD_REQUEST,
                       'reason': 'Not the host',
                   }
        self.game_started = True
        self.gc = game_init.statuses_mode(self.players_tokens)
        return { 'code': ret_code.OK }

    def get_hint(self, request_body):
        self._check_game_started()
        return self.gc.hint(request_body)

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
