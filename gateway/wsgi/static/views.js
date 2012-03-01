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

function paintEquip(ctxt, card, position) {
    var y = position * TEXT_H;
    ctxt.save();
    ctxt.textBaseline = 'top';

    ctxt.save();
    ctxt.fillStyle = SGS_STR_CARD_SUITS_COLOR[card.suit];
    ctxt.fillText(SGS_STR_CARD_RANKS[card.rank], 0, y, NUM_W);
    ctxt.fillText(SGS_STR_CARD_SUITS[card.suit], NUM_W, y, NUM_W);
    ctxt.restore();

    ctxt.save();
    ctxt.fillStyle = '#000';
    ctxt.fillText(card.name, NUM_W * 2, y, CARD_W);
    ctxt.restore();

    ctxt.restore();
}

function clearEquip(ctxt, position) {
    var y = position * TEXT_H;
    ctxt.save();
    ctxt.fillStyle = '#fff';
    ctxt.fillRect(0, y, CARD_W + NUM_W * 2, TEXT_H);
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
    this.initPosition = function(playersCount, pos) {
        var players = [];
        canvas.reset();
        var center = new CenterView(canvas, new Coord(CENTER_X, CENTER_Y));
        for (i = 0; i < 8; ++i) {
            if (i != pos) {
                players[i] = new PlayerView(i, this, canvas,
                                            childAreas[(8 + i - pos) % 8],
                                            center);
            } else {
                var me = new MeView(i, this, canvas, childAreas[0], center,
                                    players);
                players[i] = me
                this.clickOnTarget = function(target) {
                    me.clickOnTarget(target);
                };
            }
        }
        this.player = function(id) {
            return players[id];
        };
        this.deactivateAll = function() {
            for (i in players) {
                players[i].deactivate();
            }
        };
        this.clearTargets = function() {
        };

        var hintparser = new SGS_HintParser(this, center);
        this.hint = function(result) {
            hintparser.hint(result);
        };
        this.hintRegions = function(regions) {
            center.selectRegion(regions);
        };
        this.eventTransferCount = function(source, target, count) {
            this.player(source).eventDiscardCount(count);
            this.player(target).eventDrawCount(count);
        };
        this.eventTransferCards = function(source, target, cards) {
            this.player(source).eventDiscard(cards);
            this.player(target).eventDrawCards(cards);
        };
    };
}

function CenterView(pc, coord) {
    var canvas = new CanvasLite(coord.x, coord.y, CENTER_W, CENTER_H, pc);
    var ctxt = canvas.context();

    var count_cards = 0;

    function clear() {
        canvas.reset()
        count_cards = 0;
        canvas.fillBg('#ccc');
    }

    this.selectCharacters = function(candidates) {
        clear();
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
                clear();
                canvas.click(function(x, y) {});
            }
        });
    };
    this.selectRegion = function(regions) {
        clear();
        var width = (CENTER_W - (CHILD_HORI_INTERVAL * (regions.length - 1)))
                            / regions.length;
        ctxt.save();
        ctxt.textBaseline = 'top';
        for (i = 0; i < regions.length; ++i) {
            ctxt.fillStyle = '#ddd';
            var x = (width + CHILD_HORI_INTERVAL) * i;
            ctxt.fillRect(x, 0, width, CENTER_H);
            ctxt.fillStyle = '#000';
            ctxt.fillText(regions[i], x, 0, width);
        }
        ctxt.restore();
        canvas.click(function(x, y) {
            if (x % Math.floor(width + CHILD_HORI_INTERVAL) <= width) {
                var index = Math.floor(x / (width + CHILD_HORI_INTERVAL));
                post_act({ 'region': regions[index] });
                clear();
                canvas.click(function(x, y) {});
            }
        });
    };
    this.addCard = function(card) {
        paintCard(ctxt, card, count_cards);
        count_cards = (count_cards + 1) % 7;
    };
}

function PlayerView(id, game, pc, coord, center) {
    SGS_InitPlayer(this, id);

    var canvas = new CanvasLite(coord.x, coord.y, CHILD_W, CHILD_H, pc);
    canvas.fillBg('#ccc');
    var ctxt = canvas.context();

    this.updateSelected = function() {
        this.deactivate();
    };
    this.activate = function() {
        canvas.paintBorder('#f33', BORDER);
    };
    this.deactivate = function() {
        canvas.paintBorder(this.selected() ? '#0ff': '#aaa', BORDER);
    };

    this.eventDrawCards = function(cards) {
        this.eventDrawCount(cards.length);
    };
    this.onCardsCountChanged = function(before, after) {
        ctxt.save();
        ctxt.fillStyle = '#fff';
        ctxt.fillRect(0, TEXT_H, NUM_W, TEXT_H);
        ctxt.restore();

        ctxt.save();
        ctxt.textBaseline = 'top';
        ctxt.fillText(after, 0, NUM_W, TEXT_H);
        ctxt.restore();
    };
    this.onCardDropped = function(c) {
        center.addCard(c);
    };

    function refreshVigor(vigor, max) {
        var text = Array(vigor + 1).join('[]');
        text += Array(max - vigor + 1).join('//');

        ctxt.save();
        ctxt.fillStyle = '#fff';
        ctxt.fillRect(TEXT_H, NUM_W, CHILD_W - NUM_W - BORDER * 2, TEXT_H);
        ctxt.restore();

        ctxt.save();
        ctxt.textBaseline = 'top';
        ctxt.fillText(text, TEXT_H, NUM_W, CHILD_W - NUM_W - BORDER * 2);
        ctxt.restore();
    }

    this.onMaxVigorChanged = function(before, max, vigor) {
        refreshVigor(vigor, max);
    };
    this.onVigorChanged = function(before, vigor, max) {
        if (vigor < 0) vigor = 0;
        refreshVigor(vigor, max);
    };
    this.onCharNameChanged = function(before, name) {
        ctxt.save();
        ctxt.textBaseline = 'top';
        ctxt.fillText(name, 0, 0, CHILD_W - BORDER * 2);
        ctxt.restore();
    };

    var EQUIP_OFFSET = {
        'weapon': 2,
        'armor': 3,
        '+1 horse': 4,
        '-1 horse': 5,
    };
    this.paintEquip = function(card, region) {
        paintEquip(ctxt, card, EQUIP_OFFSET[region]);
    };
    this.clearEquip = function(region) {
        clearEquip(ctxt, EQUIP_OFFSET[region]);
    };

    var me = this;
    canvas.click(function(x, y) {
        game.clickOnTarget(me);
    });
}

