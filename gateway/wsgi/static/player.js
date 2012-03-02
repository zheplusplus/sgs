function SGS_InitPlayer(me, id) {
    var cards_count = 0;
    var max_vigor = 0;
    var vigor = 0;
    var char_name = "";
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

    me.eventCharSelected = function(new_name, new_max_vigor) {
        me.onCharNameChanged(char_name, new_name);
        char_name = new_name;
        me.onMaxVigorChanged(max_vigor, new_max_vigor, vigor);
        max_vigor = new_max_vigor;
        me.onVigorChanged(vigor, new_max_vigor, max_vigor);
        vigor = new_max_vigor;
    };
    me.eventKilled = function() {
        me.onKilled();
    };

    function changeCardsCount(delta) {
        var before = cards_count;
        cards_count += delta;
        me.onCardsCountChanged(before, cards_count);
    }
    me.eventDrawCount = function(count) {
        me.paintDrawCount(count);
        changeCardsCount(count);
    };
    me.eventChangeCount = function(count) {
        changeCardsCount(count);
    };
    me.eventDiscard = function(c) {
        var cardsCount = 0;
        for (i = 0; i < c.length; ++i) {
            me.paintCardDropped(c[i]);
            if (c[i].region == 'cards') cardsCount += 1;
        }
        changeCardsCount(-cardsCount);
    };
    me.eventUseCards = function(cards, targets) {
        me.onUseCards(cards, targets);
        changeCardsCount(-cards.length);
    };
    me.eventPlayCards = function(cards) {
        me.onPlayCards(cards);
        changeCardsCount(-cards.length);
    };
    me.eventShowCards = function(cards) {
        me.onShowCards(cards);
    };

    function changeVigor(delta) {
        var before = vigor;
        vigor += delta;
        me.onVigorChanged(before, vigor, max_vigor);
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
        me.clearEquip(region);
    };

    me.hintUseCards = function(m) {};
    me.hintDiscardCards = function(m) {};
}

function SGS_InitMe(id, me, game, players) {
    var cards = new Array();
    var max_vigor = 0;
    var vigor = 0;
    var char_name = "";
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

    function selectedCards() {
        var c = new Array();
        for (i in cards) {
            if (cards[i].selected) c.push(cards[i]);
        }
        return c;
    }
    function selectedTargets() {
        var t = new Array();
        for (i in players) {
            if (players[i].selected()) t.push(players[i]);
        }
        return t;
    }

    function clearSelectedCards() {
        for (i in cards) {
            cards[i].selected = false;
        }
        me.onCardsChanged(cards);
    }

    function removeCard(card) {
        for (j = 0; j < cards.length; ++j) {
            if (card.id == cards[j].id) {
                cards.splice(j, 1);
                return;
            }
        }
    }
    function removeCards(cards) {
        for (i in cards) {
            removeCard(cards[i]);
        }
    }

    me.eventCharSelected = function(new_name, new_max_vigor) {
        me.onCharNameChanged(char_name, new_name);
        char_name = new_name;
        me.onMaxVigorChanged(max_vigor, new_max_vigor, vigor);
        max_vigor = new_max_vigor;
        me.onVigorChanged(vigor, new_max_vigor, max_vigor);
        vigor = new_max_vigor;
    };
    me.eventKilled = function() {
        me.onKilled();
    };

    me.eventDrawCards = function(new_cards) {
        for (c in new_cards) {
            new_cards[c].selected = false;
        }
        cards = cards.concat(new_cards);
        me.paintDrawCards(new_cards);
        me.onCardsChanged(cards);
    };
    me.eventDiscard = function(c) {
        removeCards(c);
        me.paintDiscardCards(c);
        me.onCardsChanged(cards);
    };
    me.eventUseCards = function(c, targets) {
        removeCards(c);
        me.paintUseCards(c, targets);
        me.onCardsChanged(cards);
    };
    me.eventPlayCards = function(c) {
        removeCards(c);
        me.paintPlayCards(c);
        me.onCardsChanged(cards);
    };
    me.eventShowCards = function(c) {
        me.paintShowCards(c);
    };

    function changeVigor(delta) {
        var before = vigor;
        vigor += delta;
        me.onVigorChanged(before, vigor, max_vigor);
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
        me.onCardsChanged(cards);
    };
    me.eventUnequip = function(card, region) {
        delete equipped[region];
        me.clearEquip(region);
    };
    me.equipment = function() {
        return equipped;
    };

    me.clickOnTarget = function(target) {};
    me.clickOnCard = function(card) {};
    me.clickOnMethod = function(methodName) {};
    me.hintUseCards = function(methods) {
        var methodsMap = new Array();
        var methodsNames = new Array();
        for (i in methods) {
            methodsMap[methods[i].name()] = methods[i];
            methodsNames.push(methods[i].name());
        }
        me.onMethodsChanged(methodsNames);

        var method = methods[0];
        me.clickOnMethod = function(methodName) {
            if (method.name() == methodName) {
                var selectedC = selectedCards();
                var selectedT = selectedTargets();
                if (method.validate(selectedC, selectedT)) {
                    var cardsIds = new Array();
                    for (i in selectedC) {
                        cardsIds.push(selectedC[i].id);
                    }
                    var targetsIds = new Array();
                    for (i in selectedT) {
                        targetsIds.push(selectedT[i].id());
                    }
                    var data = {};
                    data['action'] = methodName;
                    data['use'] = cardsIds;
                    data['targets'] = targetsIds;
                    clearSelectedCards();
                    me.clearMethods();
                    me.clickOnCard = function(card) {};
                    post_act(data);
                }
                return false;
            }
            method = methodsMap[methodName];
            game.clearTargets();
            clearSelectedCards();
            return true;
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
            if (card.selected) {
                card.selected = false;
                me.onCardsChanged(cards);
                return;
            }
            if (method.filterCard(card, selectedCards(), selectedTargets())) {
                card.selected = true;
                me.onCardsChanged(cards);
            }
        };
    };

    me.hintDiscardCards = function(methods) {
        var methodsMap = new Array();
        var methodsNames = new Array();
        for (i in methods) {
            methodsMap[methods[i].name()] = methods[i];
            methodsNames.push(methods[i].name());
        }
        me.onMethodsChanged(methodsNames);

        var method = methods[0];
        me.clickOnMethod = function(methodName) {
            if (method.name() == methodName) {
                var selected = selectedCards();
                if (method.validate(selected)) {
                    var cardsIds = new Array();
                    for (i in selected) {
                        cardsIds.push(selected[i].id);
                    }
                    var data = {};
                    data['method'] = methodName;
                    data['discard'] = cardsIds;
                    clearSelectedCards();
                    me.clearMethods();
                    me.clickOnCard = function(card) {};
                    post_act(data);
                }
                return false;
            }
            method = methodsMap[methodName];
            clearSelectedCards();
            return true;
        };
        me.clickOnCard = function(card) {
            if (card.selected) {
                card.selected = false;
                me.onCardsChanged(cards);
                return;
            }
            if (method.filter(card, selectedCards())) {
                card.selected = true;
                me.onCardsChanged(cards);
            }
        };
    };
}
