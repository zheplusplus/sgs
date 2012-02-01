from core.src.damage import Damage as CoreDamage

class Damage(CoreDamage):
    def __init__(self, source, target, action, cards, category, point):
        CoreDamage.__init__(self, source, target, action, cards, category,
                            point, source.before_damaging_actions() +
                                   target.before_damaged_actions() +
                                   source.computing_before_damaging +
                                   target.computing_before_damaged,
                            source.after_damaging_actions() +
                            target.after_damaged_actions())
