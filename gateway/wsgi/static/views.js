function Coord(x, y) {
    this.x = x;
    this.y = y;

    this.isIn = function(x, y, w, h) {
        return x <= this.x && this.x < x + w && y <= this.y && this.y < y + h;
    };

    this.offset = function(dx, dy) {
        return new Coord(this.x + dx, this.y + dy);
    };

    this.translate = function(dx, dy) {
        return this.offset(-dx, -dy);
    };
}

var HORI_PADDING = 10;
var VERT_PADDING = 16;
var CHILD_HORI_INTERVAL = 16;
var CHILD_VERT_INTERVAL = 12;
var CANVAS_W = 720;
var CANVAS_H = 540;
var CHILD_W = 108;
var CHILD_H = 144;
var CENTER_W = CHILD_W * 3 + CHILD_HORI_INTERVAL * 2;
var CENTER_H = CANVAS_H - (VERT_PADDING + CHILD_H + CHILD_VERT_INTERVAL) * 2
var ME_W = CHILD_W * 5 + CHILD_HORI_INTERVAL * 4;
var ME_H = CHILD_H;
var CARD_W = 48;
var BORDER = 4;
var TEXT_H = 16;
var NUM_W = 16;

function paintCard(ctxt, card, position) {
    var x = position * CARD_W;
    ctxt.save();
    ctxt.fillStyle = card.selected ? '#fff' : '#aaa';
    ctxt.fillRect(x, 0, CARD_W, ME_H);
    ctxt.restore();

    ctxt.save();
    ctxt.textBaseline = 'top';
    ctxt.save();
    ctxt.fillStyle = SGS_STR_CARD_SUITS_COLOR[card.suit];
    ctxt.fillText(SGS_STR_CARD_RANKS[card.rank], x, 0, NUM_W);
    ctxt.fillText(SGS_STR_CARD_SUITS[card.suit], x + NUM_W, 0, NUM_W);
    ctxt.restore();
    ctxt.fillText(card.name, x, TEXT_H, CARD_W);
    ctxt.restore();
}

function Game(pane) {
    /*
     *   5 4 3
     * 6       2
     * 7       1
     *  My Pos-
     */
    var FIRST_X = HORI_PADDING + CHILD_W + CHILD_HORI_INTERVAL;
    var FIRST_Y = VERT_PADDING;
    var SECOND_X = HORI_PADDING;
    var SECOND_Y = CANVAS_H - VERT_PADDING - CHILD_H * 3 -
                        CHILD_VERT_INTERVAL * 2;
    var THIRD_X = HORI_PADDING;
    var THIRD_Y = SECOND_Y + CHILD_H + CHILD_VERT_INTERVAL;
    var CENTER_X = SECOND_X + CHILD_W + CHILD_HORI_INTERVAL;
    var CENTER_Y = FIRST_Y + CHILD_H + CHILD_VERT_INTERVAL;
    var ME_X = HORI_PADDING;
    var ME_Y = THIRD_Y + CHILD_H + CHILD_VERT_INTERVAL;
    var childAreas = [
        new Coord(ME_X, ME_Y),
        new Coord(THIRD_X + (CHILD_W + CHILD_HORI_INTERVAL) * 4, THIRD_Y),
        new Coord(SECOND_X + (CHILD_W + CHILD_HORI_INTERVAL) * 4, SECOND_Y),
        new Coord(FIRST_X + (CHILD_W + CHILD_HORI_INTERVAL) * 2, FIRST_Y),
        new Coord(FIRST_X + CHILD_W + CHILD_HORI_INTERVAL, FIRST_Y),
        new Coord(FIRST_X, FIRST_Y),
        new Coord(SECOND_X, SECOND_Y),
        new Coord(THIRD_X, THIRD_Y),
    ];

    var canvas = new CanvasLite(0, 0, CANVAS_W, CANVAS_H, null);
    canvas.hide();
    var players = [];
    this.initPosition = function(playersCount, pos) {
        canvas.reset();
        var center = new Center(canvas, new Coord(CENTER_X, CENTER_Y));
        for (i = 0; i < 8; ++i) {
            if (i != pos) {
                players[i] = new Player(canvas, childAreas[(8 + i - pos) % 8],
                                        center);
            } else {
                players[i] = new Me(canvas, childAreas[0], center);
            }
        }
        var hintparser = new SGS_HintParser(this, players, center);
        this.hint = function(result) {
            hintparser.hint(result);
        };
    };
    this.player = function(id) {
        return players[id];
    };
}

