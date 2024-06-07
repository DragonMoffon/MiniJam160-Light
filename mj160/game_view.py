from arcade import draw_text

from mj160.window import DragonView

from mj160.state import RunState, PlayerState


class GameView(DragonView):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        self.setup()

    def setup(self):
        if not RunState.run_started:
            RunState.run_start()

        if not RunState.floor:
            RunState.floor_start()

    def on_update(self, delta_time: float):
        if not RunState.floor:
            self.setup()
            return

        if not RunState.floor.generate():
            return

    def on_draw(self):
        self.clear()

        if RunState.floor and not RunState.floor.generated:
            draw_text(
                "Floor Generating",
                x=0, y=0, anchor_x='center', anchor_y='center',
                font_name='GohuFont 11 Nerd Font Mono'
            )
