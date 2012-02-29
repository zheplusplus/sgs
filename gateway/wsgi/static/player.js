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

    me.eventDrawCount = function(count) {
        me.onCardsCountChanged(cards_count, cards_count + count);
        cards_count += count;
    };
    me.eventDiscardCount = function(count) {
        me.onCardsCountChanged(cards_count, cards_count - count);
        cards_count -= count;
    };
    me.eventCharSelected = function(new_name, new_max_vigor) {
        me.onCharNameChanged(char_name, new_name);
        char_name = new_name;
        me.onMaxVigorChanged(max_vigor, new_max_vigor, vigor);
        max_vigor = new_max_vigor;
        me.onVigorChanged(vigor, new_max_vigor, max_vigor);
        vigor = new_max_vigor;
    };
    me.eventDiscard = function(c) {
        for (i = 0; i < c.length; ++i) {
            me.onCardDropped(c[i]);
        }
        me.onCardsCountChanged(cards_count, cards_count - c.length);
        cards_count -= c.length;
    };
    me.eventCardsUsed = function(cards) {
        me.eventDiscard(cards);
    };
    me.eventDamage = function(damage, category) {
        var before = vigor;
        vigor -= damage;
        me.onVigorChanged(before, vigor, max_vigor);
    };

    me.hintUseCards = function(m) {};
    me.hintDiscardCards = function(m) {};
}

function SGS_InitMe(id, me, game, players) {
    var cards = new Array();
    var targets = players;
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

    function selectedCards() {
        var c = new Array();
        for (i in cards) {
            if (cards[i].selected) c.push(cards[i]);
        }
        return c;
    }
    function selectedTargets() {
        var t = new Array();
        for (i in targets) {
            if (targets[i].selected()) t.push(targets[i]);
        }
        return t;
    }

    function clearSelectedCards() {
        for (i in cards) {
            cards[i].selected = false;
        }
    }

    me.eventDrawCards = function(new_cards) {
        for (c in new_cards) {
            new_cards[c].selected = false;
        }
        cards = cards.concat(new_cards);
        me.onCardsChanged(cards);
    };

    var max_vigor = 0;
    var vigor = 0;
    var char_name = "";

    me.eventCharSelected = function(new_name, new_max_vigor) {
        me.onCharNameChanged(char_name, new_name);
        char_name = new_name;
        me.onMaxVigorChanged(max_vigor, new_max_vigor, vigor);
        max_vigor = new_max_vigor;
        me.onVigorChanged(vigor, new_max_vigor, max_vigor);
        vigor = new_max_vigor;
    };
    me.eventDiscard = function(c) {
        for (i = 0; i < c.length; ++i) {
            me.onCardDropped(c[i]);
            for (j = 0; j < cards.length; ++j) {
                if (c[i].id == cards[j].id) {
                    cards.splice(j, 1);
                    break;
                }
            }
        }
        me.onCardsChanged(cards);
    };
    me.eventCardsUsed = function(cards) {
        this.eventDiscard(cards);
    };
    me.eventDamage = function(damage, category) {
        var before = vigor;
        vigor -= damage;
        me.onVigorChanged(before, vigor, max_vigor);
    };

    me.clickOnTarget = function(target) {};
    me.clickOnCard = function(card) {};
    me.clickOnMethod = function(methodName) {};
    function useCards(methods) {
        me.hintUseCards = function(methods) {};
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
                    post_act(data);
                    clearSelectedCards();
                    me.clearMethods();
                    me.clickOnCard = function(card) {};
                    me.hintUseCards = useCards;
                }
                return false;
            }
            method = methodsMap[methodName];
            targets.length = 0;
            game.clearTargets();
            clearSelectedCards();
            return true;
        };
        this.clickOnTarget = function(target) {
            if (target.selected()) {
                target.deselect();
                return;
            }
            if (method.filterTarget(target, selectedCards(), selectedTargets()))
            {
                target.select();
            }
        };
        this.clickOnCard = function(card) {
            if (card.selected) {
                card.selected = false;
                me.onCardsChanged(cards);
                return;
            }
            if (method.filterCard(card, selectedCards(), targets)) {
                card.selected = true;
                me.onCardsChanged(cards);
            }
        };
    };
    me.hintUseCards = useCards;

    function discardCards(methods) {
        me.hintDiscardCards = function(m) {};
        var methodsMap = new Array();
        var methodsNames = new Array();
        for (i in methods) {
            methodsMap[methods[i].name()] = methods[i];
            methodsNames.push(methods[i].name());
        }
        me.onMethodsChanged(methodsNames);

        var method = methods[0];
        this.clickOnMethod = function(methodName) {
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
                    post_act(data);
                    clearSelectedCards();
                    me.clearMethods();
                    me.clickOnCard = function(card) {};
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
    me.hintDiscardCards = discardCards;
}
