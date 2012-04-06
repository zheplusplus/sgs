function Coord(x, y) {
    return { x: x, y: y };
}

var HORI_PADDING = 10;
var VERT_PADDING = 16;
var CHILD_HORI_INTERVAL = 16;
var CHILD_VERT_INTERVAL = 12;
var CANVAS_W = 960;
var CANVAS_H = 720;
var CHILD_W = 144;
var CHILD_H = 180;
var CENTER_W = CHILD_W * 3 + CHILD_HORI_INTERVAL * 2;
var CENTER_H = CANVAS_H - (VERT_PADDING + CHILD_H + CHILD_VERT_INTERVAL) * 2
var ME_W = CHILD_W * 5 + CHILD_HORI_INTERVAL * 4;
var ME_H = CHILD_H;
var CARD_W = 64;
var BORDER = 4;
var TEXT_H = 16;
var NUM_W = 16;

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
        Coord(ME_X, ME_Y),
        Coord(THIRD_X + (CHILD_W + CHILD_HORI_INTERVAL) * 4, THIRD_Y),
        Coord(SECOND_X + (CHILD_W + CHILD_HORI_INTERVAL) * 4, SECOND_Y),
        Coord(FIRST_X + (CHILD_W + CHILD_HORI_INTERVAL) * 2, FIRST_Y),
        Coord(FIRST_X + CHILD_W + CHILD_HORI_INTERVAL, FIRST_Y),
        Coord(FIRST_X, FIRST_Y),
        Coord(SECOND_X, SECOND_Y),
        Coord(THIRD_X, THIRD_Y),
    ];

    var canvas = createRootCanvas(pane, CANVAS_W, CANVAS_H);
    this.initPosition = function(playersCount, pos) {
        var players = [];
        var center = new CenterView(canvas, Coord(CENTER_X, CENTER_Y));
        for (var i = 0; i < 8; ++i) {
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
        SGS_InitGame(this, players, center);
        this.paintTransferCount = function(s, t, c, complete) {
            complete();
        };
        this.paintTransferCards = function(s, t, c, complete) {
            complete();
        };

        this.enableAnimation = function() {
            enableGameAnimation(this, players);
        };
    };

    function enableGameAnimation(game, players) {
        initFloatings(pane);
        game.paintTransferCount = function(source, target, count, complete) {
            movingCards.moveCount(source.centerCoord(), target.centerCoord(),
                                  count, complete);
        };
        game.paintTransferCards = function(source, target, cards, complete) {
            movingCards.moveCards(source.centerCoord(), target.centerCoord(),
                                  cards, complete);
        };
        for (var i in players) {
            players[i].enableAnimation();
        }
    };
}

function CenterView(pc, coord) {
    InitCenterCanvas(this, coord.x, coord.y, CENTER_W, CENTER_H, pc);
}

function PlayerView(id, game, pc, coord, center) {
    SGS_InitPlayer(this, id);
    InitPlayerCanvas(this, game, coord.x, coord.y, CHILD_W, CHILD_H, pc);

    this.paintDamage = function(damage, category) {};
    this.paintVigorRegain = function(point) {};
    this.paintVigorLost = function(point) {};

    this.paintDrawCount = function(count, complete) {
        complete();
    };
    function paintCardsDropped(c) {
        center.addCards(c);
    };
    this.paintUseCards = function(cards, target) {
        paintCardsDropped(cards);
    };
    this.paintDiscardCards = function(c) {
        paintCardsDropped(c);
    };
    this.paintPlayCards = function(c) {
        paintCardsDropped(c);
    };
    this.paintShowCards = function(c) {
        paintCardsDropped(c);
    };
    this.paintInvokingSkill = function(n) {};

    var me = this;
    this.enableAnimation = function() {
        this.paintDrawCount = function(count, complete) {
            movingCards.moveCount(center.centerCoord(), this.centerCoord(),
                                  count, complete);
        };
        paintCardsDropped = function(c) {
            movingCards.moveCards(me.centerCoord(), center.centerCoord(),
                                  c, function() { center.addCards(c); });
        };
        this.paintInvokingSkill = this.onInvokingSkill;
    };
}

function MeView(id, game, pc, coord, center, players) {
    SGS_InitMe(this, id, game, players);
    var RIGHTW = 80;
    var MIDW = ME_W - CHILD_W - RIGHTW;
    InitMeCanvas(this, game, coord.x, coord.y, CHILD_W, MIDW, RIGHTW, ME_H, pc);

    this.paintDamage = function(damage, category) {};
    this.paintVigorRegain = function(point) {};
    this.paintVigorLost = function(point) {};

    this.paintDrawCards = function(c, complete) {
        complete();
    };
    paintCardsDropped = function(c) {
        center.addCards(c);
    };
    this.paintDiscardCards = function(c) {
        paintCardsDropped(c);
    };
    this.paintUseCards = function(c, targets) {
        paintCardsDropped(c);
    };

    this.paintPlayCards = function(c) {
        paintCardsDropped(c);
    };
    this.paintShowCards = function(c) {
        paintCardsDropped(c);
    };
    this.paintInvokingSkill = function(n) {};

    var me = this;
    this.enableAnimation = function() {
        this.paintDrawCards = function(cards, complete) {
            movingCards.moveCards(center.centerCoord(), this.centerCoord(),
                                  cards, complete);
        };
        paintCardsDropped = function(c) {
            movingCards.moveCards(me.centerCoord(), center.centerCoord(), c,
                                  function() { center.addCards(c); });
        };
        this.paintDamage = this.animeDamaged;
        this.paintInvokingSkill = this.onInvokingSkill;
    };
}
