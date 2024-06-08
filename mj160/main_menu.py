from mj160.window import DragonView
from mj160.gui.main_menu import MainMenuGui

from mj160.run_state import RunState


class MainMenuView(DragonView):

    def __init__(self):
        super().__init__()
        self.main_menu: MainMenuGui = MainMenuGui()

    def on_update(self, delta_time: float):
        self.main_menu.update()

    def on_draw(self):
        self.clear()
        self.main_menu.draw()

    def on_show_view(self):
        RunState.run_reset()
        self.main_menu.on_show()

    def on_hide_view(self):
        self.main_menu.on_hide()
