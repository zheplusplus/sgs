from core.src.game_control import GameControl
from core.src.event import EventList
from core.src.action_stack import ActionStack
import core.src.card as card
import core.src.ret_code as ret_code
from ext.src.players_control import PlayersControl
from ext.test.fake_player import Player

from test_common import *
import test_data

pc = PlayersControl()
gc = GameControl(EventList(), test_data.CardPool(test_data.gen_cards([
            test_data.CardInfo('-chitu', 5, card.HEART),
            test_data.CardInfo('-dawan', 13, card.SPADE),
            test_data.CardInfo('+jueying', 5, card.SPADE),
            test_data.CardInfo('slash', 1, card.CLUB),

            test_data.CardInfo('-zixing', 13, card.DIAMOND),
            test_data.CardInfo('+dilu', 5, card.CLUB),
            test_data.CardInfo('+hualiu', 5, card.DIAMOND),
            test_data.CardInfo('duel', 2, card.SPADE),

            test_data.CardInfo('sabotage', 3, card.HEART),
            test_data.CardInfo('dodge', 4, card.DIAMOND),
            test_data.CardInfo('slash', 5, card.DIAMOND),
            test_data.CardInfo('slash', 6, card.SPADE),

            test_data.CardInfo('+zhuahuangfeidian', 5, card.HEART),
            test_data.CardInfo('zhangba serpent spear', 7, card.HEART),

            test_data.CardInfo('slash', 8, card.SPADE),
            test_data.CardInfo('slash', 9, card.HEART),
     ])), pc, ActionStack())
players = [Player(19, 4), Player(91, 4), Player(1729, 4)]
map(lambda p: pc.add_player(p), players)
gc.start()

assert_eq(0, gc.distance_between(players[0], players[0]))
assert_eq(0, gc.distance_between(players[1], players[1]))
assert_eq(0, gc.distance_between(players[2], players[2]))
assert_eq(1, gc.distance_between(players[0], players[1]))
assert_eq(1, gc.distance_between(players[0], players[2]))
assert_eq(1, gc.distance_between(players[1], players[0]))
assert_eq(1, gc.distance_between(players[2], players[0]))

last_event_id = len(gc.get_events(players[0].token, 0)) # until getting cards

# cards:
# name                  | rank | id | suit

# -chitu                | 5    | 0  | HEART   <- equip
# -dawan                | 13   | 1  | SPADE
# +jueying              | 5    | 2  | SPADE
# slash                 | 1    | 3  | CLUB
# +zhuahuangfeidian     | 5    | 12 | HEART
# zhangba serpent spear | 7    | 13 | HEART

# -zixing               | 13   | 4  | DIAMOND
# +dilu                 | 5    | 5  | CLUB
# +hualiu               | 5    | 6  | DIAMOND
# duel                  | 2    | 7  | SPADE

