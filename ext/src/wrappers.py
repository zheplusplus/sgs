from core.src import ret_code

def as_damage_source(f):
    return lambda p, d, gc: f(p, d, gc) if p == d.source else None

def as_damage_victim(f):
    return lambda p, d, gc: f(p, d, gc) if p == d.victim else None

def as_user(f):
    return lambda p, flow, gc: f(p, flow, gc) if p == flow.user else None

def as_target(f):
    return lambda p, flow, gc: f(p, flow, gc) if p == flow.target else None

def alive(f):
    return lambda p, *args, **kwargs: f(p, *args, **kwargs) if p.alive else None

def invoke_on_success(player, skill):
    def wrapper(f):
        def invoke(gc, args):
            result = f(gc, args)
            if result['code'] == ret_code.OK:
                gc.invoke(player, skill)
            return result
        return invoke
    return wrapper
