function Player(view) {
    this.drawCount = function(count) {
        view.innerHTML += ('Player ' + ' draws ' + count + ' card(s)<br/>');
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
        view.innerHTML += ('Select ' + name + '<br/>');
    };
}
function Me(me) {
    this.drawCount = function(count) {
        me.innerHTML += ('Player ' + ' draws ' + count + ' card(s)<br/>');
    };
    this.drawCards = function(cards) {
        for (i in cards) {
            me.innerHTML +=
                ('Player ' + ' draws ' + cards[i].name + ' of rank ' +
                 cards[i].rank + SGS_STR_CARD_SUITS[cards[i].suit] + ' at '
                 + cards[i].region + '<br/>');
        }
    };
    this.activate = function() {
        me.style.backgroundColor = '#bff';
    };
    this.deactivate = function() {
        me.style.backgroundColor = '#fff';
    };
    this.selectCharacter = function(name) {
        me.innerHTML += ('Select ' + name + '<br/>');
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
