from ext.src.category_hierarchy import is_slash

def change_slash_range(f, r):
    return lambda action: r if is_slash(action) else f(action)
