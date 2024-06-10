from arcade import Sprite, SpriteList
from arcade.experimental.input.manager import InputDevice, ActionState

from mj160.util import CONFIG, CLOCK, generate_number_sprites
from mj160.data import load_texture
from mj160.view import DragonView
from mj160.states import GameState


class LoseView(DragonView):

    def __init__(self):
        super().__init__()
        self.window.upscale_renderer.into_camera.position = (0.0, 0.0)
        self._sprites: SpriteList = SpriteList()
        self._sprites.append(Sprite(load_texture("lost_screen")))
        self._sprites.extend(generate_number_sprites(GameState.play_count, 15, 28))
        self._sprites.extend(generate_number_sprites(int(GameState.play_end - GameState.play_start), 15,  -1))
        self._sprites.extend(generate_number_sprites(GameState.total_spirit_strength, 15, -31))

        self._retry_button: Sprite = Sprite(load_texture("menu_sheet", y=96, width=128, height=32), center_x=-96, center_y=-75) # Create a new game view and go again
        self._return_button: Sprite = Sprite(load_texture("menu_sheet", y=128, width=128, height=32), center_x=96, center_y=-75) # return to the main menu
        self._select_sprite: Sprite = Sprite(load_texture("menu_sheet", y=192, width=128, height=32))
        self._torch_sprite: Sprite = Sprite(load_texture("game_sheet", y=32, width=16, height=16))

        self._selected_button: Sprite = None

        self._sprites.extend((self._retry_button, self._return_button, self._torch_sprite))

    def on_draw(self):
        self.clear()
        self._sprites.draw(pixelated=True)

        if self._selected_button:
            self._select_sprite.position = self._selected_button.position
            self._select_sprite.draw(pixelated=True)

    def on_update(self, delta_time: float):
        if self._torch_sprite:
            look_x, look_y = self.window.input_manager.axis('player-look_horizontal'), self.window.input_manager.axis(
                'player-look_vertical')
            match self.window.input_manager.active_device:
                case InputDevice.KEYBOARD:
                    mouse_x, mouse_y, _ = self.window.upscale_renderer.into_camera.unproject(
                        self.window.map_to_upscale((look_x, look_y)))
                    self._torch_sprite.position = (mouse_x, mouse_y)
                case InputDevice.CONTROLLER:
                    o_pos = self._torch_sprite.position
                    self._torch_sprite.position = o_pos[0] + look_x * CLOCK.dt * CONFIG["controller_look_speed"], o_pos[1] + look_y * CLOCK.dt * CONFIG['controller_look_speed']

            self._selected_button = None
            if self._retry_button.collides_with_point(self._torch_sprite.position):
                self._selected_button = self._retry_button
            elif self._return_button.collides_with_point(self._torch_sprite.position):
                self._selected_button = self._return_button

    def on_action(self, action: str, state: ActionState):
        if state == ActionState.PRESSED:
            return

        if action == "gui-select" or action == "gui-left_click":
            if self._selected_button == self._retry_button:
                self.window.go_to_game()
            elif self._selected_button == self._return_button:
                self.window.go_to_menu()
