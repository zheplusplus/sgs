from hashlib import sha256
import time

import core.src.ret_code as ret_code
from ext.src import game_init

class GameRoom:
    def __init__(self):
        self.players_tokens = []
        self.host = ''
        self.game_started = False

    def check_token(self, request_body):
        token = request_body['token']
        return {
            'code': ret_code.OK,
            'in': 1 if token in self.players_tokens else 0,
        }

    def player_exit(self, request_body):
        token = request_body['token']
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
        token = request_body['token'] if 'token' in request_body else ''
        return {
            'code': ret_code.OK,
            'players': len(self.players_tokens),
            'started': 1 if self.game_started else 0,
            'host': 1 if self.host == token else 0,
        }

    def add_player(self, request_body):
        self._check_game_not_started()
        if 8 == len(self.players_tokens):
            raise ValueError('room full')
        token = sha256(str(request_body) + str(time.time())).hexdigest()
        if len(self.players_tokens) == 0:
            self.host = token
        self.players_tokens.append(token)
        return {
            'code': ret_code.OK,
            'token': token,
        }

    def start(self, request_body):
        self._check_game_not_started()
        token = request_body['token']
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
        return self.gc.hint(request_body['token'])

    def get_events(self, args):
        self._check_game_started()
        return {
            'code': 200,
            'events': self.gc.get_events(args['token'],
                                         args['previous event id']),
        }

    def player_act(self, request_body):
        return self.gc.player_act(request_body)

game_room = GameRoom()
