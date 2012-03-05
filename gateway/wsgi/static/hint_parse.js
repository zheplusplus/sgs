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
            for (i in cardFilters) {
                if (!cardFilters[i](card, selCards, selTargets)) return false;
            }
            return true;
        };
        me.filterTarget = function(target, selCards, selTargets) {
            for (i in targetFilters) {
                if (!targetFilters[i](target, selCards, selTargets))
                    return false;
            }
            return true;
        };
        me.validate = function(selCards, selTargets) {
            for (i in validators) {
                if (!validators[i](selCards, selTargets)) return false;
            }
            return true;
        };
    }

    function DiscardMethod(n, detail) {
        initMethodFiltersValidators(this, n);

        var HINT_ITEM_MAPPING = {
            'count': function(method, detail) {
                var count = detail['count'];
                method.addCardFilter(function(c, selCards, st) {
                    return selCards.length < count;
                });
                method.addValidator(function(selCards, st) {
                    return selCards.length == count;
                });
            },
            'candidates': function(method, detail) {
                var cards = detail['candidates'];
                function cardIn(card, selCards, selTargets) {
                    for (i in cards) {
                        if (card.id == cards[i]) return true;
                    }
                    return false;
                }
                method.addCardFilter(cardIn);
            },
        };

        var require = detail['require'];
        for (i in require) {
            HINT_ITEM_MAPPING[require[i]](this, detail);
        }
    }
    function UseMethod(name, method) {
        initMethodFiltersValidators(this, name);

        var TARGET_FILTER_MAPPING = {
            'fix target': function(method, require) {
                var targetsCand = require['targets'];
                var targetsCount = require['target count'];
                method.addTargetFilter(function(target, c, selTargets) {
                    if (selTargets.length >= targetsCount) {
                        return false;
                    }
                    for (i in targetsCand) {
                        if (target.id() == targetsCand[i]) return true;
                    }
                    return false;
                });
            },
            'cards': function(method, require) {
                var cardsIds = require['cards'];
                method.addCardFilter(function(card, sc, t) {
                    for (i in cardsIds) {
                        if (cardsIds[i] == card.id) return true;
                    }
                    return false;
                });
            },
        };
        this.name = function() {
            return name;
        };

        var require = method['require'];
        for (i in require) {
            TARGET_FILTER_MAPPING[require[i]](this, method);
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

                var TARGET_FILTER_MAPPING = {
                    'forbid': function(method, info) {
                        method.addCardFilter(function(c, selC, t) {
                            return false;
                        });
                    },
                    'implicit target': function(method, info) {
                        method.addTargetFilter(function(t, c, selT) {
                            return false;
                        });
                    },
                    'fix target': function(method, info) {
                        var targetsCand = info['targets'];
                        var targetsCount = info['count'];
                        method.addTargetFilter(function(target, c, selTargets) {
                            if (selTargets.length >= targetsCount) {
                                return false;
                            }
                            for (i in targetsCand) {
                                if (target.id() == targetsCand[i]) return true;
                            }
                            return false;
                        });
                        method.addValidator(function(selCards, selTargets) {
                            return selTargets.length == targetsCount;
                        });
                    },
                };

                TARGET_FILTER_MAPPING[cardDesc['type']](this, cardDesc);
            }
            function CardMethodsWrapper(methodsDetail) {
                initMethod(this, 'card');

                var method = null;
                this.filterCard = function(card, selCards, selTargets) {
                    if (selCards.length == 1) return false;
                    var cardMethod = cardMethods[card.id];
                    if (cardMethod.filterCard(card, selCards, selTargets)) {
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
                for (i in methodsDetail) {
                    cardMethods[parseInt(i)] = new CardMethod(methodsDetail[i]);
                }
            }
            var methodInstances = new Array();
            if (result['card']) {
                methodInstances.push(new CardMethodsWrapper(result['card']));
            }

            var methods = result['methods'];
            for (i in methods) {
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
            for (i in methods) {
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
        for (i in players) {
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
