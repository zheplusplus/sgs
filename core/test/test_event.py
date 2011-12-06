import core.src.event as event
import core.src.card as card

from test_common import *
import fake_player

cards = [
            card.Card(0, 'slash', 1, card.SPADE),
            card.Card(1, 'dodge', 2, card.HEART),
            card.Card(2, 'slash', 3, card.SPADE),
        ]
player0 = fake_player.Player(91, 29)
player1 = fake_player.Player(112, 1954)

evt = event.DealCards(player0, cards)
assert_eq({
              'type': 'DealCards',
              'player': player0.player_id,
              'get': [
                         {
                             'id': 0,
                             'name': 'slash',
                             'rank': 1,
                             'suit': 1,
                         },
                         {
                             'id': 1,
                             'name': 'dodge',
                             'rank': 2,
                             'suit': 2,
                         },
                         {
                             'id': 2,
                             'name': 'slash',
                             'rank': 3,
                             'suit': 1,
                         },
                     ],
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq({
              'type': 'DealCards',
              'player': player0.player_id,
              'get': 3,
          }, evt.serialize(player1.token))

evt = event.DiscardCards(player0, cards)
assert_eq({
              'type': 'DiscardCards',
              'player': player0.player_id,
              'discard': [
                             {
                                 'id': 0,
                                 'name': 'slash',
                                 'rank': 1,
                                 'suit': 1,
                             },
                             {
                                 'id': 1,
                                 'name': 'dodge',
                                 'rank': 2,
                                 'suit': 2,
                             },
                             {
                                 'id': 2,
                                 'name': 'slash',
                                 'rank': 3,
                                 'suit': 1,
                             },
                         ],
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq({
              'type': 'DiscardCards',
              'player': player0.player_id,
              'discard': [
                             {
                                 'name': 'slash',
                                 'rank': 1,
                                 'suit': 1,
                             },
                             {
                                 'name': 'dodge',
                                 'rank': 2,
                                 'suit': 2,
                             },
                             {
                                 'name': 'slash',
                                 'rank': 3,
                                 'suit': 1,
                             },
                         ],
          }, evt.serialize(player1.token))

evt = event.UseCardsForPlayers(player0, [player0.player_id, player1.player_id],
                               'test', cards)
assert_eq({
              'type': 'UseCardsForPlayers',
              'user': player0.player_id,
              'targets': [player0.player_id, player1.player_id],
              'action': 'test',
              'use': [
                         {
                             'id': 0,
                             'name': 'slash',
                             'rank': 1,
                             'suit': 1,
                         },
                         {
                             'id': 1,
                             'name': 'dodge',
                             'rank': 2,
                             'suit': 2,
                         },
                         {
                             'id': 2,
                             'name': 'slash',
                             'rank': 3,
                             'suit': 1,
                         },
                     ],
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq({
              'type': 'UseCardsForPlayers',
              'user': player0.player_id,
              'targets': [player0.player_id, player1.player_id],
              'action': 'test',
              'use': [
                         {
                             'name': 'slash',
                             'rank': 1,
                             'suit': 1,
                         },
                         {
                             'name': 'dodge',
                             'rank': 2,
                             'suit': 2,
                         },
                         {
                             'name': 'slash',
                             'rank': 3,
                             'suit': 1,
                         },
                     ],
          }, evt.serialize(player1.token))

evt = event.PlayCards(player0, cards)
assert_eq({
              'type': 'PlayCards',
              'player': player0.player_id,
              'play': [
                          {
                              'id': 0,
                              'name': 'slash',
                              'rank': 1,
                              'suit': 1,
                          },
                          {
                              'id': 1,
                              'name': 'dodge',
                              'rank': 2,
                              'suit': 2,
                          },
                          {
                              'id': 2,
                              'name': 'slash',
                              'rank': 3,
                              'suit': 1,
                          },
                      ],
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq({
              'type': 'PlayCards',
              'player': player0.player_id,
              'play': [
                          {
                              'name': 'slash',
                              'rank': 1,
                              'suit': 1,
                          },
                          {
                              'name': 'dodge',
                              'rank': 2,
                              'suit': 2,
                          },
                          {
                              'name': 'slash',
                              'rank': 3,
                              'suit': 1,
                          },
                      ],
          }, evt.serialize(player1.token))

evt = event.ShowCards(player0, cards)
assert_eq({
              'type': 'ShowCards',
              'player': player0.player_id,
              'show': [
                          {
                              'name': 'slash',
                              'rank': 1,
                              'suit': 1,
                          },
                          {
                              'name': 'dodge',
                              'rank': 2,
                              'suit': 2,
                          },
                          {
                              'name': 'slash',
                              'rank': 3,
                              'suit': 1,
                          },
                      ],
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq(evt.as_log(), evt.serialize(player1.token))

evt = event.Damage(player0, 1, 'normal')
assert_eq({
              'type': 'Damage',
              'victim': player0.player_id,
              'damage': 1,
              'category': 'normal',
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq(evt.as_log(), evt.serialize(player1.token))
