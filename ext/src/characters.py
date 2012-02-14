from ext.src.skills import bequeathed_strategy, merciless, dragon_heart,       \
                           martial_saint, prodigy, horsemanship, fury_pith,    \
                           heavenly_scent

class Character:
    def __init__(self, name, character_skills):
        self.name = name
        self.skills = character_skills

    def select(self, player):
        player.character_name = self.name
        for s in self.skills: s.add_to(player)

DEFAULT = Character('Default', [])

GUO_JIA = Character('Guo Jia', [bequeathed_strategy])
ZHANG_CHUNHUA = Character('Zhang Chunhua', [merciless])

ZHAO_YUN = Character('Zhao Yun', [dragon_heart])
GUAN_YU = Character('Guan Yu', [martial_saint])
HUANG_YUEYING = Character('Huang Yueying', [prodigy])
MA_CHAO = Character('Ma Chao', [horsemanship])
WEI_YAN = Character('Wei Yan', [fury_pith])

JUNIOR_QIAO = Character('Junior Qiao', [heavenly_scent])

MA_CHAO_SP = Character('Ma Chao SP', [horsemanship])
PANG_DE = Character('Pang De', [horsemanship])

ALL = [GUO_JIA, ZHANG_CHUNHUA, ZHAO_YUN, GUAN_YU, HUANG_YUEYING, MA_CHAO,
       WEI_YAN, JUNIOR_QIAO, MA_CHAO_SP, PANG_DE]
