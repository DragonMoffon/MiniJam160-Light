from logging import getLogger
from typing import Callable

from pyglet.input import get_controllers

from arcade import Sprite, SpriteList, Texture, get_window, get_sprites_at_point
from arcade.experimental.input import ActionState
from arcade.experimental.input.manager import InputDevice

from mj160.util import ProceduralAnimator, CLOCK
from mj160.data import load_texture
from mj160.util.procedural_animator import SecondOrderAnimatorKClamped
from mj160.window import DragonWindow

from mj160.game_view import GameView

logger = getLogger("mj160")


class GameLogo(Sprite):

    def __init__(self):
        super().__init__()


class MainMenuButton(Sprite):

    def __init__(self, x: float, y: float, texture: Texture, callback: Callable):
        super().__init__(center_x=x, center_y=y, path_or_texture=texture)
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

    def setup(self):
        self.buttons = SpriteList()

        center = self.window.center

        controllers = get_controllers()
        if controllers and controllers[0] != self.window.input_manager.controller:
            self.window.input_manager.unbind_controller()
            self.window.input_manager.bind_controller(controllers[0])

        start_: MainMenuButton = MainMenuButton(0.0, 0.0, load_texture("menu_sheet", width=64, height=16), lambda: self.window.show_view(GameView()))
        options_: MainMenuButton = MainMenuButton(0.0, -32.0, load_texture("menu_sheet", x=64, width=64, height=16), lambda: logger.error("NOT IMPLEMENTED"))
        quit_: MainMenuButton = MainMenuButton(0.0, -64.0, load_texture("menu_sheet", x=128, width=64, height=16), lambda: self.window.start_close())

        self.buttons.extend((start_, options_, quit_))

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
        if self.selected_button:
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

        if self.window.input_manager.active_device == InputDevice.KEYBOARD:
            mouse_x = self.window.input_manager.axis('player-look_horizontal')
            mouse_y = self.window.input_manager.axis('player-look_vertical')

            mouse_x, mouse_y = self.window.map_to_upscale((mouse_x, mouse_y))
            mouse_x, mouse_y, _ = self.window.upscale_renderer.into_camera.unproject((mouse_x, mouse_y, 0.0))

            collisions = get_sprites_at_point((mouse_x, mouse_y), self.buttons)

            self.select_button(None if not collisions else collisions[-1])
        else:
            if self.selected_button is None:
                self.select_button(self.buttons[0])

    def draw(self):
        if not self.buttons:
            return
        self.buttons.draw(pixelated=True)

    def on_show(self):
        self.window.input_manager.register_action_handler(self.on_action)
        self.window.upscale_renderer.into_camera.position = (0.0, 0.0)
        self.setup()

    def on_hide(self):
        self.window.input_manager.on_action_listeners.remove(self.on_action)
        self.cleanup()
