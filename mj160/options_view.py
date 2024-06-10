from arcade import Sprite, SpriteList, get_sprites_at_point
from arcade.experimental.input.manager import InputDevice, ActionState

from mj160.view import DragonView
from mj160.util import CONFIG, CLOCK
from mj160.data import load_texture


class OptionsView(DragonView):

    def __init__(self):
        super().__init__()
        self._dot_texture = load_texture("options_sheet", x=128, y=64, width=32, height=32)

        self._title: Sprite = Sprite(load_texture("menu_sheet", y=256, width=128, height=32), center_x=0.0, center_y=CONFIG['win_resolution'][1]/2.0 - 16)
        self._torch: Sprite = Sprite(load_texture("game_sheet", y=32, width=16, height=16))

        self._fullscreen_text: Sprite = Sprite(load_texture("options_sheet", width=288, height=32), center_y=32)
        self._fullscreen_toggle: Sprite = Sprite(self._dot_texture, center_x=80, center_y=32)

        self._volume_text: Sprite = Sprite(load_texture("options_sheet", y=32, width=288, height=32), center_y=0)
        self._volume_text_2: Sprite = Sprite(self._dot_texture, center_x=-16)
        self._volume_text_4: Sprite = Sprite(self._dot_texture, center_x=18)
        self._volume_text_6: Sprite = Sprite(self._dot_texture, center_x=52)
        self._volume_text_8: Sprite = Sprite(self._dot_texture, center_x=86)
        self._volume_text_F: Sprite = Sprite(self._dot_texture, center_x=120)
        self._volume_indicator: Sprite = Sprite()

        self._return_button: Sprite = Sprite(load_texture("menu_sheet", y=128, width=128, height=32), center_x=0, center_y=-64)

        self._buttons: SpriteList = SpriteList()
        self._buttons.extend((self._fullscreen_toggle, self._volume_text_2, self._volume_text_4, self._volume_text_6, self._volume_text_8, self._volume_text_F, self._return_button))
        self._pick_volume()
        self._fullscreen_toggle.visible = self.window.fullscreen

        self._selected_button: Sprite = None

    def _pick_volume(self):
        self._volume_text_2.visible = False
        self._volume_text_4.visible = False
        self._volume_text_6.visible = False
        self._volume_text_8.visible = False
        self._volume_text_F.visible = False
        match CONFIG['game_volume']:
            case 0.2:
                self._volume_text_2.visible = True
            case 0.4:
                self._volume_text_4.visible = True
            case 0.6:
                self._volume_text_6.visible = True
            case 0.8:
                self._volume_text_8.visible = True
            case 1.0:
                self._volume_text_F.visible = True

    def on_action(self, action: str, state: ActionState):
        if state == ActionState.PRESSED:
            return

        if not self._selected_button:
            return

        if action == "gui-select" or action == "gui-left_click":
            match self._selected_button:
                case self._return_button:
                    self.window.go_to_menu()
                case self._fullscreen_toggle:
                    CONFIG['win_fullscreen'] = not CONFIG['win_fullscreen']
                    self.window.set_fullscreen(CONFIG['win_fullscreen'])
                    self._fullscreen_toggle.visible = CONFIG['win_fullscreen']
                    if not CONFIG['win_fullscreen']:
                        self.window.center_window()
                case self._volume_text_2:
                    if CONFIG['game_volume'] == 0.2:
                        CONFIG['game_volume'] = 0
                    else:
                        CONFIG['game_volume'] = 0.2
                    self._pick_volume()
                case self._volume_text_4:
                    if CONFIG['game_volume'] == 0.4:
                        CONFIG['game_volume'] = 0
                    else:
                        CONFIG['game_volume'] = 0.4
                    self._pick_volume()
                case self._volume_text_6:
                    if CONFIG['game_volume'] == 0.6:
                        CONFIG['game_volume'] = 0
                    else:
                        CONFIG['game_volume'] = 0.6
                    self._pick_volume()
                case self._volume_text_8:
                    if CONFIG['game_volume'] == 0.8:
                        CONFIG['game_volume'] = 0
                    else:
                        CONFIG['game_volume'] = 0.8
                    self._pick_volume()
                case self._volume_text_F:
                    if CONFIG['game_volume'] == 1.0:
                        CONFIG['game_volume'] = 0
                    else:
                        CONFIG['game_volume'] = 1.0
                    self._pick_volume()

    def on_update(self, delta_time: float):
        look_x, look_y = self.window.input_manager.axis('player-look_horizontal'), self.window.input_manager.axis(
            'player-look_vertical')
        match self.window.input_manager.active_device:
            case InputDevice.KEYBOARD:
                mouse_x, mouse_y, _ = self.window.upscale_renderer.into_camera.unproject(
                    self.window.map_to_upscale((look_x, look_y)))
                self._torch.position = (mouse_x, mouse_y)
            case InputDevice.CONTROLLER:
                o_pos = self._torch.position
                self._torch.position = o_pos[0] + look_x * CLOCK.engine_dt * CONFIG["controller_look_speed"], o_pos[1] + look_y * CLOCK.engine_dt * CONFIG['controller_look_speed']

        if self._selected_button:
            self._selected_button.scale = 1.0
        self._selected_button = None
        collisions = get_sprites_at_point(self._torch.position, self._buttons)
        if collisions:
            self._selected_button = collisions[-1]
            self._selected_button.scale = 1.1

    def on_draw(self):
        self.clear()
        self._title.draw(pixelated=True)
        self._fullscreen_text.draw(pixelated=True)
        self._volume_text.draw(pixelated=True)
        self._buttons.draw(pixelated=True)
        self._torch.draw(pixelated=True)
