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
