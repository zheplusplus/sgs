function SGS_HintParser(game, center) {
    function initMethod(me, n) {
        me.name = function() {
            return n;
        };
    }
    function AbortMethod() {
        initMethod(this, 'abort');

        this.filterCard = function(c, sc, st) {
            return false;
        };
        this.filterTarget = function(t, sc, st) {
            return false;
        };
        this.validate = function(sc, st) {
            return true;
        };
    }

    function initMethodFiltersValidators(me, n) {
        initMethod(me, n);

        var targetFilters = new Array();
        me.addTargetFilter = function(f) {
            targetFilters.push(f);
        };
        var cardFilters = new Array();
        me.addCardFilter = function(f) {
            cardFilters.push(f);
        };
        var validators = new Array();
        me.addValidator = function(f) {
            validators.push(f);
        };

        me.filterCard = function(card, selCards, selTargets) {
            for (var i in cardFilters) {
                if (!cardFilters[i](card, selCards, selTargets)) return false;
            }
            return true;
        };
        me.filterTarget = function(target, selCards, selTargets) {
            for (var i in targetFilters) {
                if (!targetFilters[i](target, selCards, selTargets))
                    return false;
            }
            return true;
        };
        me.validate = function(selCards, selTargets) {
            for (var i in validators) {
                if (!validators[i](selCards, selTargets)) return false;
            }
            return true;
        };
    }

    var RESTRICTION_MAPPER = {
        'forbid': function(method, info) {
            method.addCardFilter(function(c, selC, t) {
                return false;
            });
            method.addTargetFilter(function(t, c, selT) {
                return false;
            });
        },
        'implicit target': function(method, info) {
            method.addTargetFilter(function(t, c, selT) {
                return false;
            });
        },
        'fix target': function(method, detail) {
            var targetsCand = detail['targets'];
            var targetsCount = detail['target count'];
            method.addTargetFilter(function(target, c, selTargets) {
                if (selTargets.length >= targetsCount) {
                    return false;
                }
                for (var i in targetsCand) {
                    if (target.id() == targetsCand[i]) return true;
                }
                return false;
            });
            method.addValidator(function(sc, selTargets) {
                return selTargets.length == targetsCount;
            });
        },
        'fix card count': function(method, detail) {
            var cardsIds = detail['cards'];
            var cardsCount = detail['card count'];
            method.addCardFilter(function(card, selCards, t) {
                if (selCards.length == cardsCount) return false;
                for (var i in cardsIds) {
                    if (cardsIds[i] == card.id) return true;
                }
                return false;
            });
            method.addValidator(function(selCards, st) {
                return selCards.length == cardsCount;
            });
        },
        'min card count': function(method, detail) {
            var cardsIds = detail['cards'];
            var cardsCount = detail['card count'];
            method.addCardFilter(function(card, selCards, t) {
                for (var i in cardsIds) {
                    if (cardsIds[i] == card.id) return true;
                }
                return false;
            });
            method.addValidator(function(selCards, st) {
                return cardsCount <= selCards.length;
            });
        },
    };

    function DiscardMethod(n, detail) {
        initMethodFiltersValidators(this, n);
        var require = detail['require'];
        for (var i in require) {
            RESTRICTION_MAPPER[require[i]](this, detail);
        }
    }
    function UseMethod(name, method) {
        initMethodFiltersValidators(this, name);
        this.name = function() {
            return name;
        };
        var require = method['require'];
        for (var i in require) {
            RESTRICTION_MAPPER[require[i]](this, method);
        }
    }

    var NAMING_MAPPING = {
        'select character': function(result) {
            if ('candidates' in result) {
                center.selectCharacters(result['candidates']);
            }
        },
        'use': function(result) {
            function CardMethod(cardDesc) {
                initMethodFiltersValidators(this, null);
                RESTRICTION_MAPPER[cardDesc['type']](this, cardDesc);
            }
            function CardMethodsWrapper(methodsDetail) {
                initMethod(this, 'card');

                var method = null;
                this.filterCard = function(card, selCards, selTargets) {
                    if (selCards.length == 1) return false;
                    var cardMethod = cardMethods[card.id];
                    if (cardMethod &&
                        cardMethod.filterCard(card, selCards, selTargets))
                    {
                        method = cardMethod;
                        return true;
                    }
                    return false;
                };
                this.filterTarget = function(target, selCards, selTargets) {
                    if (selCards.length == 0) {
                        return false;
                    }
                    return method.filterTarget(target, selCards, selTargets);
                };
                this.validate = function(selCards, selTargets) {
                    if (selCards.length != 1) {
                        return false;
                    }
                    return cardMethods[selCards[0].id].validate(selCards,
                                                                selTargets);
                };

                var cardMethods = {};
                for (var i in methodsDetail) {
                    cardMethods[parseInt(i)] = new CardMethod(methodsDetail[i]);
                }
            }
            var methodInstances = new Array();
            if (result['card']) {
                methodInstances.push(new CardMethodsWrapper(result['card']));
            }

            var methods = result['methods'];
            for (var i in methods) {
                methodInstances.push(new UseMethod(i, methods[i]));
            }

            if (result['abort'] == 'allow') {
                methodInstances.push(new AbortMethod());
            }
            game.player(result['players'][0]).hintUseCards(methodInstances);
        },
        'discard': function(result) {
            var methods = result['methods'];
            var methodInstances = new Array();
            for (var i in methods) {
                methodInstances.push(new DiscardMethod(i, methods[i]));
            }
            if (result['abort'] == 'allow') {
                methodInstances.push(new AbortMethod());
            }
            game.player(result['players'][0]).hintDiscardCards(methodInstances);
        },
        'region': function(result) {
            if (result['regions']) {
                game.hintRegions(result['regions']);
            }
        },
    };

    function setActivatedPlayers(players) {
        game.deactivateAll();
        for (var i in players) {
            game.player(players[i]).activate();
        }
    }

    var lastHint;
    this.hint = function(result) {
        if (JSON.stringify(result) == JSON.stringify(lastHint)) {
            return;
        }
        lastHint = result;
        setActivatedPlayers(result['players']);
        var action = result['action'];
        if (action in NAMING_MAPPING) {
            NAMING_MAPPING[action](result);
        }
    };
}
