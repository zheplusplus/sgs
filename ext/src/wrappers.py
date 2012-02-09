def as_damage_source(f):
    return lambda p, d, gc: f(p, d, gc) if p == d.source else None

def as_damage_victim(f):
    return lambda p, d, gc: f(p, d, gc) if p == d.victim else None

def alive(f):
    return lambda p, *args, **kwargs: f(p, *args, **kwargs) if p.alive else None
