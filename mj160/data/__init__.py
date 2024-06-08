import importlib.resources as pkg_resources

import arcade


import mj160.data.images as imgs
import mj160.data.fonts as fonts
import mj160.data.audio as audio
import mj160.data.shaders as shaders


def load_texture(name, *, fmt: str = "png", **kwargs):
    with pkg_resources.path(imgs, f"{name}.{fmt}") as texture_path:
        return arcade.load_texture(texture_path, **kwargs)


def load_font(name: str) -> None:
    font_name = name + ".ttf"
    with pkg_resources.path(fonts, font_name) as path:

        arcade.text.load_font(path)


def load_audio(name: str, *, streaming: bool = False) -> arcade.Sound:
    audio_name = f"{name}.wav"
    with pkg_resources.path(audio, audio_name) as audio_path:
        return arcade.load_sound(audio_path, streaming=streaming)


def load_shader(name: str):
    shader_name = f"{name}.glsl"
    return pkg_resources.read_text(shaders, shader_name)