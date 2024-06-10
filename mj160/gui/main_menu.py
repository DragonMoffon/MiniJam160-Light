from __future__ import annotations
from logging import getLogger
from typing import Callable, TYPE_CHECKING

from pyglet.input import get_controllers

from arcade import Sprite, SpriteList, Texture, get_window, get_sprites_at_point
from arcade.experimental.input import ActionState
from arcade.experimental.input.manager import InputDevice

from mj160.util import ProceduralAnimator, CLOCK, CONFIG
from mj160.data import load_texture
from mj160.util.procedural_animator import SecondOrderAnimatorKClamped

from mj160.game_view import GameView

logger = getLogger("mj160")

if TYPE_CHECKING:
    from mj160.window import DragonWindow


class GameLogo(Sprite):

    def __init__(self):
        super().__init__()


class MainMenuButton(Sprite):

    def __init__(self, x: float, y: float, texture: Texture, callback: Callable):
        super().__init__(center_x=x, center_y=y, path_or_texture=texture)
        self.depth = -1.0
        self.hover_animator: SecondOrderAnimatorKClamped = ProceduralAnimator(2.0, 1.0, 0.5, 1.0, 1.0, 0.0)
        self.target_scale: float = 1.0
        self.clicking = False
        self.selected = False
        self.callback = callback

    def update(self):
        self.scale = self.hover_animator.update(CLOCK.dt, self.target_scale)

    def select(self):
        if self.clicking or self.selected:
            return
        self.selected = True
        self.target_scale = 1.333

    def deselect(self):
        self.selected = False
        self.clicking = False
        self.target_scale = 1.0

    def start_click(self):
        self.clicking = True
        self.target_scale = 1 / 1.333

    def finish_click(self):
        if self.selected:
            self.callback()
        self.deselect()


class MainMenuGui:

    def __init__(self):
        self.window: DragonWindow = get_window()

        self.buttons: SpriteList[MainMenuButton] = None

        self.selected_button: MainMenuButton = None

        self._mouse: Sprite = None

    def setup(self):
        self.buttons = SpriteList()

        self._mouse: Sprite = Sprite(load_texture("game_sheet", y=32, width=16, height=16))
        self._title: Sprite = Sprite(load_texture("menu_sheet", y=256, width=128, height=32), center_x=0.0, center_y=CONFIG['win_resolution'][1]/2.0 - 16)

        controllers = get_controllers()
        if controllers and controllers[0] != self.window.input_manager.controller:
            self.window.input_manager.unbind_controller()
            self.window.input_manager.bind_controller(controllers[0])

        start_: MainMenuButton = MainMenuButton(0.0, 34, load_texture("menu_sheet", width=128, height=32), lambda: self.window.go_to_game())
        options_: MainMenuButton = MainMenuButton(0.0, 1, load_texture("menu_sheet", y=32, width=128, height=32), lambda: self.window.go_to_options())
        info_: MainMenuButton = MainMenuButton(0, -32, load_texture("menu_sheet", y=224, width=128, height=32), lambda: self.window.go_to_splash())
        quit_: MainMenuButton = MainMenuButton(0.0, -66, load_texture("menu_sheet", y=64, width=128, height=32), lambda: self.window.start_close())

        self.buttons.extend((start_, options_, quit_, info_))

    def cleanup(self):
        self.buttons = None

    def select_button(self, button: MainMenuButton):
        if button == self.selected_button:
            return

        if self.selected_button:
            self.selected_button.deselect()

        self.selected_button = button

        if self.selected_button:
            self.selected_button.select()

    def click_button(self):
        if self.selected_button:
            self.selected_button.start_click()

    def release_button(self):
        if self.selected_button and self.selected_button.clicking:
            self.selected_button.finish_click()

    def on_action(self, action: str, state: ActionState):
        if not self.buttons:
            return

        if state == ActionState.PRESSED:
            if action == "gui-select" or action == "gui-left_click":
                self.click_button()
            elif action == "gui-down":
                if self.selected_button is None:
                    self.select_button(self.buttons[0])
                else:
                    idx = (self.buttons.index(self.selected_button) + 1) % len(self.buttons)
                    self.select_button(self.buttons[idx])
            elif action == "gui-up":
                if self.selected_button is None:
                    self.select_button(self.buttons[0])
                else:
                    idx = (self.buttons.index(self.selected_button) - 1) % len(self.buttons)
                    self.select_button(self.buttons[idx])
            return

        if action == "gui-select" or action == "gui-left_click":
            self.release_button()

    def update(self):
        if not self.buttons:
            return
        self.buttons.update()

        if self.selected_button and self.selected_button.clicking:
            return

        if self._mouse:
            look_x, look_y = self.window.input_manager.axis('player-look_horizontal'), self.window.input_manager.axis('player-look_vertical')
            match self.window.input_manager.active_device:
                case InputDevice.KEYBOARD:
                    mouse_x, mouse_y, _ = self.window.upscale_renderer.into_camera.unproject(self.window.map_to_upscale((look_x, look_y)))
                    self._mouse.position = (mouse_x, mouse_y)
                case InputDevice.CONTROLLER:
                    o_pos = self._mouse.position
                    self._mouse.position = o_pos[0] + look_x * CLOCK.dt * CONFIG["controller_look_speed"], o_pos[1] + look_y * CLOCK.dt * CONFIG['controller_look_speed']
            collisions = get_sprites_at_point(self._mouse.position, self.buttons)
            self.select_button(None if not collisions else collisions[-1])

    def draw(self):
        if not self.buttons:
            return
        self.buttons.draw(pixelated=True)
        self._title.draw(pixelated=True)
        self._mouse.draw(pixelated=True)

    def on_show(self):
        self.window.input_manager.register_action_handler(self.on_action)
        self.window.upscale_renderer.into_camera.position = (0.0, 0.0)
        self.setup()

    def on_hide(self):
        self.window.input_manager.on_action_listeners.remove(self.on_action)
        self.cleanup()
