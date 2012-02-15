function initViews(gamePane) {
    function Game(me, others, center) {
        var players = new Array();

        this.initPosition = function(playerCount, myPosition) {
            /*
             * 6 5 4 3 2
             * 7       1
             *  My Pos-
             */
            var positions = new Array(6, 5, 4, 3, 2, 7, 1, 0);
            others.push(me);
            for (i in positions) {
                var index = (positions[i] + myPosition) % 8;
                if (index != myPosition) {
                    players[index] = new Player(others[i]);
                } else {
                    players[index] = new Me(me);
                }
            }
        }
        this.player = function(id) {
            return players[id];
        };
        var hintparser = new SGS_HintParser(this, players, new Center(center));
        this.hint = function(result) {
            center.innerHTML = '';
            hintparser.hint(result);
        };
    }

    var views = new Array();

    var row1st = document.createElement('tr');
    for (col = 0; col < 5; ++col) {
        var column = document.createElement('td');
        row1st.appendChild(column);
        views.push(column);
    }
    gamePane.appendChild(row1st);

    var row2nd = document.createElement('tr');
    var cell2 = document.createElement('td');
    row2nd.appendChild(cell2);
    var cellcenter = document.createElement('td');
    cellcenter.setAttribute('colspan', '3');
    row2nd.appendChild(cellcenter);
    var cell6 = document.createElement('td');
    row2nd.appendChild(cell6);
    gamePane.appendChild(row2nd);

    views.push(cell2);
    views.push(cell6);

    var row3rd = document.createElement('tr');
    var cellme = document.createElement('td');
    cellme.setAttribute('colspan', '5');
    row3rd.appendChild(cellme);
    gamePane.appendChild(row3rd);

    return new Game(cellme, views, cellcenter);
}

function Player(view) {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.height = 128;
    canvas.width = 72;
    view.appendChild(canvas);

    this.cards_count = 0;

    this.drawCount = function(count) {
        this.cards_count += count;
        context.save();
        context.fillStyle = '#fff';
        context.fillRect(0, 16, 72, 16);
        context.restore();

        context.save();
        context.textBaseline = 'top';
        context.fillText(this.cards_count, 0, 16, 16);
        context.restore();
    };
    this.drawCards = function(cards) {
        for (i in cards) {
            view.innerHTML +=
                ('Player ' + ' draws ' + cards[i].name + ' of rank ' +
                 cards[i].rank + SGS_STR_CARD_SUITS[cards[i].suit] + ' at '
                 + cards[i].region + '<br/>');
        }
    };
    this.activate = function() {
        view.style.backgroundColor = '#ffb';
    };
    this.deactivate = function() {
        view.style.backgroundColor = '#fff';
    };
    this.selectCharacter = function(name) {
        context.save();
        context.textBaseline = 'top';
        context.fillText(name, 0, 0, 72);
        context.restore();
    };
}

function Me(me) {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.height = 128;
    canvas.width = 360;
    me.appendChild(canvas);

    this.cards = new Array();

    this.drawCards = function(cards) {
        this.cards = this.cards.concat(cards);
        context.save();
        context.fillStyle = '#ddd';
        context.fillRect(80, 0, 320, 128);
        context.restore();

        context.save();
        context.textBaseline = 'top';
        for (i = 0; i < this.cards.length; ++i) {
            var c = this.cards[i];
            var x = 80 + i * 40;
            context.fillText(c.rank + 1, x, 0, 16);
            context.fillText(SGS_STR_CARD_SUITS[c.suit], x + 16, 0, 16);
            context.fillText(c.name, x, 16, 40);
        }
        context.restore();
    };
    this.activate = function() {
        me.style.backgroundColor = '#bff';
    };
    this.deactivate = function() {
        me.style.backgroundColor = '#fff';
    };
    this.selectCharacter = function(name) {
        context.save();
        context.textBaseline = 'top';
        context.fillText(name, 0, 0, 80);
        context.restore();
    };
}

function Center(center) {
    this.selectCharacters = function(candidates) {
        var selections = new Array();
        for (i in candidates) {
            var s = document.createElement('button');
            s.innerHTML = candidates[i];
            s.onclick = function(event) {
                post_act({
                             'select': this.innerHTML,
                         });
            };
            center.appendChild(s);
        }
    };
}
