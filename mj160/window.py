from __future__ import annotations

from typing import Optional, Tuple

from arcade import Window, View
from arcade.experimental.input.manager import InputManager, InputDevice
from arcade.types import RGBOrA255, RGBANormalized

from mj160.util.config import CONFIG
from mj160.util.splash import SplashView
from mj160.util.clock import CLOCK
from mj160.util.input import setup_input
from mj160.light_state import LightState


from mj160.util.upscale_fbo import UpscaleFBO


class DragonView(View):

    def __init__(self):
        super().__init__()


class DragonWindow(Window):

    def __init__(self, next_view: type[DragonView]):
        w, h = CONFIG['win_min_size']
        super().__init__(w, h, CONFIG['win_name'], fullscreen=CONFIG['win_fullscreen'], center_window=True,
                         update_rate=CONFIG['game_fps'], draw_rate=CONFIG['game_dps'], vsync=True)
        LightState.initialise()
        self.input_manager: InputManager = InputManager()
        setup_input(self.input_manager)

        self.upscale_renderer: UpscaleFBO = UpscaleFBO()

        self.upscale_renderer.use()
        self.show_view(SplashView(next_view))

        self.set_mouse_visible(False)

        self.closing = False
        self._next_view: type[DragonView] = None
        self._next_view_args: tuple = ()
        self._next_view_kwargs: dict = {}

    def on_mouse_enter(self, x: int, y: int):
        self.set_mouse_visible(False)

    def start_close(self):
        self.closing = True

    def next_view(self, view: type[DragonView], *args, **kwargs):
        self._next_view = view
        self._next_view_args = args
        self._next_view_kwargs = kwargs

    def clear(
        self,
        color: Optional[RGBOrA255] = None,
        color_normalized: Optional[RGBANormalized] = None,
        viewport: Optional[Tuple[int, int, int, int]] = None,
    ):
        super().clear(color, color_normalized, viewport)
        self.upscale_renderer.clear()

    def _dispatch_updates(self, delta_time: float):
        CLOCK.tick(delta_time)
        self.input_manager.update()
        super()._dispatch_updates(delta_time)

        if self.closing:
            self.close()

        if self._next_view is not None:
            self.show_view(self._next_view(*self._next_view_args, **self._next_view_kwargs))
            self._next_view = None

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.input_manager.active_device = InputDevice.KEYBOARD

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.input_manager.active_device = InputDevice.KEYBOARD

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.input_manager.active_device = InputDevice.KEYBOARD

    def show_view(self, new_view: 'View'):
        super().show_view(new_view)
        self.upscale_renderer.use()

    def on_draw(self):
        self.upscale_renderer.display()

    def map_to_upscale(self, raw_mouse_pos: Tuple[float, float]):
        # All the window mouse events are for the actual size of the window
        # This maps them to the size of the upscale fbo, and accounts for any pixel perfect borders
        # Still need to map to world coordinates from here

        x = (raw_mouse_pos[0] - self.upscale_renderer.display_camera.viewport.left) / self.upscale_renderer.display_camera.viewport.width
        y = (raw_mouse_pos[1] - self.upscale_renderer.display_camera.viewport.bottom) / self.upscale_renderer.display_camera.viewport.height

        return x * self.upscale_renderer.into_camera.viewport.width, y * self.upscale_renderer.into_camera.viewport.height