# sabotage              | 3    | 8  | HEART
# dodge                 | 4    | 9  | DIAMOND
# slash                 | 5    | 10 | DIAMOND
# slash                 | 6    | 11 | SPADE
result = gc.player_act({
                          'token': players[0].token,
                          'action': 'equip',
                          'use': [0],
                      })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('-chitu', event['equip']['name'])
    assert_eq(5, event['equip']['rank'])
    assert_eq(card.HEART, event['equip']['suit'])
    assert_eq(0, event['equip']['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('-chitu', event['equip']['name'])
    assert_eq(5, event['equip']['rank'])
    assert_eq(card.HEART, event['equip']['suit'])
p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(p1_events, p2_events)
last_event_id += 1

assert_eq(-1, gc.distance_between(players[0], players[0]))
assert_eq(0, gc.distance_between(players[1], players[1]))
assert_eq(0, gc.distance_between(players[2], players[2]))
assert_eq(0, gc.distance_between(players[0], players[1]))
assert_eq(0, gc.distance_between(players[0], players[2]))
assert_eq(1, gc.distance_between(players[1], players[0]))
assert_eq(1, gc.distance_between(players[1], players[2]))
assert_eq(1, gc.distance_between(players[2], players[0]))
assert_eq(1, gc.distance_between(players[2], players[1]))

# cards:
# name                  | rank | id | suit

# -chitu                | 5    | 0  | HEART   <- equipped
# -dawan                | 13   | 1  | SPADE
# +jueying              | 5    | 2  | SPADE   <- equip
# slash                 | 1    | 3  | CLUB
# +zhuahuangfeidian     | 5    | 12 | HEART
# zhangba serpent spear | 7    | 13 | HEART

# -zixing               | 13   | 4  | DIAMOND
# +dilu                 | 5    | 5  | CLUB
# +hualiu               | 5    | 6  | DIAMOND
# duel                  | 2    | 7  | SPADE

# sabotage              | 3    | 8  | HEART
# dodge                 | 4    | 9  | DIAMOND
# slash                 | 5    | 10 | DIAMOND
# slash                 | 6    | 11 | SPADE
result = gc.player_act({
                          'token': players[0].token,
                          'action': 'equip',
                          'use': [2],
                      })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(1, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('+jueying', event['equip']['name'])
    assert_eq(5, event['equip']['rank'])
    assert_eq(card.SPADE, event['equip']['suit'])
    assert_eq(2, event['equip']['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(1, len(p1_events))
if True: # just indent for a nice appearance
    event = p1_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('+jueying', event['equip']['name'])
    assert_eq(5, event['equip']['rank'])
    assert_eq(card.SPADE, event['equip']['suit'])
p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(p1_events, p2_events)
last_event_id += 1

assert_eq(0, gc.distance_between(players[0], players[0]))
assert_eq(0, gc.distance_between(players[1], players[1]))
assert_eq(0, gc.distance_between(players[2], players[2]))
assert_eq(0, gc.distance_between(players[0], players[1]))
assert_eq(0, gc.distance_between(players[0], players[2]))
assert_eq(2, gc.distance_between(players[1], players[0]))
assert_eq(1, gc.distance_between(players[1], players[2]))
assert_eq(2, gc.distance_between(players[2], players[0]))
assert_eq(1, gc.distance_between(players[2], players[1]))

# cards:
# name                  | rank | id | suit

# -chitu                | 5    | 0  | HEART   <- replaced
# -dawan                | 13   | 1  | SPADE   <- equip
# +jueying              | 5    | 2  | SPADE   <- equipped
# slash                 | 1    | 3  | CLUB
# +zhuahuangfeidian     | 5    | 12 | HEART
# zhangba serpent spear | 7    | 13 | HEART

# -zixing               | 13   | 4  | DIAMOND
# +dilu                 | 5    | 5  | CLUB
# +hualiu               | 5    | 6  | DIAMOND
# duel                  | 2    | 7  | SPADE

# sabotage              | 3    | 8  | HEART
# dodge                 | 4    | 9  | DIAMOND
# slash                 | 5    | 10 | DIAMOND
# slash                 | 6    | 11 | SPADE
result = gc.player_act({
                          'token': players[0].token,
                          'action': 'equip',
                          'use': [1],
                      })
assert_eq(ret_code.OK, result['code'])
p0_events = gc.get_events(players[0].token, last_event_id)
assert_eq(2, len(p0_events))
if True: # just indent for a nice appearance
    event = p0_events[0]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('-1 horse', event['region'])
    assert_eq('-chitu', event['unequip']['name'])
    assert_eq(5, event['unequip']['rank'])
    assert_eq(card.HEART, event['unequip']['suit'])
    event = p0_events[1]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('-dawan', event['equip']['name'])
    assert_eq(13, event['equip']['rank'])
    assert_eq(card.SPADE, event['equip']['suit'])
    assert_eq(1, event['equip']['id'])
p1_events = gc.get_events(players[1].token, last_event_id)
assert_eq(2, len(p1_events))
if True: # just indent for a nice appearance
    assert_eq(p0_events[0], p1_events[0])
    event = p1_events[1]
    assert_eq(players[0].player_id, event['player'])
    assert_eq('-dawan', event['equip']['name'])
    assert_eq(13, event['equip']['rank'])
    assert_eq(card.SPADE, event['equip']['suit'])
p2_events = gc.get_events(players[2].token, last_event_id)
assert_eq(p1_events, p2_events)
last_event_id += 1

assert_eq(0, gc.distance_between(players[0], players[0]))
assert_eq(0, gc.distance_between(players[1], players[1]))
assert_eq(0, gc.distance_between(players[2], players[2]))
assert_eq(0, gc.distance_between(players[0], players[1]))
assert_eq(0, gc.distance_between(players[0], players[2]))
assert_eq(2, gc.distance_between(players[1], players[0]))
assert_eq(1, gc.distance_between(players[1], players[2]))
assert_eq(2, gc.distance_between(players[2], players[0]))
assert_eq(1, gc.distance_between(players[2], players[1]))

# cards:
# name                  | rank | id | suit

# -dawan                | 13   | 1  | SPADE   <- equipped
# +jueying              | 5    | 2  | SPADE   <- equipped
# slash                 | 1    | 3  | CLUB
# +zhuahuangfeidian     | 5    | 12 | HEART
# zhangba serpent spear | 7    | 13 | HEART

# -zixing               | 13   | 4  | DIAMOND
# +dilu                 | 5    | 5  | CLUB
# +hualiu               | 5    | 6  | DIAMOND
# duel                  | 2    | 7  | SPADE

# sabotage              | 3    | 8  | HEART
# dodge                 | 4    | 9  | DIAMOND
# slash                 | 5    | 10 | DIAMOND
# slash                 | 6    | 11 | SPADE
result = gc.player_act({
                          'token': players[0].token,
                          'action': 'give up',
                      })
assert_eq(ret_code.OK, result['code'])

assert_eq(0, gc.distance_between(players[0], players[0]))
assert_eq(0, gc.distance_between(players[1], players[1]))
assert_eq(0, gc.distance_between(players[2], players[2]))
assert_eq(0, gc.distance_between(players[0], players[1]))
assert_eq(0, gc.distance_between(players[0], players[2]))
assert_eq(2, gc.distance_between(players[1], players[0]))
assert_eq(1, gc.distance_between(players[1], players[2]))
assert_eq(2, gc.distance_between(players[2], players[0]))
assert_eq(1, gc.distance_between(players[2], players[1]))

# cards:
# name                  | rank | id | suit

# -dawan                | 13   | 1  | SPADE   <- equipped
# +jueying              | 5    | 2  | SPADE   <- equipped
# slash                 | 1    | 3  | CLUB

# -zixing               | 13   | 4  | DIAMOND <- equip
# +dilu                 | 5    | 5  | CLUB
# +hualiu               | 5    | 6  | DIAMOND
# duel                  | 2    | 7  | SPADE
# slash                 | 7    | 14 | SPADE
# slash                 | 8    | 15 | HEART

# sabotage              | 3    | 8  | HEART
# dodge                 | 4    | 9  | DIAMOND
# slash                 | 5    | 10 | DIAMOND
# slash                 | 6    | 11 | SPADE
result = gc.player_act({
                          'token': players[1].token,
                          'action': 'equip',
                          'use': [4],
                      })
assert_eq(ret_code.OK, result['code'])

assert_eq(0, gc.distance_between(players[0], players[0]))
assert_eq(-1, gc.distance_between(players[1], players[1]))
assert_eq(0, gc.distance_between(players[2], players[2]))
assert_eq(0, gc.distance_between(players[0], players[1]))
assert_eq(0, gc.distance_between(players[0], players[2]))
assert_eq(1, gc.distance_between(players[1], players[0]))
assert_eq(0, gc.distance_between(players[1], players[2]))
assert_eq(2, gc.distance_between(players[2], players[0]))
assert_eq(1, gc.distance_between(players[2], players[1]))

# cards:
# name                  | rank | id | suit

# -dawan                | 13   | 1  | SPADE   <- equipped
# +jueying              | 5    | 2  | SPADE   <- equipped
# slash                 | 1    | 3  | CLUB

# -zixing               | 13   | 4  | DIAMOND <- equipped
# +dilu                 | 5    | 5  | CLUB    <- equip
# +hualiu               | 5    | 6  | DIAMOND
# duel                  | 2    | 7  | SPADE
# slash                 | 7    | 14 | SPADE
# slash                 | 8    | 15 | HEART

# sabotage              | 3    | 8  | HEART
# dodge                 | 4    | 9  | DIAMOND
# slash                 | 5    | 10 | DIAMOND
# slash                 | 6    | 11 | SPADE
result = gc.player_act({
                          'token': players[1].token,
                          'action': 'equip',
                          'use': [5],
                      })
assert_eq(ret_code.OK, result['code'])

assert_eq(0, gc.distance_between(players[0], players[0]))
assert_eq(0, gc.distance_between(players[1], players[1]))
assert_eq(0, gc.distance_between(players[2], players[2]))
assert_eq(1, gc.distance_between(players[0], players[1]))
assert_eq(0, gc.distance_between(players[0], players[2]))
assert_eq(1, gc.distance_between(players[1], players[0]))
assert_eq(0, gc.distance_between(players[1], players[2]))
assert_eq(2, gc.distance_between(players[2], players[0]))
assert_eq(2, gc.distance_between(players[2], players[1]))

# cards:
# name                  | rank | id | suit

# -dawan                | 13   | 1  | SPADE   <- equipped
# +jueying              | 5    | 2  | SPADE   <- equipped
# slash                 | 1    | 3  | CLUB

# -zixing               | 13   | 4  | DIAMOND <- equipped
# +dilu                 | 5    | 5  | CLUB    <- replaced
# +hualiu               | 5    | 6  | DIAMOND <- equip
# duel                  | 2    | 7  | SPADE
# slash                 | 7    | 14 | SPADE
# slash                 | 8    | 15 | HEART

# sabotage              | 3    | 8  | HEART
# dodge                 | 4    | 9  | DIAMOND
# slash                 | 5    | 10 | DIAMOND
# slash                 | 6    | 11 | SPADE
result = gc.player_act({
                          'token': players[1].token,
                          'action': 'equip',
                          'use': [6],
                      })
assert_eq(ret_code.OK, result['code'])

assert_eq(0, gc.distance_between(players[0], players[0]))
assert_eq(0, gc.distance_between(players[1], players[1]))
assert_eq(0, gc.distance_between(players[2], players[2]))
assert_eq(1, gc.distance_between(players[0], players[1]))
assert_eq(0, gc.distance_between(players[0], players[2]))
assert_eq(1, gc.distance_between(players[1], players[0]))
assert_eq(0, gc.distance_between(players[1], players[2]))
assert_eq(2, gc.distance_between(players[2], players[0]))
assert_eq(2, gc.distance_between(players[2], players[1]))
