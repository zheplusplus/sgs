import ext.src.wrappers as wrappers
import ext.src.category_hierarchy as hierarchy

def add_to(player):
    player.cards_used_char = draw_1

@wrappers.as_user
def draw_1(player, flow, gc):
    if hierarchy.is_imm_sleevecards(flow.action):
        gc.deal_cards(player, 1)