function Center(pc, coord) {
    var canvas = new CanvasLite(coord.x, coord.y, CENTER_W, CENTER_H, pc);

    var count_cards = 0;

    function clearCenter() {
        canvas.reset()
        count_cards = 0;
        canvas.fillBg('#ccc');
    };

    this.clear = clearCenter;
    this.selectCharacters = function(candidates) {
        var ctxt = canvas.context();
        ctxt.save();
        var width = (CENTER_W - (CHILD_HORI_INTERVAL * (candidates.length - 1)))
                            / candidates.length;
        ctxt.textBaseline = 'top';
        for (i = 0; i < candidates.length; ++i) {
            ctxt.fillStyle = '#ddd';
            var x = (width + CHILD_HORI_INTERVAL) * i;
            ctxt.fillRect(x, 0, width, CENTER_H);
            ctxt.fillStyle = '#000';
            ctxt.fillText(candidates[i], x, 0, width);
        }
        ctxt.restore();
        canvas.click(function(x, y) {
            if (x % Math.floor(width + CHILD_HORI_INTERVAL) <= width) {
                var index = Math.floor(x / (width + CHILD_HORI_INTERVAL));
                post_act({ 'select': candidates[index] });
                clearCenter();
                canvas.click(function(x, y) {});
            }
        });
    };
    this.addCard = function(card) {
        var x = count_cards * CARD_W;
        ++count_cards;
        var c = new CanvasLite(x, 0, CARD_W, CENTER_H, canvas);
        c.fillBg(card.selected ? '#fff' : '#aaa');

        var ctxt = c.context();
        ctxt.save();
        ctxt.textBaseline = 'top';
        ctxt.fillStyle = SGS_STR_CARD_SUITS_COLOR[card.suit];
        ctxt.fillText(SGS_STR_CARD_RANKS[card.rank], 0, 0, NUM_W);
        ctxt.fillText(SGS_STR_CARD_SUITS[card.suit], NUM_W, 0, NUM_W);
        ctxt.fillText(card.name, 0, TEXT_H, CARD_W);
        ctxt.restore();
    };
}

function Player(pc, coord, center) {
    var canvas = new CanvasLite(coord.x, coord.y, CHILD_W, CHILD_H, pc);
    canvas.fillBg('#ccc');
    var cards_count = 0;
    function repaintCardCount() {
        var ctxt = canvas.context();
        ctxt.save();
        ctxt.save();
        ctxt.fillStyle = '#fff';
        ctxt.fillRect(0, TEXT_H, NUM_W, TEXT_H);
        ctxt.restore();

        ctxt.textBaseline = 'top';
        ctxt.fillText(cards_count, 0, NUM_W, TEXT_H);
        ctxt.restore();
    }
    this.eventDrawCount = function(count) {
        cards_count += count;
        repaintCardCount();
    };
    this.activate = function() {
        canvas.paintBorder('#f33', BORDER);
    };
    this.deactivate = function() {
        canvas.paintBorder('#aaa', BORDER);
    };
    this.eventCharSelected = function(name, max_vigor) {
        var ctxt = canvas.context();
        ctxt.save();
        ctxt.textBaseline = 'top';
        ctxt.fillText(name, 0, 0, CHILD_W - BORDER * 2);
        ctxt.fillText(Array(max_vigor + 1).join('[]'), TEXT_H, NUM_W,
                      CHILD_W - NUM_W - BORDER * 2);
        ctxt.restore();
    };
    this.hintUseCards = function() {};
    this.hintDiscardCards = function(count, filter) {}
    this.eventDiscard = function(c) {
        center.clear();
        for (i = 0; i < c.length; ++i) {
            center.addCard(c[i]);
        }
        cards_count -= c.length;
        repaintCardCount();
    };
}

