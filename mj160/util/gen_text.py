from mj160.data import load_texture
from arcade import Sprite


def generate_number_sprites(num: int, s_x: int, s_y: int, padding: int = 1):
    LETTER_MAP = {
        "0": {"x": 0, "width": 16, "height": 32},
        "1": {"x": 16, "width": 16, "height": 32},
        "2": {"x": 32, "width": 16, "height": 32},
        "3": {"x": 48, "width": 16, "height": 32},
        "4": {"x": 64, "width": 16, "height": 32},
        "5": {"x": 80, "width": 16, "height": 32},
        "6": {"x": 96, "width": 16, "height": 32},
        "7": {"x": 112, "width": 16, "height": 32},
        "8": {"x": 128, "width": 16, "height": 32},
        "9": {"x": 144, "width": 16, "height": 32},
    }

    num_str = str(num)
    characters = []
    x = s_x
    y = s_y
    for char in num_str:
        tex = load_texture('number_sheet', **LETTER_MAP[char])
        characters.append(Sprite(tex, center_x=x, center_y=y))
        x += padding + tex.width

    return characters