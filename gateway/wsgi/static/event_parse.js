function EventList() {
    function buildEvent(detail) {
        function Card(id, name, rank, suit) {
            this.id = id;
            this.name = name;
            this.rank = rank;
            this.suit = suit;
        }
        function buildCards(detail) {
            var result = new Array();
            for (i = 0; i < detail.length; ++i) {
                result.push(new Card(detail[i]['id'], detail[i]['name'],
                                     detail[i]['rank'], detail[i]['suit']));
            }
            return result;
        }
        var NAMING_MAPPING = {
            'GameStarted': function(detail) {
                this.characters = detail['characters'];
                this.exhibit = function(game) {
                };
            }, 'DrawCards': function(detail) {
                this.player = detail['player'];
                this.cards = detail['draw'];
                this.exhibit = function(game) {
                    var player = game.player(this.player);
                    if (typeof this.cards === 'number') {
                        player.drawCount(this.cards);
                    } else {
                        player.drawCards(buildCards(this.cards));
                    }
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
