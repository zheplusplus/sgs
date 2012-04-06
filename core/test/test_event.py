import core.src.event as event
import core.src.card as card

from test_common import *
import fake_player

cards = [
            card.Card(0, 'slash', 1, card.SPADE),
            card.Card(1, 'dodge', 2, card.HEART),
            card.Card(2, 'slash', 3, card.SPADE),
        ]
player0 = fake_player.Player(91)
player0.player_id = 0
player1 = fake_player.Player(112)
player1.player_id = 1

evt = event.GameInit([player1, player0])
assert_eq({
    91: 0,
    112: 1,
    'type': 'GameInit',
}, evt.as_log())
assert_eq({
    'players': 2,
    'position': 0,
    'type': 'GameInit',
}, evt.serialize(player0.token))
assert_eq({
    'players': 2,
    'position': 1,
    'type': 'GameInit',
}, evt.serialize(player1.token))

evt = event.DrawCards(player0, cards)
assert_eq({
    'type': 'DrawCards',
    'player': player0.player_id,
    'draw': [
        {
            'id': 0,
            'name': 'slash',
            'rank': 1,
            'suit': 1,
            'region': 'cardpool',
        },
        {
            'id': 1,
            'name': 'dodge',
            'rank': 2,
            'suit': 2,
            'region': 'cardpool',
        },
        {
            'id': 2,
            'name': 'slash',
            'rank': 3,
            'suit': 1,
            'region': 'cardpool',
        },
    ],
}, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq({
              'type': 'DrawCards',
              'player': player0.player_id,
              'draw': 3,
          }, evt.serialize(player1.token))

for c in cards: c.set_region('onhand')
evt = event.DiscardCards(player0, cards)
for c in cards: c.set_region('cardpool')
assert_eq({
              'type': 'DiscardCards',
              'player': player0.player_id,
              'discard': [
                             {
                                 'id': 0,
                                 'name': 'slash',
                                 'rank': 1,
                                 'suit': 1,
                                 'region': 'onhand',
                             },
                             {
                                 'id': 1,
                                 'name': 'dodge',
                                 'rank': 2,
                                 'suit': 2,
                                 'region': 'onhand',
                             },
                             {
                                 'id': 2,
                                 'name': 'slash',
                                 'rank': 3,
                                 'suit': 1,
                                 'region': 'onhand',
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
                                 'region': 'onhand',
                             },
                             {
                                 'name': 'dodge',
                                 'rank': 2,
                                 'suit': 2,
                                 'region': 'onhand',
                             },
                             {
                                 'name': 'slash',
                                 'rank': 3,
                                 'suit': 1,
                                 'region': 'onhand',
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
            'region': 'cardpool',
        },
        {
            'id': 1,
            'name': 'dodge',
            'rank': 2,
            'suit': 2,
            'region': 'cardpool',
        },
        {
            'id': 2,
            'name': 'slash',
            'rank': 3,
            'suit': 1,
            'region': 'cardpool',
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
            'region': 'cardpool',
        },
        {
            'name': 'dodge',
            'rank': 2,
            'suit': 2,
            'region': 'cardpool',
        },
        {
            'name': 'slash',
            'rank': 3,
            'suit': 1,
            'region': 'cardpool',
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
                              'region': 'cardpool',
                          },
                          {
                              'id': 1,
                              'name': 'dodge',
                              'rank': 2,
                              'suit': 2,
                              'region': 'cardpool',
                          },
                          {
                              'id': 2,
                              'name': 'slash',
                              'rank': 3,
                              'suit': 1,
                              'region': 'cardpool',
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
                              'region': 'cardpool',
                          },
                          {
                              'name': 'dodge',
                              'rank': 2,
                              'suit': 2,
                              'region': 'cardpool',
                          },
                          {
                              'name': 'slash',
                              'rank': 3,
                              'suit': 1,
                              'region': 'cardpool',
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
                              'region': 'cardpool',
                          },
                          {
                              'name': 'dodge',
                              'rank': 2,
                              'suit': 2,
                              'region': 'cardpool',
                          },
                          {
                              'name': 'slash',
                              'rank': 3,
                              'suit': 1,
                              'region': 'cardpool',
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

evt = event.VigorLost(player0, 1)
assert_eq({
              'type': 'VigorLost',
              'player': player0.player_id,
              'point': 1,
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq(evt.as_log(), evt.serialize(player1.token))

evt = event.VigorRegain(player0, 1)
assert_eq({
              'type': 'VigorRegain',
              'player': player0.player_id,
              'point': 1,
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq(evt.as_log(), evt.serialize(player1.token))

evt = event.Invocation(player0, 'dragon heart')
assert_eq({
    'type': 'Invocation',
    'player': player0.player_id,
    'invoke': 'dragon heart',
}, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq(evt.as_log(), evt.serialize(player1.token))

equipment_card = card.Card(0, 'zhangba serpent spear', 12, card.SPADE)
evt = event.Equip(player0, equipment_card, 'weapon')
assert_eq({
              'player': player0.player_id,
              'region': 'weapon',
              'type': 'Equip',
              'equip': {
                           'id': 0,
                           'name': 'zhangba serpent spear',
                           'rank': 12,
                           'suit': 1,
                           'region': 'cardpool',
                       }
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq({
              'player': player0.player_id,
              'region': 'weapon',
              'type': 'Equip',
              'equip': {
                           'name': 'zhangba serpent spear',
                           'rank': 12,
                           'suit': 1,
                           'region': 'cardpool',
                       }
          }, evt.serialize(player1.token))

evt = event.Unequip(player0, equipment_card, 'weapon')
assert_eq({
              'player': player0.player_id,
              'region': 'weapon',
              'type': 'Unequip',
              'unequip': {
                             'id': 0,
                             'name': 'zhangba serpent spear',
                             'rank': 12,
                             'suit': 1,
                             'region': 'cardpool',
                         }
          }, evt.as_log())
assert_eq({
              'player': player0.player_id,
              'region': 'weapon',
              'type': 'Unequip',
              'unequip': {
                             'name': 'zhangba serpent spear',
                             'rank': 12,
                             'suit': 1,
                             'region': 'cardpool',
                         }
          }, evt.serialize(player0.token))
assert_eq(evt.serialize(player1.token), evt.serialize(player0.token))

player2 = fake_player.Player(1123)
player2.player_id = 2
evt = event.PrivateCardsTransfer(player0, player1, cards)
assert_eq({
              'type': 'PrivateCardsTransfer',
              'source': player0.player_id,
              'target': player1.player_id,
              'transfer': [
                              {
                                  'id': 0,
                                  'name': 'slash',
                                  'rank': 1,
                                  'suit': 1,
                                  'region': 'cardpool',
                              },
                              {
                                  'id': 1,
                                  'name': 'dodge',
                                  'rank': 2,
                                  'suit': 2,
                                  'region': 'cardpool',
                              },
                              {
                                  'id': 2,
                                  'name': 'slash',
                                  'rank': 3,
                                  'suit': 1,
                                  'region': 'cardpool',
                              },
                          ],
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq(evt.serialize(player0.token), evt.serialize(player1.token))
assert_eq({
              'type': 'PrivateCardsTransfer',
              'source': player0.player_id,
              'target': player1.player_id,
              'transfer': 3,
          }, evt.serialize(player2.token))

evt = event.PublicCardsTransfer(player0, player1, cards)
assert_eq({
              'type': 'PublicCardsTransfer',
              'source': player0.player_id,
              'target': player1.player_id,
              'transfer': [
                              {
                                  'id': 0,
                                  'name': 'slash',
                                  'rank': 1,
                                  'suit': 1,
                                  'region': 'cardpool',
                              },
                              {
                                  'id': 1,
                                  'name': 'dodge',
                                  'rank': 2,
                                  'suit': 2,
                                  'region': 'cardpool',
                              },
                              {
                                  'id': 2,
                                  'name': 'slash',
                                  'rank': 3,
                                  'suit': 1,
                                  'region': 'cardpool',
                              },
                          ],
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq(evt.serialize(player0.token), evt.serialize(player1.token))
assert_eq({
              'type': 'PublicCardsTransfer',
              'source': player0.player_id,
              'target': player1.player_id,
              'transfer': [
                              {
                                  'name': 'slash',
                                  'rank': 1,
                                  'suit': 1,
                                  'region': 'cardpool',
                              },
                              {
                                  'name': 'dodge',
                                  'rank': 2,
                                  'suit': 2,
                                  'region': 'cardpool',
                              },
                              {
                                  'name': 'slash',
                                  'rank': 3,
                                  'suit': 1,
                                  'region': 'cardpool',
                              },
                          ],
          }, evt.serialize(player2.token))

evt = event.PlayerKilled(player0)
assert_eq({
              'type': 'PlayerKilled',
              'player': player0.player_id,
          }, evt.as_log())
assert_eq(evt.as_log(), evt.serialize(player0.token))
assert_eq(evt.as_log(), evt.serialize(player1.token))
assert_eq(evt.as_log(), evt.serialize(player2.token))
