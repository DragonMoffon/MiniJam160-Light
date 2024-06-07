from typing import NamedTuple, Generator
from math import sin, pi

from arcade import Sprite, View


class Splash(NamedTuple):
    src: str
    scale: float
    duration: float
    is_growing: bool
    is_pixelated: bool = False
    do_fade_in: bool = True
    do_fade_out: bool = True


SPLASHES = (
    Splash(
        "splash_arcade",
        1.0,
        3.0,
        True
    ),
    Splash(
        "splash_dragon",
        1.0,
        3.0,
        False,
        True
    ),
    Splash(
        "splash_digi",
        0.1,
        3.0,
        False
    )
)


class SplashView(View):

    def __init__(self, next_view: type):
        super().__init__()
        self._next = next_view

        self._splash_sprite: Sprite = None
        self._splash_timer: float = 0.0
        self._current_splash: Splash = None
        self._splashes: Generator[Splash] = (splash for splash in SPLASHES)

    def leave(self):
        self._splash_sprite = None
        self.window.show_view(self._next())
        return

    def _next_splash(self):
        self._current_splash = next(self._splashes, None)

        if self._current_splash is None:
            return self.leave()

        self._splash_timer = 0.0

        self._splash_sprite.scale = self._current_splash.scale
        self._splash_sprite.texture = get_texture(self._current_splash.src)
        self._splash_sprite.scale = self._current_splash.scale
        self._splash_sprite.alpha = 255 * (not self._current_splash.do_fade_in)

    def on_show_view(self):
        super().on_show_view()
        self._splash_sprite = Sprite()
        self._next_splash()

    def on_key_release(self, symbol: int, modifiers: int):
        self._current_splash = None
        self.leave()
        return super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float):
        if self._current_splash is None:
            return

        self._splash_timer += delta_time

        if self._splash_timer >= self._current_splash.duration:
            self._next_splash()
            return

        self._splash_sprite.position = self.window.center

        splash_fraction = self._splash_timer / self._current_splash.duration

        if self._current_splash.is_growing:
            self._splash_sprite.scale = self._current_splash.scale + splash_fraction * 0.25

        fade_fraction = min(0.5 + 0.5 * self._current_splash.do_fade_out, max(0.5 - 0.5 * self._current_splash.do_fade_in, splash_fraction))
        self._splash_sprite.alpha = int(255 * sin(pi * fade_fraction))

    def on_draw(self):
        self.clear()

        if self._current_splash is None:
            return

        self._splash_sprite.draw(pixelated=self._current_splash.is_pixelated)
