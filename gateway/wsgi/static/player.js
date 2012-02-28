function SGS_Player(id) {
    var cards_count = 0;
    var max_vigor = 0;
    var vigor = 0;
    var char_name = "";
    var selected = false;

    this.id = function() {
        return id;
    };

    var on_toggle = function(sel) {};
    this.toggle = function() {
        selected = !selected;
        on_toggle(selected);
        return selected;
    };
    this.selected = function() {
        return selected;
    };

    this.onToggle = function(cb) {
        on_toggle = cb;
    };

    var on_cards_count_change = function(before, after) {};
    this.onCardsCountChange = function(cb) {
        on_cards_count_change = cb;
    };

    var on_card_drop = function(c) {};
    this.onCardDrop = function(cb) {
        on_card_drop = cb;
    };

    var on_max_vigor_change = function(before, after, current_vigor) {};
    this.onMaxVigorChange = function(cb) {
        on_max_vigor_change = cb;
    };

    var on_vigor_change = function(before, after, current_max) {};
    this.onVigorChange = function(cb) {
        on_vigor_change = cb;
    };

    var on_name_change = function(before, after) {};
    this.onNameChange = function(cb) {
        on_name_change = cb;
    };

    var on_activated = function() {};
    this.onActivated = function(cb) {
        on_activated = cb;
    };

    var on_deactivated = function() {};
    this.onDeactivated = function(cb) {
        on_deactivated = cb;
    };

    this.activate = function() {
        on_activated();
    };
    this.deactivate = function() {
        on_deactivated();
    };

    this.eventDrawCount = function(count) {
        on_cards_count_change(cards_count, cards_count + count);
        cards_count += count;
    };
    this.eventCharSelected = function(new_name, new_max_vigor) {
        on_name_change(char_name, new_name);
        char_name = new_name;
        on_max_vigor_change(max_vigor, new_max_vigor, vigor);
        max_vigor = new_max_vigor;
        on_vigor_change(vigor, new_max_vigor, max_vigor);
        vigor = new_max_vigor;
    };
    this.eventDiscard = function(c) {
        for (i = 0; i < c.length; ++i) {
            on_card_drop(c[i]);
        }
        on_cards_count_change(cards_count, cards_count - c.length);
        cards_count -= c.length;
    };
    this.eventCardsUsed = function(cards) {
        this.eventDiscard(cards);
    };
    this.eventDamage = function(damage, category) {
        var before = vigor;
        vigor -= damage;
        on_vigor_change(before, vigor, max_vigor);
    };

    this.hintUseCards = function(m) {};
    this.hintDiscardCards = function(m) {}
}

function SGS_Me(game) {
    var cards = new Array();
    var targets = new Array();

    var on_cards_changed = function(cards_after_change) {};
    this.onCardsChanged = function(cb) {
        on_cards_changed = cb;
    };
    var on_card_drop = function(c) {};
    this.onCardDrop = function(cb) {
        on_card_drop = cb;
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
        on_cards_changed(cards);
    }
    this.eventDrawCards = function(new_cards) {
        for (c in new_cards) {
            new_cards[c].selected = false;
        }
        cards = cards.concat(new_cards);
        on_cards_changed(cards);
    };

    var max_vigor = 0;
    var vigor = 0;
    var char_name = "";

    var on_max_vigor_change = function(before, after, current_vigor) {};
    this.onMaxVigorChange = function(cb) {
        on_max_vigor_change = cb;
    };

    var on_vigor_change = function(before, after, current_max) {};
    this.onVigorChange = function(cb) {
        on_vigor_change = cb;
    };

    var on_name_change = function(before, after) {};
    this.onNameChange = function(cb) {
        on_name_change = cb;
    };

    var on_activated = function() {};
    this.onActivated = function(cb) {
        on_activated = cb;
    };

    var on_deactivated = function() {};
    this.onDeactivated = function(cb) {
        on_deactivated = cb;
    };

    this.activate = function() {
        on_activated();
    };
    this.deactivate = function() {
        on_deactivated();
    };
    this.eventCharSelected = function(new_name, new_max_vigor) {
        on_name_change(char_name, new_name);
        char_name = new_name;
        on_max_vigor_change(max_vigor, new_max_vigor, vigor);
        max_vigor = new_max_vigor;
        on_vigor_change(vigor, new_max_vigor, max_vigor);
        vigor = new_max_vigor;
    };
    this.eventDiscard = function(c) {
        for (i = 0; i < c.length; ++i) {
            on_card_drop(c[i]);
            for (j = 0; j < cards.length; ++j) {
                if (c[i].id == cards[j].id) {
                    cards.splice(j, 1);
                    break;
                }
            }
        }
        on_cards_changed(cards);
    };
    this.eventCardsUsed = function(cards) {
        this.eventDiscard(cards);
    };
    this.eventDamage = function(damage, category) {
        var before = vigor;
        vigor -= damage;
        on_vigor_change(before, vigor, max_vigor);
    };

    var on_methods_changed = function(methods) {};
    this.onMethodsChanged = function(cb) {
        on_methods_changed = cb;
    };
    var clear_methods = function() {};
    this.clearMethods = function(cb) {
        clear_methods = cb;
    };

    this.clickOnTarget = function(target) {};
    this.clickOnCard = function(card) {};
    this.clickOnMethod = function(methodName) {};
    function useCards(methods) {
        this.hintUseCards = function(methods) {};
        var methodsMap = new Array();
        var methodsNames = new Array();
        for (i in methods) {
            methodsMap[methods[i].name()] = methods[i];
            methodsNames.push(methods[i].name());
        }
        on_methods_changed(methodsNames);

        var method = methods[0];
        this.clickOnMethod = function(methodName) {
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
                    data[methodName] = cardsIds;
                    data['targets'] = targetsIds;
                    post_act(data);
                    clearSelectedCards();
                    clear_methods();
                    this.clickOnCard = function(card) {};
                    this.hintUseCards = useCards;
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
                target.toggle();
                return;
            }
            if (method.filterTarget(target, selectedCards(), targets)) {
                target.toggle();
                targets.push(target);
            }
        };
        this.clickOnCard = function(card) {
            if (card.selected) {
                card.selected = false;
                on_cards_changed(cards);
                return;
            }
            if (method.filterCard(card, selectedCards(), targets)) {
                card.selected = true;
                on_cards_changed(cards);
            }
        };
    };
    this.hintUseCards = useCards;

    this.hintDiscardCards = function(methods) {
        var methodsMap = new Array();
        var methodsNames = new Array();
        for (i in methods) {
            methodsMap[methods[i].name()] = methods[i];
            methodsNames.push(methods[i].name());
        }
        on_methods_changed(methodsNames);

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
                    data[methodName] = cardsIds;
                    post_act(data);
                    clearSelectedCards();
                    clear_methods();
                    this.clickOnCard = function(card) {};
                }
                return false;
            }
            method = methodsMap[methodName];
            clearSelectedCards();
            return true;
        };
        this.clickOnCard = function(card) {
            if (card.selected) {
                card.selected = false;
                on_cards_changed(cards);
                return;
            }
            if (method.filter(card, selectedCards())) {
                card.selected = true;
                on_cards_changed(cards);
            }
        };
    };
}
