function SGS_EventParser() {
    function buildEvent(detail) {
        function Card(detail) {
            if (!('id' in detail)) {
                detail['id'] = -1;
            }
            if (!('region' in detail)) {
                detail['region'] = 'cards';
            }
            this.id = detail['id'];
            this.name = detail['name'];
            this.rank = detail['rank'];
            this.suit = detail['suit'];
            this.region = detail['region'];
        }
        function buildCards(detail) {
            var result = new Array();
            for (i = 0; i < detail.length; ++i) {
                result.push(new Card(detail[i]));
            }
            return result;
        }
        var NAMING_MAPPING = {
            'GameInit': function(detail) {
                var players = detail['players'];
                var position = detail['position'];
                this.exhibit = function(game) {
                    game.initPosition(players, position);
                };
            },
            'SelectCharacter': function(detail) {
                var player = detail['player'];
                var character = detail['character'];
                var max_vigor = detail['max vigor'];
                this.exhibit = function(game) {
                    game.player(player).eventCharSelected(character, max_vigor);
                };
            },
            'DrawCards': function(detail) {
                var player = detail['player'];
                var cards = detail['draw'];
                if (typeof cards === 'number') {
                    this.exhibit = function(game) {
                        game.player(player).eventDrawCount(cards);
                    };
                } else {
                    this.exhibit = function(game) {
                        game.player(player).eventDrawCards(buildCards(cards));
                    };
                }
            },
            'DiscardCards': function(detail) {
                var player = detail['player'];
                var cards = detail['discard'];
                this.exhibit = function(game) {
                    game.player(player).eventDiscard(buildCards(cards));
                };
            },
            'PublicCardsTransfer': function(detail) {
                var source = detail['source'];
                var target = detail['target'];
                var transfer = detail['transfer'];
                this.exhibit = function(game) {
                    game.eventTransferCards(source, target,
                                            buildCards(transfer));
                };
            },
            'PrivateCardsTransfer': function(detail) {
                var source = detail['source'];
                var target = detail['target'];
                var trans = detail['transfer'];
                if (typeof trans === 'number') {
                    this.exhibit = function(game) {
                        game.eventTransferCount(source, target, trans);
                    };
                } else {
                    this.exhibit = function(game) {
                        game.eventTransferCards(source, target,
                                                buildCards(trans));
                    };
                }
            },
            'UseCardsForPlayers': function(detail) {
                var user = detail['user'];
                var targets = detail['target'];
                var use = detail['use'];
                this.exhibit = function(game) {
                    game.player(user).eventUseCards(buildCards(use), targets);
                };
            },
            'PlayCards': function(detail) {
                var player = detail['player'];
                var play = detail['play'];
                this.exhibit = function(game) {
                    game.player(player).eventPlayCards(buildCards(play));
                };
            },
            'ShowCards': function(detail) {
                var player = detail['player'];
                var show = detail['show'];
                this.exhibit = function(game) {
                    game.player(player).eventShowCards(buildCards(show));
                };
            },
            'Damage': function(detail) {
                var victim = detail['victim'];
                var damage = detail['damage'];
                var category = detail['category'];
                this.exhibit = function(game) {
                    game.player(victim).eventDamage(damage, category);
                };
            },
            'VigorLost': function(detail) {
                var player = detail['player'];
                var point = detail['point'];
                this.exhibit = function(game) {
                    game.player(player).eventVigorLost(point);
                };
            },
            'VigorRegain': function(detail) {
                var player = detail['player'];
                var point = detail['point'];
                this.exhibit = function(game) {
                    game.player(player).eventVigorRegain(point);
                };
            },
            'PlayerKilled': function(detail) {
                var player = detail['player'];
                this.exhibit = function(game) {
                    game.player(player).eventKilled();
                };
            },
            'Equip': function(detail) {
                var player = detail['player'];
                var equip = detail['equip'];
                var region = detail['region'];
                this.exhibit = function(game) {
                    game.player(player).eventEquip(new Card(equip), region);
                };
            },
            'Unequip': function(detail) {
                var player = detail['player'];
                var unequip = detail['unequip'];
                var region = detail['region'];
                this.exhibit = function(game) {
                    game.player(player).eventUnequip(new Card(unequip), region);
                };
            },
        };
        return new NAMING_MAPPING[detail['type']](detail);
    }
    this.events = new Array();

    this.prevId = function() {
        return this.events.length;
    };
    this.append = function(result, game) {
        if (result['code'] != 200) {
            return;
        }
        var events = result['events'];
        for (i in events) {
            var e = buildEvent(events[i]);
            this.events.push(e);
            e.exhibit(game);
        }
    };
}
