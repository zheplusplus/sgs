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
            players[result['players'][0]].hintDiscardCards(
                        result['count'], function(c) { return true; });
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
