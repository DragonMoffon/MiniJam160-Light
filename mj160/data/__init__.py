import importlib.resources as pkg_resources

import arcade


import mj160.data.images as imgs
import mj160.data.fonts as fonts


def load_texture(name, *, fmt: str = "png", **kwargs):
    with pkg_resources.path(imgs, f"{name}.{fmt}") as texture_path:
        return arcade.load_texture(texture_path, **kwargs)


def load_font(name: str) -> None:
    font_name = name + ".ttf"
    with pkg_resources.path(fonts, font_name) as path:
        arcade.text.load_font(path)
