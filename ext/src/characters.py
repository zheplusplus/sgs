from ext.src.skills import bequeathed_strategy, merciless, dragon_heart,       \
                           martial_saint, prodigy, horsemanship, fury_pith,    \
                           heavenly_scent, youth_beauty, surprise_raid,        \
                           intellect_gathering

class Character:
    def __init__(self, name, vigor, character_skills):
        self.name = name
        self.skills = character_skills
        self.vigor = vigor

    def select(self, player):
        player.character_name = self.name
        for s in self.skills: s.add_to(player)
        player.max_vigor = self.vigor
        player.vigor = self.vigor

ALL = (
    Character('Guo Jia', 3, [bequeathed_strategy]),
    Character('Zhang Chunhua', 3, [merciless]),

    Character('Zhao Yun', 4, [dragon_heart]),
    Character('Guan Yu', 4, [martial_saint]),
    Character('Huang Yueying', 3, [prodigy, intellect_gathering]),
    Character('Ma Chao', 4, [horsemanship]),
    Character('Wei Yan', 4, [fury_pith]),

    Character('Gan Ning', 4, [surprise_raid]),
    Character('Junior Qiao', 3, [heavenly_scent, youth_beauty]),

    Character('Ma Chao SP', 4, [horsemanship]),
    Character('Pang De', 4, [horsemanship]),
)
