function clearElement(e) {
    while (e.hasChildNodes()) {
        e.removeChild(e.lastChild);
    }
}

function createRootCanvas(pane, w, h) {
    root = document.createElement('div');
    root.style.width = w + 'px';
    root.style.height = h + 'px';
    root.style.zIndex = 0;
    clearElement(pane);
    pane.appendChild(root);
    return root;
}

var movingCards = null;

function createCardView(card) {
    var view = document.createElement('div');
    view.style.color = 'black';
    view.innerHTML = SGS_STR_Card(card.name);
    view.appendChild(document.createElement('br'));
    var suit = document.createElement('span');
    suit.style.color = SGS_STR_CARD_SUITS_COLOR[card.suit];
    suit.innerHTML = SGS_STR_CARD_RANKS[card.rank] + ' ' +
                     SGS_STR_CARD_SUITS[card.suit];
    view.appendChild(suit);
    view.style.width = CARD_W + 'px';
    return view;
}

function createFloatingCardView(card, offset) {
    var view = createCardView(card);
    view.style.position = 'absolute';
    view.style.left = offset * CARD_W + 'px';
    view.style.height = '80px';
    return view;
}

function initFloatings(pane) {
    if (movingCards != null) return;

    movingCards = document.createElement('div');
    movingCards.style.position = 'absolute';
    movingCards.style.visibility = 'hidden';
    movingCards.style.width = '128px';
    movingCards.style.height = '160px';
    movingCards.style.backgroundColor = 'transparent';
    movingCards.style.color = 'black';
    movingCards.style.zIndex = 256;

    movingCards.moveCount = function(initCoord, destCoord, count, complete) {
        animeQ.add(function(complete) {
            movingCards.innerHTML = count;
            moveFromTo(initCoord, destCoord, complete);
        }, function() {
            resetView();
            complete();
        });
    };
    movingCards.moveCards = function(initCoord, destCoord, cards, complete) {
        animeQ.add(function(complete) {
            movingCards.style.width = cards.length * CARD_W + 'px';
            for (var i = 0; i < cards.length; ++i) {
                movingCards.appendChild(createFloatingCardView(cards[i], i));
            }
            moveFromTo(initCoord, destCoord, complete);
        }, function() {
            resetView();
            complete();
        });
    };

    function resetView() {
        clearElement(movingCards);
        movingCards.style.width = '128px';
        movingCards.style.visibility = 'hidden';
    };
    function moveFromTo(initCoord, destCoord, complete) {
        movingCards.style.visibility = 'visible';
        movingCards.style.textAlign = 'center';
        var me = $(movingCards);
        me.offset({
            left: initCoord.x - me.width() / 2,
            top: initCoord.y - me.height() / 2,
        });
        var targetX = destCoord.x - me.width() / 2;
        var targetY = destCoord.y - me.height() / 2;
        me.animate({ left: targetX + 'px', top: targetY + 'px' }, 1000,
                   complete);
    }

    function AnimeQueue() {
        var playing = false;
        var q = [];

        this.add = function(anime, complete) {
            q.push(function() {
                anime(function() {
                    complete();
                    play();
                });
            });
            notify();
        };

        function notify() {
            if (playing) return;
            playing = true;
            play();
        }

        function play() {
            if (q.length > 0) {
                q.splice(0, 1)[0]();
            } else {
                playing = false;
            }
        }
    }
    var animeQ = new AnimeQueue();

    pane.appendChild(movingCards);
}