function Me(pc, coord, center) {
    this.click = function(c) {};
    var canvas = new CanvasLite(coord.x, coord.y, ME_W, ME_H, pc);
    var cards = new Array();

    var LEFT_AREA = 80;
    var RIGHT_AREA = 80;

    var left = new CanvasLite(0, 0, LEFT_AREA, ME_H, canvas);
    var middle = new CanvasLite(LEFT_AREA, 0, ME_W - LEFT_AREA - RIGHT_AREA,
                                ME_H, canvas);
    var right = new CanvasLite(ME_W - RIGHT_AREA, 0, RIGHT_AREA, CHILD_H,
                               canvas);
    var me = this;

    function enableCardClick(filter) {
        middle.click(function (x, y) {
            if (x < CARD_W * cards.length) {
                var index = Math.floor(x / CARD_W);
                var card = cards[index];
                if (card.selected || filter(card, selected())) {
                    card.selected = !card.selected;
                    paintCard(middle.context(), card, index);
                }
            }
        });
    }

    function disableCardClick() {
        middle.click(function (x, y) {});
    }

    function repaintCards() {
        middle.fillBg('#ccc');
        for (i = 0; i < cards.length; ++i) {
            paintCard(middle.context(), cards[i], i);
        }
    }
    function resetRight() {
        right.fillBg('#fff');
    }

    this.eventDrawCards = function(new_cards) {
        for (c in new_cards) {
            new_cards[c].selected = false;
        }
        cards = cards.concat(new_cards);
        repaintCards();
    };
    this.activate = function() {
        canvas.paintBorder('#bb1', BORDER);
    };
    this.deactivate = function() {
        canvas.paintBorder('#aaa', BORDER);
    };
    this.eventCharSelected = function(name, max_vigor) {
        var ctxt = left.context();
        ctxt.save();
        ctxt.textBaseline = 'top';
        ctxt.fillText(name, 0, 0, LEFT_AREA);
        ctxt.fillText(Array(max_vigor + 1).join('[]'), 0, TEXT_H, LEFT_AREA);
        ctxt.restore();
    };
    this.hintUseCards = function() {
        enableCardClick(function(c, s) { return true; });
        var ctxt = right.context();

        ctxt.save();
        ctxt.textBaseline = 'top';

        ctxt.save();
        ctxt.fillStyle = '#f88';
        ctxt.fillRect(0, 0, RIGHT_AREA, ME_H / 2);
        ctxt.restore();
        ctxt.save();
        ctxt.fillStyle = '#088';
        ctxt.fillText('Use!', 0, 0, RIGHT_AREA);
        ctxt.restore();

        ctxt.save();
        ctxt.fillStyle = '#afa';
        ctxt.fillRect(0, ME_H / 2, RIGHT_AREA, ME_H / 4);
        ctxt.restore();
        ctxt.save();
        ctxt.fillStyle = '#808';
        ctxt.fillText('Cancel', 0, ME_H / 2, RIGHT_AREA);
        ctxt.restore();

        ctxt.save();
        ctxt.fillStyle = '#888';
        ctxt.fillRect(0, ME_H * 3 / 4, RIGHT_AREA, ME_H / 4);
        ctxt.restore();
        ctxt.save();
        ctxt.fillStyle = '#000';
        ctxt.fillText('Give up', 0, ME_H * 3 / 4, RIGHT_AREA);
        ctxt.restore();

        ctxt.restore();

        right.click(function(x, y) {
            if (ME_H * 3 / 4 < y) {
                disableCardClick();
                post_act({
                             'action': 'give up',
                         });
            }
        });
    };

    function selectedCount() {
        var c = 0;
        for (i in cards) {
            if (cards[i].selected) ++c;
        }
        return c;
    }
    function selected() {
        var c = new Array();
        for (i in cards) {
            if (cards[i].selected) c.push(cards[i]);
        }
        return c;
    }
    function removeCards(c) {
        for (i = 0; i < c.length; ++i) {
            for (j = 0; j < cards.length; ++j) {
                if (c[i].id == cards[j].id) {
                    cards.splice(j, 1);
                    break;
                }
            }
        }
    }

    this.hintDiscardCards = startDiscarding;

    function startDiscarding(filter, validator, giveUpAllow) {
        this.hintDiscardCards = function(filter, giveUpAllow) {};
        enableCardClick(filter);

        var ctxt = right.context();
        for (i = 0; i < cards.length; ++i) {
            if (cards[i].selected) {
                cards[i].selected = false;
            }
        }
        repaintCards();

        right.fillBg('#aaa');
        ctxt.save();
        ctxt.textBaseline = 'top';
        ctxt.fillStyle = '#111';
        ctxt.fillText('Discard', 0, 0, RIGHT_AREA);
        ctxt.restore();

        right.click(function(x, y) {
            if (validator(selected())) {
                var discarding = new Array();
                var selectedCards = selected();
                for (i in selectedCards) {
                    discarding.push(selectedCards[i].id);
                }
                disableCardClick();
                resetRight();
                post_act({ 'discard': discarding });
                me.hintDiscardCards = startDiscarding;
            }
        });
    };

    this.eventDiscard = function(c) {
        center.clear();
        removeCards(c);
        repaintCards();
        for (i = 0; i < c.length; ++i) {
            center.addCard(c[i]);
        }
    };
}
