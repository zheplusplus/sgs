function SGS_HintParser(game, players, center) {
    function setActivatedPlayers(result) {
        var activated = result['players'];
        for (i in players) {
            players[i].deactivate();
        }
        for (i in activated) {
            players[i].activate();
        }
    }
    var NAMING_MAPPING = {
        '_SelectCharacter': function(result) {
            setActivatedPlayers(result);
            if ('candidate' in result) {
                center.selectCharacters(result['candidate']);
            }
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
