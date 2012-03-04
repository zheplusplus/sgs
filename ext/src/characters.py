from ext.src.skills import bequeathed_strategy, merciless, dragon_heart,       \
                           martial_saint, prodigy, horsemanship, fury_pith,    \
                           heavenly_scent, youth_beauty

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

GUO_JIA = Character('Guo Jia', 3, [bequeathed_strategy])
ZHANG_CHUNHUA = Character('Zhang Chunhua', 3, [merciless])

ZHAO_YUN = Character('Zhao Yun', 4, [dragon_heart])
GUAN_YU = Character('Guan Yu', 4, [martial_saint])
HUANG_YUEYING = Character('Huang Yueying', 3, [prodigy])
MA_CHAO = Character('Ma Chao', 4, [horsemanship])
WEI_YAN = Character('Wei Yan', 4, [fury_pith])

JUNIOR_QIAO = Character('Junior Qiao', 3, [heavenly_scent, youth_beauty])

MA_CHAO_SP = Character('Ma Chao SP', 4, [horsemanship])
PANG_DE = Character('Pang De', 4, [horsemanship])

ALL = [GUO_JIA, ZHANG_CHUNHUA, ZHAO_YUN, GUAN_YU, HUANG_YUEYING, MA_CHAO,
       WEI_YAN, JUNIOR_QIAO, MA_CHAO_SP, PANG_DE]
