from arcade import Sprite, SpriteList, Texture, get_window, SpriteSolidColor
from arcade.experimental.input.manager import ActionState, InputDevice

from mj160.data import load_texture
from mj160.states import PlayerState, GameState
from mj160.util import CONFIG, CLOCK, generate_number_sprites


class EmberTracker:

    def __init__(self):
        self.win = get_window()

        self.ember_cell: Texture = load_texture("ui_sheet", width=16, height=16)
        self.ember_fill: Texture = load_texture("ui_sheet", x=16, width=16, height=16)
        self.move_cell: Texture = load_texture("ui_sheet", x=32, width=16, height=16)
        self.move_fill: Texture = load_texture("ui_sheet", x=48, width=16, height=16)

        self._renderer: SpriteList = SpriteList()

        self._cells = (Sprite(self.ember_cell, center_x=CONFIG['win_resolution'][0] - 8, center_y=CONFIG['win_resolution'][1] - 8 - idx * 9) for idx in range(16))
        self._fills = tuple(Sprite(self.ember_fill, center_x=CONFIG['win_resolution'][0] - 8, center_y=CONFIG['win_resolution'][1] - 8 - idx * 9) for idx in range(16))
        self._move_cells = (Sprite(self.move_cell, center_x=CONFIG['win_resolution'][0] - 24, center_y=CONFIG['win_resolution'][1] - 12 - idx * 6) for idx in range(4))
        self._move_fills = tuple(Sprite(self.move_fill, center_x=CONFIG['win_resolution'][0] - 24, center_y=CONFIG['win_resolution'][1] - 12 - idx * 6) for idx in range(4))

        self._renderer.extend(self._cells)
        self._renderer.extend(self._fills)
        self._renderer.extend(self._move_cells)
        self._renderer.extend(self._move_fills)

        self._last_score: int = -1
        self._score_text: list = []

    def draw(self):
        for idx in range(16):
            fill = self._fills[idx]
            fill.visible = idx + 1 <= PlayerState.embers

        for idx in range(4):
            fill = self._move_fills[idx]
            fill.visible = idx + 1 <= PlayerState.move_track

        if self._last_score != GameState.total_spirit_strength:
            self._last_score = GameState.total_spirit_strength
            for sprite in self._score_text:
                self._renderer.remove(sprite)

            self._score_text = generate_number_sprites(GameState.total_spirit_strength, 16, 16)
            self._renderer.extend(self._score_text)

        with self.win.default_camera.activate():
            self._renderer.draw(pixelated=True)


class PausedOverlay:

    def __init__(self):
        self._win = get_window()
        w, h = CONFIG['win_resolution']

        self._overlay: Sprite = SpriteSolidColor(w, h, w/2, h/2, (120, 120, 120, 120))
        self._selector: Sprite = Sprite(load_texture('menu_sheet', y=192, width=128, height=32))
        self._paused: Sprite = Sprite(load_texture('menu_sheet', y=160, width=128, height=32), 1.0, w/2, h/2 + 64.0)
        self._return_button: Sprite = Sprite(load_texture('menu_sheet', y=129, width=128, height=32), 1.0, w/2, h/2 - 0.0)
        self._retry_button: Sprite = Sprite(load_texture('menu_sheet', y=96, width=128, height=32), 1.0, w/2, h/2 - 32.0)
        self._quit_button: Sprite = Sprite(load_texture('menu_sheet', y=64, width=128, height=32), 1.0, w/2, h/2 - 64.0)

        self._selected_button: Sprite = None

        self._torch: Sprite = Sprite(load_texture("game_sheet", y=32, width=16, height=16))

        self._renderer: SpriteList = SpriteList()
        self._renderer.extend((self._overlay, self._paused, self._return_button, self._retry_button, self._quit_button, self._torch))

        self._paused: bool = False

    @property
    def paused(self):
        return self._paused

    def on_action(self, action: str, state: ActionState):
        if state == state.PRESSED:
            return

        match action:
            case "gui-back":
                self.toggle()
            case "gui-select" if self._paused:
                self.click()
            case "gui-left_click" if self._paused:
                self.click()
    def click(self):
        if self._selected_button == self._retry_button:
            self.unpause()
            self._win.go_to_game()
        elif self._selected_button == self._return_button:
            self.unpause()
        elif self._selected_button == self._quit_button:
            self.unpause()
            self._win.go_to_menu()

    def pause(self):
        self._paused = True
        CLOCK._elapse_speed = 0.0

    def unpause(self):
        self._paused = False
        CLOCK._elapse_speed = 1.0

    def toggle(self):
        if self._paused:
            self.unpause()
        else:
            self.pause()

    def draw(self):
        if not self._paused:
            return

        with get_window().default_camera.activate():
            self._renderer.draw(pixelated=True)

            if self._selected_button:
                self._selector.position = self._selected_button.position
                self._selector.draw()

    def update(self):
        if not self._paused:
            return

        look_x, look_y = self._win.input_manager.axis('player-look_horizontal'), self._win.input_manager.axis(
            'player-look_vertical')
        match self._win.input_manager.active_device:
            case InputDevice.KEYBOARD:
                mouse_x, mouse_y = self._win.map_to_upscale((look_x, look_y))
                self._torch.position = (mouse_x, mouse_y)
            case InputDevice.CONTROLLER:
                o_pos = self._torch.position
                self._torch.position = o_pos[0] + look_x * CLOCK.engine_dt * CONFIG["controller_look_speed"], o_pos[1] + look_y * CLOCK.engine_dt * CONFIG['controller_look_speed']

        self._selected_button = None
        if self._retry_button.collides_with_point(self._torch.position):
            self._selected_button = self._retry_button
        elif self._return_button.collides_with_point(self._torch.position):
            self._selected_button = self._return_button
        elif self._quit_button.collides_with_point(self._torch.position):
            self._selected_button = self._quit_button
