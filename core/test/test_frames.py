from test_common import *
import fake_player

from core.src.game_control import GameControl
from core.src.event import EventList
import core.src.card as card
import core.src.ret_code as ret_code
import core.src.action_frames as frames

player = fake_player.Player(10, 0)
cards = [
            card.Card(0, 'slash', 1, card.SPADE),
            card.Card(1, 'slash', 2, card.SPADE),
            card.Card(2, 'slash', 3, card.SPADE),
            card.Card(3, 'slash', 4, card.SPADE),
        ]
cards[0].set_owner(player)
cards[2].set_owner(player)
cards_of_player = [0, 2]
cards_free = [1, 3]

def make_gc():
    class FakeCardPool:
        def cards_by_ids(self, ids):
            return map(lambda i: cards[i], ids)
    class FakeActionStack:
        def pop(self):
            pass
    return GameControl(EventList(), FakeCardPool(), None, FakeActionStack())

result = None
def on_result_f(gc, a):
    global result
    result = a

def fake_action(gc, a):
    global result
    result = a
    return { 'code': ret_code.OK }

use_cards_frm = frames.UseCards(make_gc(), player, { 'test': fake_action },
                                on_result_f)
assert_eq([player], use_cards_frm.allowed_players())
response = use_cards_frm.react({
                                   'token': 10,
                                   'action': 'test',
                                   'cards': [0],
                               })
assert_eq(ret_code.OK, response['code'])
assert_eq({
              'token': 10,
              'action': 'test',
              'cards': [0],
          }, result)
result = None
try:
    response = use_cards_frm.react({
                                       'token': 10,
                                       'cards': [0],
                                   })
    assert False
except KeyError, e:
    assert_eq('action', e.message)
assert_eq(None, result)
response = use_cards_frm.react({
                                   'token': 10,
                                   'action': 'no such action',
                                   'cards': [0],
                               })
assert_eq({
              'code': 400,
              'reason': ret_code.BR_INCORRECT_INTERFACE,
          }, response)
assert_eq(None, result)
try:
    response = use_cards_frm.react({
                                       'token': 10,
                                       'action': 'test',
                                       'cards': [1],
                                   })
    assert False
except ValueError:
    pass
assert_eq(None, result)

def show_card_check(cards):
    if len(cards) != 1:
        raise ValueError('need one card only')
show_card_frm = frames.ShowCards(make_gc(), player, show_card_check,
                                 on_result_f)
assert_eq([player], show_card_frm.allowed_players())
response = show_card_frm.react({
                                   'token': 10,
                                   'show': [0],
                               })
assert_eq(ret_code.OK, response['code'])
assert_eq({
              'token': 10,
              'show': [0],
          }, result)
result = None
try:
    response = show_card_frm.react({ 'token': 10 })
    assert False
except KeyError, e:
    assert_eq('show', e.message)
assert_eq(None, result)

try:
    response = show_card_frm.react({
                                       'token': 10,
                                       'show': [0, 2],
                                   })
    assert False
except ValueError, e:
    assert_eq('need one card only', e.message)
assert_eq(None, result)

try:
    response = show_card_frm.react({
                                       'token': 10,
                                       'show': [],
                                   })
    assert False
except ValueError, e:
    assert_eq('need one card only', e.message)
assert_eq(None, result)

try:
    response = show_card_frm.react({
                                       'token': 10,
                                       'show': [1],
                                   })
    assert False
except ValueError:
    pass
assert_eq(None, result)

def discard_card_check(cards):
    if 1 < len(cards):
        raise ValueError('number of cards more than 1')
discard_card_frm = frames.DiscardCards(make_gc(), player, discard_card_check,
                                       on_result_f)
assert_eq([player], discard_card_frm.allowed_players())
response = discard_card_frm.react({
                                      'token': 10,
                                      'discard': [0],
                                  })
assert_eq(ret_code.OK, response['code'])
assert_eq({
              'token': 10,
              'discard': [0],
          }, result)
result = None
response = discard_card_frm.react({
                                      'token': 10,
                                      'discard': [],
                                  })
assert_eq(ret_code.OK, response['code'])
assert_eq({
              'token': 10,
              'discard': [],
          }, result)
result = None
try:
    response = discard_card_frm.react({ 'token': 10 })
    assert False
except KeyError, e:
    assert_eq('discard', e.message)
assert_eq(None, result)

try:
    response = discard_card_frm.react({
                                          'token': 10,
                                          'discard': [0, 2],
                                      })
    assert False
except ValueError, e:
    assert_eq('number of cards more than 1', e.message)
assert_eq(None, result)

try:
    response = discard_card_frm.react({
                                          'token': 10,
                                          'discard': [1],
                                      })
    assert False
except ValueError:
    pass
assert_eq(None, result)

def on_message(args):
    if 'bing' in args:
        raise ValueError('bang')
acc_msg_frm = frames.AcceptMessage(make_gc(), [player], on_message, on_result_f)
response = acc_msg_frm.react({ 'bang': 'bing' })
assert_eq({ 'bang': 'bing' }, result)
assert_eq(ret_code.OK, response['code'])
result = None
try:
    response = acc_msg_frm.react({ 'bing': 'bang' })
    assert False
except ValueError:
    pass
assert_eq(None, result)
