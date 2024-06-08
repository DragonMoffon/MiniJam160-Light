from arcade import Text

from mj160.window import DragonView

from mj160.player_state import PlayerState
from mj160.run_state import RunState
from mj160.light_state import LightState, Light


class GameView(DragonView):

    def __init__(self):
        super().__init__()

        self.loading_text = Text(
                "Floor Generating",
                x=0, y=0, anchor_x='center', anchor_y='center',
                font_name='GohuFont 11 Nerd Font Mono'
            )

    def on_show_view(self):
        self.setup()
        if RunState.floor is not None and RunState.floor.generated:
            LightState.enable()

    def on_hide_view(self):
        LightState.disable()

    def setup(self):
        if not RunState.run_started:
            PlayerState.run_reset()
            RunState.run_start()

        if not RunState.floor:
            PlayerState.floor_reset()
            RunState.floor_start()

        RunState.floor.disable()
        PlayerState.player_manager.disable()

    def on_update(self, delta_time: float):
        if not RunState.floor:
            self.setup()
            return

        if not RunState.floor.generated:
            if RunState.floor.generate():
                RunState.floor.enable()
                PlayerState.player_manager.enable()
                PlayerState.player_manager.spawn()
                LightState.enable()
                LightState.add_light(Light(1.0, 0.0, 1.0, 0.0, 0.0, 100.0))

    def on_draw(self):
        if RunState.floor and not RunState.floor.generated:
            self.loading_text.draw()