function InitCenterCanvas(me, x, y, w, h, p) {
    me.centerCoord = function() {
        return Coord(x + w / 2, y + h / 2);
    };

    var baseCanvas = document.createElement('div');
    baseCanvas.style.position = 'absolute';
    baseCanvas.style.left = x;
    baseCanvas.style.top = y;
    baseCanvas.style.width = w + 'px';
    baseCanvas.style.height = h + 'px';
    baseCanvas.style.backgroundColor = '#ccc';
    p.appendChild(baseCanvas);

    var discardedCardsTable = document.createElement('table');
    baseCanvas.appendChild(discardedCardsTable);
    discardedCardsTable.style.borderSpacing = '5px';
    discardedCardsTable.style.backgroundColor = '#ccc';
    var cardsRow = discardedCardsTable.insertRow();

    function addCard(card) {
        if (cardsRow.cells.length == 5) {
            cardsRow.deleteCell(0);
        }
        var cell = cardsRow.insertCell(-1);
        var cardView = createCardView(card);
        cell.appendChild(cardView);
    }

    me.addCards = function(cards) {
        for (var i in cards) {
            addCard(cards[i]);
        }
    };

    var floatingCanvas = document.createElement('div');
    floatingCanvas.style.position = 'absolute';
    floatingCanvas.style.visibility = 'hidden';
    floatingCanvas.style.backgroundColor = '#ccc';
    p.appendChild(floatingCanvas);

    function hideFloating() {
        floatingCanvas.style.visibility = 'hidden';
    }

    function showFloating() {
        floatingCanvas.style.visibility = 'visible';
        floatingCanvas.style.zIndex = movingCards.style.zIndex + 1;
    }

    function selectFrom(candidates, strMapper, onClick) {
        clearElement(floatingCanvas);
        showFloating();
        floatingCanvas.style.left = baseCanvas.style.left;
        floatingCanvas.style.top = baseCanvas.style.top;
        floatingCanvas.style.width = baseCanvas.style.width;
        floatingCanvas.style.height = baseCanvas.style.height;
        var table = document.createElement('table');
        floatingCanvas.appendChild(table);
        table.style.borderSpacing = '20px';
        table.style.backgroundColor = '#ccc';
        var row = table.insertRow();
        for (var i = 0; i < candidates.length; ++i) {
            var cell = row.insertCell(-1);
            cell.innerHTML = strMapper(candidates[i]);
            cell.actualValue = candidates[i];
            cell.style.backgroundColor = 'white';
            cell.onclick = function() {
                hideFloating();
                onClick(this.actualValue);
            };
        }
    }

    me.selectCharacters = function(candidates) {
        selectFrom(candidates, SGS_STR_CharName, function(value) {
            post_act({ 'select': value });
        });
    };
    me.selectRegion = function(regions) {
        selectFrom(regions, SGS_STR_Region, function(value) {
            post_act({ 'region': value });
        });
    };
}

function vigorString(vigor, max) {
    if (vigor < 0) vigor = 0;
    return Array(vigor + 1).join('[]') + Array(max - vigor + 1).join('//');
}

var EQUIP_OFFSET = {
    'weapon': 0,
    'armor': 1,
    '-1 horse': 2,
    '+1 horse': 3,
};
function equipString(card) {
    return '<span style="color:' + SGS_STR_CARD_SUITS_COLOR[card.suit] + ';">' +
           SGS_STR_CARD_RANKS[card.rank] + SGS_STR_CARD_SUITS[card.suit] +
           '</span>' + SGS_STR_Card(card.name);
}

function InitPlayerCanvas(me, game, x, y, w, h, p) {
    me.centerCoord = function() {
        return Coord(x + w / 2, y + h / 2);
    };

    var canvas = document.createElement('div');
    p.appendChild(canvas);

    canvas.style.position = 'absolute';
    canvas.style.left = x;
    canvas.style.top = y;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    canvas.style.borderRadius = '6px';

    canvas.onclick = function() { game.clickOnTarget(me) };

    me.activate = function() {
        paintBorder('#f33', BORDER);
    };
    me.deactivate = function() {
        paintBorder('#aaa', BORDER);
    };
    function paintBorder(color, borderSize) {
        canvas.style.border = 'solid ' + borderSize + 'px';
        canvas.style.borderColor = color;
    };

    me.updateSelected = function() {
        canvas.style.backgroundColor = me.selected() ? '#8ff': '#ccc';
    };
    me.updateSelected(false);

    var content = document.createElement('table');
    var nameRow = content.insertRow(-1);
    var nameCell = nameRow.insertCell();
    nameCell.colSpan = 2;
    nameCell.innerHTML = '&nbsp;';
    var statusRow = content.insertRow(-1);
    var vigorCell = statusRow.insertCell();
    vigorCell.style.textAlign = 'right';
    var cardsCountCell = statusRow.insertCell();
    cardsCountCell.innerHTML = '&nbsp;';

    var equipCells = [];
    for (var i = 0; i < 4; ++i) {
        var eqRow = content.insertRow(-1);
        var eqCell = eqRow.insertCell();
        eqCell.colSpan = 2;
        equipCells.push(eqCell);
        eqCell.innerHTML = '&nbsp;';
    }

    me.onCharNameChanged = function(name) {
        nameCell.innerHTML = SGS_STR_CharName(name);
    };
    me.paintCardsCountChanged = function(count) {
        cardsCountCell.innerHTML = count;
    };
    me.refreshVigor = function(vigor, max) {
        vigorCell.innerHTML = vigorString(vigor, max);
    };
    me.paintKilled = function() {
        nameCell.innerHTML += (' (' + SGS_STR_DEATH + ')');
    };

    me.paintEquip = function(card, region) {
        equipCells[EQUIP_OFFSET[region]].innerHTML = equipString(card);
    };
    me.clearEquip = function(card, region) {
        equipCells[EQUIP_OFFSET[region]].innerHTML = '&nbsp;';
    };
    canvas.appendChild(content);
    nameCell.style.width = w + 'px';
}

