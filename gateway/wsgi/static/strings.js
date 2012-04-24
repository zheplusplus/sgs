SGS_STR_CARD_SUITS = ['', '♠', '♥', '♣', '♦'];
SGS_STR_CARD_SUITS_COLOR = ['#000', '#000', '#f00', '#000', '#f00'];
SGS_STR_CARD_RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J',
                      'Q', 'K'];
SGS_STR_DEATH = '阵亡';

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
        'Gan Ning': '甘宁',

        'Ma Chao SP': 'SP 馬超',
        'Pang De': '龐德',
    }, id);
}

function SGS_STR_Card(id) {
    return SGS_InternalNameLookup({
        'slash': '殺',
        'thunder slash': '雷殺',
        'fire slash': '火殺',
        'dodge': '閃',
        'peach': '桃',

        'duel': '決鬥',
        'arson attack': '火攻',
        'sabotage': '過河拆橋',
        'steal': '順手牽羊',

        'zhangba serpent spear': '丈八蛇矛',
        'vermilion feather fan': '朱雀羽扇',
        'rattan armor': '藤甲',
        '-chitu': '赤兔 (-1)',
        '-dawan': '大宛 (-1)',
        '-zixing': '紫騂 (-1)',
        '+dilu': '的盧 (+1)',
        '+hualiu': '驊騮 (+1)',
        '+jueying': '絕影 (+1)',
        '+zhuahuangfeidian': '爪黃飛電 (+1)',
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
        'martial saint:onhand': '武圣 (手牌)',
        'martial saint:weapon': '武圣 (武器)',
        'martial saint:armor': '武圣 (防具)',
        'martial saint:-1 horse': '武圣 (进攻马)',
        'martial saint:+1 horse': '武圣 (防御马)',
        'heavenly scent': '天香',
        'surprise raid': '奇袭',

        'zhangba serpent spear': '丈八蛇矛',
        'vermilion feather fan': '朱雀羽扇',
        'rattan armor': '藤甲',
    }, id);
}

function SGS_STR_Region(id) {
    return SGS_InternalNameLookup({
        'onhand': '手牌',
        'weapon': '武器',
        'armor': '防具',
        '-1 horse': '进攻马',
        '+1 horse': '防御马',
    }, id);
}
