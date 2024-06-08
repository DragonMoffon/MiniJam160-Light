from __future__ import annotations

from typing import TYPE_CHECKING
from logging import getLogger

from pyglet.math import Vec2

from arcade import Sprite, SpriteList, get_window, Window
from arcade.experimental.input import ActionState
from arcade.experimental.input.manager import InputDevice

from mj160.run_state import RunState
from mj160.light_state import LightState, Light
from mj160.window import DragonWindow
from mj160.util import CLOCK, CONFIG, ProceduralAnimator
from mj160.data import load_texture

if TYPE_CHECKING:
    from mj160.player_state import PlayerState

logger = getLogger("mj160")


class Player:

    def __init__(self, state: PlayerState):
        self._state: PlayerState = state

        self._is_enabled: bool = False
        self._window: DragonWindow = get_window()

        self._renderer: SpriteList = SpriteList()
        self._body_sprite: Sprite = Sprite(load_texture("game_sheet", y=16, width=16, height=16))
        self._body_sprite.depth = -0.5
        self._torch_sprite: Sprite = Sprite(load_texture("game_sheet", y=32, width=16, height=16))
        self._torch_sprite.depth = -0.5

        self._renderer.extend((self._body_sprite, self._torch_sprite))

        self._last_move: float = 0.0

        self._camera_animator: ProceduralAnimator = ProceduralAnimator(2.0, 1.0, 0.5, Vec2(0.0, 0.0), Vec2(0.0, 0.0), Vec2(0.0, 0.0))

    @property
    def body(self):
        return self._body_sprite

    @property
    def torch(self):
        return self._torch_sprite

    def spawn(self):
        if not RunState.floor:
            return

        self._state.x, self._state.y = RunState.floor.spawn_point()
        self._body_sprite.position = RunState.floor.move(self._state.x, self._state.y)

    def enable(self):
        if self._is_enabled:
            return
        self._is_enabled = True
        self._window.input_manager.register_action_handler(self.on_action)
        self._window.push_handlers(on_update=self.update, on_draw=self.draw)

    def disable(self):
        if not self._is_enabled:
            return
        self._is_enabled = False
        self._window.input_manager.on_action_listeners.remove(self.on_action)
        self._window.remove_handlers(on_update=self.update, on_draw=self.draw)

    def on_action(self, action: str, state: ActionState):
        pass

    def update(self, dt: float):
        self._window.upscale_renderer.into_camera.position = self._camera_animator.update(CLOCK.dt, Vec2(*self._body_sprite.position))

        input_manager = self._window.input_manager
        look_x, look_y = input_manager.axis("player-look_horizontal"), input_manager.axis("player-look_vertical")
        match input_manager.active_device:
            case InputDevice.KEYBOARD:
                mouse_x, mouse_y, _ = self._window.upscale_renderer.into_camera.unproject(self._window.map_to_upscale((look_x, look_y)))
                diff = Vec2(mouse_x - self._body_sprite.center_x, mouse_y - self._body_sprite.center_y)

            case InputDevice.CONTROLLER:
                diff = Vec2(self._state.aim.x + look_x * CONFIG['controller_look_speed'] * CLOCK.dt, self._state.aim.y + look_y * CONFIG['controller_look_speed'] * CLOCK.dt)

        length = min(CONFIG['torch_move_radius'], diff.mag)
        self._state.aim = diff.normalize() * length
        self._torch_sprite.position = self._body_sprite.center_x + self._state.aim.x, self._body_sprite.center_y + self._state.aim.y
        LightState.modify_directly(0, Light(1.0, 0.4, 0.0, self._torch_sprite.center_x, self._torch_sprite.center_y, 16.0 * self._state.embers))

        move_x, move_y = input_manager.axis("player-move_horizontal"), input_manager.axis("player-move_vertical")
        if not (move_x or move_y):
            return

        if CLOCK.time_since(self._last_move) < self._state.move_speed:
            return
        self._last_move = CLOCK.time

        if move_x:
            n_x = self._state.x + (1 if move_x > 0 else -1)
        else:
            n_x = self._state.x

        if move_y:
            n_y = self._state.y + (1 if move_y > 0 else -1)
        else:
            n_y = self._state.y

        if not RunState.floor.try_move(self._state.x, self._state.y, n_x, n_y):
            return

        self._state.x = n_x
        self._state.y = n_y

        x, y = RunState.floor.move(n_x, n_y)
        self._state.move_track -= 1
        if self._state.move_track <= 0:
            self._state.embers -= 1
            self._state.move_track = self._state.move_cost

        if self._state.embers < 0:
            raise ValueError("Ded")

        self._body_sprite.position = x, y

    def draw(self):
        self._renderer.draw(pixelated=True)