function InitMeCanvas(me, game, x, y, leftW, midW, rightW, h, p) {
    var w = leftW + midW + rightW;
    me.centerCoord = function() {
        return Coord(x + w / 2, y + h / 2);
    };

    var canvas = document.createElement('div');
    p.appendChild(canvas);

    canvas.style.position = 'absolute';
    canvas.style.left = x;
    canvas.style.top = y;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    canvas.style.borderRadius = '6px';

    me.activate = function() {
        paintBorder('#bb1', BORDER);
    };
    me.deactivate = function() {
        paintBorder('#aaa', BORDER);
    };
    function paintBorder(color, borderSize) {
        canvas.style.border = 'solid ' + borderSize + 'px';
        canvas.style.borderColor = color;
    };

    var content = document.createElement('table');
    canvas.appendChild(content);
    var contentRow = content.insertRow();

    var leftCell = contentRow.insertCell(-1);
    me.updateSelected = function() {
        leftCell.style.backgroundColor = me.selected() ? '#8ff': 'white';
    };
    me.animeDamaged = function(damage, category) {};

    var left = document.createElement('table');
    var nameRow = left.insertRow(-1);
    var nameCell = nameRow.insertCell();
    nameCell.innerHTML = '&nbsp;';
    me.onCharNameChanged = function(name) {
        nameCell.innerHTML = SGS_STR_CharName(name);
    };

    var statusRow = left.insertRow(-1);
    var vigorCell = statusRow.insertCell();
    vigorCell.innerHTML = '&nbsp;';
    me.refreshVigor = function(vigor, max) {
        vigorCell.innerHTML = vigorString(vigor, max);
    };
    me.paintKilled = function() {
        nameCell.innerHTML += (' (' + SGS_STR_DEATH + ')');
    };

    var equipCells = [];
    for (var i = 0; i < 4; ++i) {
        var eqRow = left.insertRow(-1);
        var eqCell = eqRow.insertCell();
        equipCells.push(eqCell);
        eqCell.innerHTML = '&nbsp;';
    }

    me.paintEquip = function(card, region) {
        var index = EQUIP_OFFSET[region];
        equipCells[index].innerHTML = equipString(card);
        equipCells[index].onclick = function() {
            if (me.clickOnEquip(region)) {
                selectEquip(index, me.equipment(region).selected);
            }
        };
        equipCells[index].style.backgroundColor = '#aaa';
    };
    function selectEquip(region, selected) {
        equipCells[region].style.backgroundColor = selected ? 'white' : '#aaa';
    };
    me.clearEquip = function(card, region) {
        equipCells[EQUIP_OFFSET[region]].innerHTML = '&nbsp;';
        equipCells[EQUIP_OFFSET[region]].onclick = function() {};
    };
    leftCell.appendChild(left);
    nameCell.style.width = leftW + 'px';

    nameCell.onclick = function() { game.clickOnTarget(me) };
    vigorCell.onclick = function() { game.clickOnTarget(me) };

    var cardsCell = contentRow.insertCell(-1);
    cardsCell.style.width = midW + 'px';
    cardsCell.style.backgroundColor = '#aaa';
    var cardsTable = document.createElement('table');
    cardsCell.appendChild(cardsTable);
    var cardsRow = cardsTable.insertRow();

    me.paintCards = function(cards) {
        clearElement(cardsRow);
        me.paintCardsAppended(cards);
    };
    me.paintCardsAppended = function(cards) {
        var offsetIndex = cardsRow.cells.length;
        for (var i = 0; i < cards.length; ++i) {
            var cardView = createCardView(cards[i]);
            var cardCell = cardsRow.insertCell(-1);
            cardCell.appendChild(cardView);
            cardCell.backgroundColor = '#ccc';
            cardCell.onclick = function() {
                var cardIndex = this.cellIndex - offsetIndex;
                if (me.clickOnCard(cards[cardIndex])) {
                    this.style.backgroundColor =
                        cards[cardIndex].selected ? 'white' : '#aaa';
                }
            };
        }
    };

    var methodsCell = contentRow.insertCell(-1);
    methodsCell.style.width = rightW + 'px';
    var methodsTable = document.createElement('table');
    methodsCell.appendChild(methodsTable);

    function changeMethods(methods, selectedIndex) {
        me.clearMethods();
        for (var i = 0; i < methods.length; ++i) {
            var row = methodsTable.insertRow(-1);
            var cell = row.insertCell();
            cell.innerHTML = SGS_STR_Action(methods[i]);
            if (i == selectedIndex) {
                row.style.backgroundColor = '#0c8';
            }
            row.onclick = function() {
                if (me.clickOnMethod(methods[this.rowIndex])) {
                    changeMethods(methods, this.rowIndex);
                }
            };
        }
    }
    me.onMethodsChanged = function(methods) {
        changeMethods(methods, 0);
    };
    me.clearMethods = function() {
        clearElement(methodsTable);
    };
}
