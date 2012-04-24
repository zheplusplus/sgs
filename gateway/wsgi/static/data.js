function SGS_InitGame(me, players, center) {
    var hint_parser = new SGS_HintParser(me, center);

    me.hint = function(result) {
        hint_parser.hint(result);
    };
    me.player = function(id) {
        return players[id];
    };
    me.deactivateAll = function() {
        for (var i in players) {
            players[i].deactivate();
        }
    };
    me.clearTargets = function() {
        for (var i in players) {
            players[i].deselect();
        }
    };
    me.hintRegions = function(regions) {
        center.selectRegion(regions);
    };
    me.eventTransferCount = function(source, target, count) {
        var sourceV = me.player(source);
        var targetV = me.player(target);
        sourceV.eventChangeCount(-count);
        me.paintTransferCount(sourceV, targetV, count, function() {
            targetV.eventChangeCount(count);
        });
    };
    me.eventTransferCards = function(source, target, cards) {
        var sourceV = me.player(source);
        var targetV = me.player(target);
        sourceV.lostCards(cards);
        me.paintTransferCards(sourceV, targetV, cards, function() {
            targetV.gainCards(cards);
        });
    };
}

function SGS_InitPlayer(me, id) {
    var cards_count = 0;
    var max_vigor = 0;
    var vigor = 0;
    var char_name = '';
    var selected = false;

    me.id = function() {
        return id;
    };

    me.select = function() {
        selected = true;
        me.updateSelected();
    };
    me.deselect = function() {
        selected = false;
        me.updateSelected();
    };
    me.selected = function() {
        return selected;
    };

    me.gainCards = function(c) {
        changeCardsCount(c.length);
    };
    me.lostCards = function(c) {
        changeCardsCount(-c.filter(function(card) {
            return card.region == 'onhand';
        }).length);
    };

    me.hasFreeOnHandCards = function() {
        return cards_count != 0;
    };

    me.eventCharSelected = function(new_name, new_max_vigor) {
        char_name = new_name;
        me.onCharNameChanged(char_name);
        max_vigor = new_max_vigor;
        vigor = new_max_vigor;
        me.refreshVigor(vigor, max_vigor);
    };
    me.eventKilled = function() {
        me.paintKilled();
    };

    function changeCardsCount(delta) {
        me.paintCardsCountChanged(cards_count += delta);
    }
    me.eventDrawCount = function(count) {
        me.paintDrawCount(count, function() {
            changeCardsCount(count);
        });
    };
    me.eventChangeCount = function(count) {
        changeCardsCount(count);
    };
    me.eventDiscard = function(c) {
        me.lostCards(c);
        me.paintDiscardCards(c);
    };
    me.eventUseCards = function(cards, targets) {
        me.lostCards(cards);
        me.paintUseCards(cards, targets);
    };
    me.eventPlayCards = function(cards) {
        me.lostCards(cards);
        me.paintPlayCards(cards);
    };
    me.eventShowCards = function(cards) {
        me.paintShowCards(cards);
    };

    function changeVigor(delta) {
        vigor += delta;
        me.refreshVigor(vigor, max_vigor);
    }
    me.eventDamage = function(damage, category) {
        me.paintDamage(damage, category);
        changeVigor(-damage);
    };
    me.eventVigorRegain = function(point) {
        me.paintVigorRegain(point);
        changeVigor(point);
    };
    me.eventVigorLost = function(point) {
        me.paintVigorLost(point);
        changeVigor(-point);
    };
    me.eventEquip = function(card, region) {
        changeCardsCount(-1);
        me.paintEquip(card, region);
    };
    me.eventUnequip = function(card, region) {
        me.clearEquip(card, region);
    };

    me.hintUseCards = function(m) {};
    me.hintDiscardCards = function(m) {};
}

