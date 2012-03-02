function SGS_HintParser(game, center) {
    function setActivatedPlayers(players) {
        game.deactivateAll();
        for (i in players) {
            game.player(players[i]).activate();
        }
    }

    function Method(n, method) {
        this.name = function() {
            return n;
        };

        var filters = new Array();
        this.addFilter = function(f) {
            filters.push(f);
        };
        var validators = new Array();
        this.addValidator = function(f) {
            validators.push(f);
        };

        this.filter = function(card, selected) {
            for (i in filters) {
                if (!filters[i](card, selected)) return false;
            }
            return true;
        };
        this.validate = function(selected) {
            for (i in validators) {
                if (!validators[i](selected)) return false;
            }
            return true;
        };

        var require = method['require'];
        for (i in require) {
            HINT_ITEM_MAPPING[require[i]](this, method);
        }
    }
    function TargetMethod(name, method) {
        var TARGET_FILTER_MAPPING = {
            'fix target': function(method, require) {
                var targetsCand = require['candidates'];
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

        var targetFilters = new Array();
        this.addTargetFilter = function(f) {
            targetFilters.push(f);
        };
        var cardFilters = new Array();
        this.addCardFilter = function(f) {
            cardFilters.push(f);
        };
        var validators = new Array();
        this.addValidator = function(f) {
            validators.push(f);
        };

        this.filterCard = function(card, selCards, selTargets) {
            for (i in cardFilters) {
                if (!cardFilters[i](card, selCards, selTargets)) return false;
            }
            return true;
        };
        this.filterTarget = function(target, selCards, selTargets) {
            for (i in targetFilters) {
                if (!targetFilters[i](target, selCards, selTargets)) {
                    return false;
                }
            }
            return true;
        };
        this.validate = function(selected) {
            for (i in validators) {
                if (!validators[i](selected)) return false;
            }
            return true;
        };

        var require = method['require'];
        for (i in require) {
            TARGET_FILTER_MAPPING[require[i]](this, method);
        }
    }
    function CardMethod(id, cardDesc) {
        var TARGET_FILTER_MAPPING = {
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
            'fix target': function(method, info) {
                var targetsCand = info['candidates'];
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
            },
        };
        this.id = function() {
            return id;
        };

        var targetFilters = new Array();
        this.addTargetFilter = function(f) {
            targetFilters.push(f);
        };
        var cardFilters = new Array();
        this.addCardFilter = function(f) {
            cardFilters.push(f);
        };

        this.filterCard = function(card, selCards, selTargets) {
            for (i in cardFilters) {
                if (!cardFilters[i](card, selCards, selTargets)) return false;
            }
            return true;
        };
        this.filterTarget = function(target, selCards, selTargets) {
            for (i in targetFilters) {
                if (!targetFilters[i](target, selCards, selTargets)) {
                    return false;
                }
            }
            return true;
        };

        TARGET_FILTER_MAPPING[cardDesc['type']](this, cardDesc);
    }
    var HINT_ITEM_MAPPING = {
        'count': function(hint, method) {
            var count = method['count'];
            hint.addFilter(function(c, selected) {
                return selected.length < count;
            });
            hint.addValidator(function(selected) {
                return selected.length == count;
            });
        },
        'candidates': function(hint, method) {
            var cards = method['candidates'];
            function cardIn(card) {
                for (i in cards) {
                    if (card.id == cards[i]) return true;
                }
                return false;
            }
            hint.addFilter(cardIn);
        },
    };
    var NAMING_MAPPING = {
        'select character': function(result) {
            if ('candidates' in result) {
                center.selectCharacters(result['candidates']);
            }
        },
        'use': function(result) {
            function CardMethodsWrapper(cardMethods) {
                this.name = function() {
                    return 'card';
                };

                var method = null;
                this.cleared = function() {
                    method = null;
                };

                this.filterCard = function(card, selCards, selTargets) {
                    if (selCards.length == 1) return false;
                    method = cardMethods[card.id];
                    return method.filterCard(card, selCards, selTargets);
                };
                this.filterTarget = function(target, selCards, selTargets) {
                    if (method == null) {
                        return false;
                    }
                    return method.filterTarget(target, selCards, selTargets);
                };
                this.validate = function(c, t) { return true; };
            }
            var methodInstances = new Array();
            if (result['card']) {
                var cardMethodInstances = {};
                var cardMethods = result['card'];
                for (i in cardMethods) {
                    cardMethodInstances[parseInt(i)] =
                                new CardMethod(parseInt(i), cardMethods[i]);
                }
                methodInstances.push(new CardMethodsWrapper(
                                                cardMethodInstances));
            }

            var methods = result['methods'];
            for (i in methods) {
                methodInstances.push(new TargetMethod(i, methods[i]));
            }

            if (result['abort'] == 'allow') {
                methodInstances.push(new Method('abort', { 'require': [] }));
            }
            game.player(result['players'][0]).hintUseCards(methodInstances);
        },
        'discard': function(result) {
            var methods = result['methods'];
            var methodInstances = new Array();
            for (i in methods) {
                methodInstances.push(new Method(i, methods[i]));
            }
            if (result['abort'] == 'allow') {
                methodInstances.push(new Method('abort', { 'require': [] }));
            }
            game.player(result['players'][0]).hintDiscardCards(methodInstances);
        },
        'region': function(result) {
            if (result['candidates']) {
                game.hintRegions(result['candidates']);
            }
        },
    };
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
