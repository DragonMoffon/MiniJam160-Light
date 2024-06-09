from arcade import Sprite, SpriteList, Texture, get_window

from mj160.data import load_texture
from mj160.states import PlayerState
from mj160.util import CONFIG


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

    def draw(self):
        for idx in range(16):
            fill = self._fills[idx]
            fill.visible = idx + 1 <= PlayerState.embers

        for idx in range(4):
            fill = self._move_fills[idx]
            fill.visible = idx + 1 <= PlayerState.move_track

        with self.win.default_camera.activate():
            self._renderer.draw(pixelated=True)