function SGS_InitMe(me, id, game, players) {
    var cards = new Array();
    var max_vigor = 0;
    var vigor = 0;
    var char_name = '';
    var selected = false;
    var equipped = {};

    me.id = function() {
        return id;
    };

    me.select = function() {
        selected = true;
        me.updateSelected();
    };
    me.deselect = function() {
        selected = false;
        me.updateSelected();
    };
    me.selected = function() {
        return selected;
    };

    me.hasFreeOnHandCards = function() {
        for (var c in cards) {
            if (!cards[c].selected) return true;
        }
        return false;
    };

    function appendCards(new_cards) {
        for (var c in new_cards) {
            new_cards[c].selected = false;
        }
        cards = cards.concat(new_cards);
    }

    me.gainCards = function(new_cards) {
        appendCards(new_cards);
        me.paintCards(cards);
    };
    me.lostCards = function(c) {
        removeCards(c);
        me.paintCards(cards);
    };

    function selectedCards() {
        var c = new Array();
        for (var i in cards) {
            if (cards[i].selected) c.push(cards[i]);
        }
        for (var i in equipped) {
            if (equipped[i].selected) c.push(equipped[i]);
        }
        return c;
    }
    function selectedTargets() {
        var t = new Array();
        for (var i in players) {
            if (players[i].selected()) t.push(players[i]);
        }
        return t;
    }

    function clearSelectedCards() {
        for (var i in cards) {
            cards[i].selected = false;
        }
        me.paintCards(cards);
    }

    function removeCard(card) {
        for (var j = 0; j < cards.length; ++j) {
            if (card.id == cards[j].id) {
                cards.splice(j, 1);
                return;
            }
        }
    }
    function removeCards(cards) {
        for (var i in cards) {
            removeCard(cards[i]);
        }
    }

    me.eventCharSelected = function(new_name, new_max_vigor) {
        char_name = new_name;
        me.onCharNameChanged(char_name);
        max_vigor = new_max_vigor;
        vigor = new_max_vigor;
        me.refreshVigor(vigor, max_vigor);
    };
    me.eventKilled = function() {
        me.paintKilled();
    };

    me.eventDrawCards = function(new_cards) {
        appendCards(new_cards);
        me.paintDrawCards(new_cards, function() {
            me.paintCardsAppended(new_cards);
        });
    };
    me.eventDiscard = function(c) {
        removeCards(c);
        me.paintDiscardCards(c);
        me.paintCards(cards);
    };
    me.eventUseCards = function(c, targets) {
        removeCards(c);
        me.paintCards(cards);
        me.paintUseCards(c, targets);
    };
    me.eventPlayCards = function(c) {
        removeCards(c);
        me.paintPlayCards(c);
        me.paintCards(cards);
    };
    me.eventShowCards = function(c) {
        me.paintShowCards(c);
    };

    function changeVigor(delta) {
        vigor += delta;
        me.refreshVigor(vigor, max_vigor);
    }
    me.eventDamage = function(damage, category) {
        me.paintDamage(damage, category);
        changeVigor(-damage);
    };
    me.eventVigorRegain = function(point) {
        me.paintVigorRegain(point);
        changeVigor(point);
    };
    me.eventVigorLost = function(point) {
        me.paintVigorLost(point);
        changeVigor(-point);
    };
    me.eventEquip = function(card, region) {
        equipped[region] = card;
        removeCard(card);
        me.paintEquip(card, region);
        me.paintCards(cards);
    };
    me.eventUnequip = function(card, region) {
        delete equipped[region];
        me.clearEquip(card, region);
    };
    me.equipment = function(region) {
        return equipped[region];
    };
    me.clickOnEquip = function(region) {
        var card = equipped[region];
        return card && me.clickOnCard(card);
    };

    var method = null;
    me.clickOnTarget = function(target) {};
    me.clickOnCard = function(card) { return false; };
    me.clickOnMethod = function(methodName) {};
    me.hintUseCards = function(methods) {
        var methodsMap = new Array();
        var methodsNames = new Array();
        for (var i in methods) {
            methodsMap[methods[i].name()] = methods[i];
            methodsNames.push(methods[i].name());
        }
        me.onMethodsChanged(methodsNames);

        method = methods[0];
        me.clickOnMethod = function(methodName) {
            return clickOnMethod('action', methodName, 'use', methodsMap);
        };
        me.clickOnTarget = function(target) {
            if (target.selected()) {
                target.deselect();
                return;
            }
            if (method.filterTarget(target, selectedCards(), selectedTargets()))
            {
                target.select();
            }
        };
        me.clickOnCard = function(card) {
            return clickOnCard(method, card);
        };
    };

    me.hintDiscardCards = function(methods) {
        var methodsMap = new Array();
        var methodsNames = new Array();
        for (var i in methods) {
            methodsMap[methods[i].name()] = methods[i];
            methodsNames.push(methods[i].name());
        }
        me.onMethodsChanged(methodsNames);

        method = methods[0];
        me.clickOnMethod = function(methodName) {
            return clickOnMethod('method', methodName, 'discard', methodsMap);
        };
        me.clickOnTarget = function(target) {};
        me.clickOnCard = function(card) {
            return clickOnCard(method, card);
        };
    };

    function clickOnMethod(methodKey, methodName, type, methodsMap) {
        if (method.name() == methodName) {
            var selectedC = selectedCards();
            var selectedT = selectedTargets();
            if (method.validate(selectedC, selectedT)) {
                var cardsIds = new Array();
                for (var i in selectedC) {
                    cardsIds.push(selectedC[i].id);
                }
                var targetsIds = new Array();
                for (var i in selectedT) {
                    targetsIds.push(selectedT[i].id());
                }
                var data = {};
                data[methodKey] = methodName;
                data[type] = cardsIds;
                data['targets'] = targetsIds;
                clearSelectedCards();
                game.clearTargets();
                me.clearMethods();
                me.clickOnCard = function(card) { return false; };
                post_act(data);
            }
            return false;
        }
        method = methodsMap[methodName];
        game.clearTargets();
        clearSelectedCards();
        return true;
    }
    function clickOnCard(method, card) {
        if (card.selected) {
            card.selected = false;
            game.clearTargets();
            return true;
        }
        if (method.filterCard(card, selectedCards(), selectedTargets())) {
            card.selected = true;
            return true;
        }
        return false;
    }
}
