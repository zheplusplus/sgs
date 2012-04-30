import json
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

import core.src.ret_code as ret_code
import game

class Index(RequestHandler):
    def get(self):
        self.render('static/index.html')

class SocketHandlerBase(WebSocketHandler):
    def send(self, message):
        self.write_message(json.dumps(message))

    def on_message(self, message):
        self.recv(json.loads(message))

class IncomeHandler(SocketHandlerBase):
    def handle(self, message):
        path = message['controller']
        if not path in self.handlers():
            return { 'code': 404 }
        return self.handlers()[path](message)

class StatusHandler(IncomeHandler):
    def handlers(self):
        return {
            'status': game.game_room.game_status,
            'events': game.game_room.get_events,
            'hint': game.game_room.get_hint,
            'checktoken': game.game_room.check_token,
        }

    def recv(self, message):
        self.send(self.handle(message))

class ActionHandler(IncomeHandler):
    def handlers(self):
        return {
            'add': game.game_room.add_player,
            'exit': game.game_room.player_exit,
            'start': game.game_room.start,
            'act': game.game_room.player_act,
        }

    def recv(self, message):
        result = self.handle(message)
        if result['code'] == ret_code.OK:
            Commander.send({ 'action': 'update' })
        self.send(result)

class Commander(SocketHandlerBase):
    clients = set()

    @staticmethod
    def send(message):
        for c in Commander.clients:
            SocketHandlerBase.send(c, message)

    def open(self):
        Commander.clients.add(self)

    def on_close(self):
        Commander.clients.remove(self)
