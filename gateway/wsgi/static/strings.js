SGS_STR_CARD_SUITS = ['', '♠', '♥', '♣', '♦'];
SGS_STR_CARD_SUITS_COLOR = ['#000', '#000', '#f00', '#000', '#f00'];
SGS_STR_CARD_RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J',
                      'Q', 'K'];

function SGS_InternalNameLookup(dict, id) {
    var name = dict[id];
    if (name) return name;
    return id;
}

function SGS_STR_CharName(id) {
    return SGS_InternalNameLookup({
        'Guo Jia': '郭嘉',
        'Zhang Chunhua': '張春華',

        'Zhao Yun': '趙雲',
        'Guan Yu': '關羽',
        'Huang Yueying': '黃月英',
        'Ma Chao': '馬超',
        'Wei Yan': '魏延',

        'Junior Qiao': '小喬',

        'Ma Chao SP': 'SP 馬超',
        'Pang De': '龐德',
    }, id);
}

function SGS_STR_Card(id) {
    return SGS_InternalNameLookup({
        'slash': '殺',
        'dodge': '閃',
        'peach': '桃',

        'duel': '決鬥',
        'fire attack': '火攻',
        'sabotage': '過河拆橋',
        'steal': '順手牽羊',

        'zhangba serpent spear': '丈八蛇矛',
        'rattan armor': '藤甲',
        '-chitu': '赤兔',
        '-dawan': '大宛',
        '-zixing': '紫騂',
        '+dilu': '的盧',
        '+hualiu': '驊騮',
        '+jueying': '絕影',
        '+zhuahuangfeidian': '爪黃飛電',
    }, id);
}

function SGS_STR_Action(id) {
    return SGS_InternalNameLookup({
        'card': '使用',
        'discard': '弃置',
        'show': '展示',
        'abort': '停止',

        'slash': '杀',
        'dodge': '闪',
        'peach': '桃',

        'bequeathed strategy': '遗计',
        'dragon heart': '龙胆',
        'martial saint': '武圣',

        'zhangba serpent spear': '丈八蛇矛',
    }, id);
}

function SGS_STR_Region(id) {
    return SGS_InternalNameLookup({
        'cards': '手牌',
        'weapon': '武器',
        'armor': '防具',
        '-1 horse': '进攻马',
        '+1 horse': '防御马',
    }, id);
}