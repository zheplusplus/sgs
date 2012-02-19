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
            if ('candidate' in result) {
                center.selectCharacters(result['candidate']);
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
                    }, 'region': function region(f) {
                        var region = result['region'];
                        return function(card, s) {
                            return f(card, s) && card.region == region;
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
                    }, 'region': function region(f) {
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
                        filters(), validators(), result['give up'] == 'allow');
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
