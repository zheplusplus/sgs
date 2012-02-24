function SGS_HintParser(game, players, center) {
    function setActivatedPlayers(result) {
        var activated = result['players'];
        for (i in players) {
            players[i].deactivate();
        }
        for (i in activated) {
            players[activated[i]].activate();
        }
    }
    var NAMING_MAPPING = {
        '_SelectCharacter': function(result) {
            setActivatedPlayers(result);
            if ('candidates' in result) {
                center.selectCharacters(result['candidates']);
            }
        }, 'UseCards': function(result) {
            players[result['players'][0]].hintUseCards();
        }, 'DiscardCards': function(result) {
            var require = result['require'];
            function filters() {
                var FILTER_MAPPING = {
                    'count': function(f) {
                        var count = result['count'];
                        return function(c, selected) {
                            return f(c, selected) && selected.length < count;
                        };
                    }, 'candidates': function region(f) {
                        var candidates = result['candidates'];
                        function cardIn(card) {
                            for (i in candidates) {
                                if (card.id == candidates[i]) return true;
                            }
                            return false;
                        }
                        return function(card, s) {
                            return f(card, s) && cardIn(card);
                        };
                    },
                };
                var filter = function(c, s) { return true; };
                for (name in require) {
                    filter = FILTER_MAPPING[require[name]](filter);
                }
                return filter;
            }
            function validators() {
                var VALIDATOR_MAPPING = {
                    'count': function(f) {
                        var count = result['count'];
                        return function(selected) {
                            return f(selected) && selected.length == count;
                        };
                    }, 'candidates': function region(f) {
                        return f;
                    },
                };
                var validator = function(s) { return true; };
                for (name in require) {
                    validator = VALIDATOR_MAPPING[require[name]](validator);
                }
                return validator;
            }
            players[result['players'][0]].hintDiscardCards(
                        filters(), validators(), result['abort'] == 'allow');
        },
    };
    this.hint = function(result) {
        var action = result['action'];
        setActivatedPlayers(result);
        if (action in NAMING_MAPPING) {
            NAMING_MAPPING[action](result);
        }
    };
}