function MeView(id, game, pc, coord, center, players) {
    SGS_InitMe(id, this, game, players);
    this.click = function(c) {};
    var canvas = new CanvasLite(coord.x, coord.y, ME_W, ME_H, pc);

    var LEFT_AREA = 80;
    var RIGHT_AREA = 80;

    var left = new CanvasLite(0, 0, LEFT_AREA, ME_H, canvas);
    var middle = new CanvasLite(LEFT_AREA, 0, ME_W - LEFT_AREA - RIGHT_AREA,
                                ME_H, canvas);
    var right = new CanvasLite(ME_W - RIGHT_AREA, 0, RIGHT_AREA, CHILD_H,
                               canvas);
    right.fillBg('#888');

    var activated = false;
    this.updateSelected = function() {
        this.deactivate();
    };
    this.activate = function() {
        activated = true;
        canvas.paintBorder('#bb1', BORDER);
    };
    this.deactivate = function() {
        activated = false;
        canvas.paintBorder(this.selected() ? '#0ff': '#aaa', BORDER);
    };

    this.onCardDropped = function(c) {
        center.addCard(c);
    };

    function refreshVigor(vigor, max) {
        var ctxt = left.context();
        var text = Array(vigor + 1).join('[]');
        text += Array(max - vigor + 1).join('//');

        ctxt.save();
        ctxt.fillStyle = '#fff';
        ctxt.fillRect(0, TEXT_H, LEFT_AREA, TEXT_H);
        ctxt.restore();

        ctxt.save();
        ctxt.textBaseline = 'top';
        ctxt.fillText(text, 0, TEXT_H, LEFT_AREA);
        ctxt.restore();
    }
    this.onMaxVigorChanged = function(before, max, vigor) {
        refreshVigor(vigor, max);
    };
    this.onVigorChanged = function(before, vigor, max) {
        refreshVigor(vigor, max);
    };
    this.onCharNameChanged = function(before, name) {
        var ctxt = left.context();
        ctxt.save();
        ctxt.textBaseline = 'top';
        ctxt.fillText(name, 0, 0, LEFT_AREA);
        ctxt.restore();
    };
    var EQUIP_OFFSET = {
        'weapon': 2,
        'armor': 3,
        '+1 horse': 4,
        '-1 horse': 5,
    };
    this.paintEquip = function(card, region) {
        paintEquip(left.context(), card, EQUIP_OFFSET[region]);
    };
    this.clearEquip = function(region) {
        clearEquip(left.context(), EQUIP_OFFSET[region]);
    };

    function paintMethods(methods, selectedIndex) {
        right.fillBg('#888');
        var ctxt = right.context();
        var heightEach = ME_H / methods.length;
        ctxt.save();
        ctxt.fillStyle = '#0c8';
        ctxt.fillRect(0, heightEach * selectedIndex, RIGHT_AREA, heightEach);
        ctxt.restore();

        ctxt.save();
        ctxt.textBaseline = 'top';
        for (i = 0; i < methods.length; ++i) {
            ctxt.fillText(methods[i], 0, heightEach * i, RIGHT_AREA);
        }
        ctxt.restore();
        return heightEach;
    }

    this.clearMethods = function() {
        right.fillBg('#888');
        right.click(function(x, y) {});
    };

    var me = this;
    this.onMethodsChanged = function(methods) {
        var heightEach = paintMethods(methods, 0);
        right.click(function(x, y) {
            var index = Math.floor(y / heightEach);
            if (me.clickOnMethod(methods[index])) {
                paintMethods(methods, index);
            }
        });
    };
    this.clickOnTarget = function(target) {
        me.clickOnTarget(target);
    };
    this.onCardsChanged = function(cards) {
        middle.fillBg('#ccc');
        for (i = 0; i < cards.length; ++i) {
            paintCard(middle.context(), cards[i], i);
        }
        middle.click(function(x, y) {
            var index = Math.floor(x / CARD_W);
            if (index < cards.length) {
                me.clickOnCard(cards[index]);
            }
        });
    };
    left.click(function(x, y) {
        game.clickOnTarget(me);
    });
}
