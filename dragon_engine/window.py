from arcade import Window, View

from dragon_engine.config import CONFIG


class DragonWindow(Window):

    def __init__(self):
        w, h = CONFIG['win_resolution']
        super().__init__(w, h, CONFIG['win_name'], fullscreen=CONFIG['win_fullscreen'], center_window=True)
