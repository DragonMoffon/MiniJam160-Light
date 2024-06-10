from __future__ import annotations
from typing import TYPE_CHECKING

from arcade import Sprite, SpriteList, get_window
from arcade.experimental.input.manager import InputDevice

from pyglet.math import Vec2

from mj160.data import load_texture, load_audio
from mj160.util import CLOCK, CONFIG, ProceduralAnimator
from mj160.states import PlayerState, LightState, MapState, Light

if TYPE_CHECKING:
    from mj160.window import DragonWindow


class PlayerManager:

    def __init__(self):
        self.ember_sound = load_audio("ember")

        self._window: DragonWindow = get_window()

        self.renderer: SpriteList = SpriteList()
        self._player_sprite: Sprite = Sprite(load_texture("game_sheet", y=16, width=16, height=16))
        self._torch_sprite: Sprite = Sprite(load_texture("game_sheet", y=32, width=16, height=16))
        self._torch_light: Light = Light(1.0, 0.4, 0.0, 0.0, 0.0, 1.0)

        self.renderer.extend((self._player_sprite, self._torch_sprite))
        LightState.add_light(self._torch_light)

        self.camera_animator: ProceduralAnimator = ProceduralAnimator(1.0, 0.75, 1.2, Vec2(0.0), Vec2(0.0), Vec2(0.0))
        self.torch_animator: ProceduralAnimator = ProceduralAnimator(2.0, 0.75, 1.2, Vec2(0.0), Vec2(0.0), Vec2(0.0))

        self.buffered_move: tuple[int, int] = None

    def spawn(self):
        i_x, i_y = MapState.spawn_point
        n_x, n_y = MapState.move(i_x, i_y)

        PlayerState.x = i_x
        PlayerState.y = i_y

        self._player_sprite.position = n_x, n_y
        self.buffered_move = None

    def look(self):
        input_manager = self._window.input_manager
        look_x, look_y = input_manager.axis("player-look_horizontal"), input_manager.axis("player-look_vertical")
        diff = Vec2(0.0, 0.0)
        match input_manager.active_device:
            case InputDevice.KEYBOARD:
                mouse_x, mouse_y, _ = self._window.upscale_renderer.into_camera.unproject(
                    self._window.map_to_upscale((look_x, look_y)))
                diff = Vec2(mouse_x - self._player_sprite.center_x, mouse_y - self._player_sprite.center_y)

            case InputDevice.CONTROLLER:
                diff = Vec2(PlayerState.aim.x + look_x * CONFIG['controller_look_speed'] * CLOCK.dt,
                            PlayerState.aim.y + look_y * CONFIG['controller_look_speed'] * CLOCK.dt)

        length = min(CONFIG['torch_move_radius'], diff.mag)
        PlayerState.aim = diff.normalize() * length
        pos = Vec2(self._player_sprite.center_x + PlayerState.aim.x, self._player_sprite.center_y + PlayerState.aim.y)
        (self._torch_light.x, self._torch_light.y) = PlayerState.torch = self._torch_sprite.position = self.torch_animator.update(CLOCK.dt, pos)

    def move(self):
        input_manager = self._window.input_manager

        move_x, move_y = input_manager.axis("player-move_horizontal"), input_manager.axis("player-move_vertical")
        if not (move_x or move_y) and self.buffered_move is None:
            return

        self.buffered_move = (move_x, move_y)
        if CLOCK.time_since(PlayerState.last_move) < PlayerState.move_speed:
            return
        PlayerState.last_move = CLOCK.time
        if self.buffered_move and not (move_x, move_y):
            move_x, move_y = self.buffered_move
        self.buffered_move = None

        if move_x:
            n_x = PlayerState.x + (1 if move_x > 0 else -1)
        else:
            n_x = PlayerState.x

        if move_y:
            n_y = PlayerState.y + (1 if move_y > 0 else -1)
        else:
            n_y = PlayerState.y

        if MapState.try_interact(n_x, n_y):
            MapState.interact(n_x, n_y)
            return

        if not MapState.try_move(n_x, n_y):
            return

        PlayerState.x = n_x
        PlayerState.y = n_y

        x, y = MapState.move(n_x, n_y)
        PlayerState.move_track = max(0, PlayerState.move_track - 1)
        if PlayerState.move_track <= 0:
            if PlayerState.embers > 0:
                PlayerState.move_track = PlayerState.move_cost
            self.ember_sound.play(CONFIG['game_volume'])
            PlayerState.embers -= 1

        self._player_sprite.position = x, y

    def update(self):
        self._window.upscale_renderer.into_camera.position = self.camera_animator.update(CLOCK.dt, Vec2(*self._player_sprite.position))
        self.look()
        self.move()

        if CLOCK.time_since(PlayerState.last_hit) < 1.0/8.0:
            self._torch_light.b = 1.0
        else:
            self._torch_light.b = 0.0

        self._torch_light.s = max(0.0, PlayerState.embers * CONFIG['floor_tile_size'])

    def draw(self):
        self.renderer.draw(pixelated=True)
