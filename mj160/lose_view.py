from arcade import Text

from mj160.window import DragonView
from mj160.light_state import LightState


class LoseView(DragonView):

    def __init__(self):
        super().__init__()
        self.window.upscale_renderer.into_camera.position = (0.0, 0.0)
        self._lose = Text("YOU LOST", x=0, y=0, anchor_x='center', anchor_y='center', font_name='GohuFont 11 Nerd Font Mono', font_size=16)

    def on_show_view(self):
        LightState.disable()

    def on_draw(self):
        self.clear()
        self._lose.draw()
