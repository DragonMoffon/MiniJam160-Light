from arcade import Sprite, SpriteSolidColor
from mj160.util import CLOCK, CONFIG

from mj160.view import DragonView

from mj160.states import GameState, PlayerState, EmberState, SpiritState, LightState
from mj160.managers import LightManager, PlayerManager, MapManager, EmberManager, SpiritManager

from mj160.gui.game import EmberTracker


class GameView(DragonView):

    def __init__(self):
        super().__init__()
        GameState.next_play()
        self.ember_tracker: EmberTracker = EmberTracker()
        self.map: MapManager = None
        self.ember: EmberManager = None
        self.player: PlayerManager = None
        self.light: LightManager = None
        self.spirit: SpiritManager = None

        # TODO
        # self.paused: bool = False
        # self.paused_button: Sprite = None
        # self.paused_overlay: Sprite = SpriteSolidColor(self.window)
        # self.paused_overlay:

    def on_show_view(self):
        self.setup()

    def setup(self):
        if not self.light:
            LightState.reset()
            self.light = LightManager()

        if not self.map:
            EmberState.reset_braziers()
            self.map = MapManager()

        if not self.ember:
            self.ember = EmberManager()

        if not self.player:
            self.player = PlayerManager()
            PlayerState.reset()
            self.player.spawn()

        if not self.spirit:
            SpiritState.reset()
            self.spirit = SpiritManager()

    def on_update(self, delta_time: float):
        self.ember.update()
        self.map.update()
        self.player.update()
        self.spirit.update()

        if PlayerState.embers == 0 and PlayerState.move_track == 0:
            GameState.end_play()
            self.window.go_to_lose()

    def on_draw(self):
        self.clear(color_normalized=(0.75, 0.75, 0.75, 1.0))

        self.map.draw()

        self.player.draw()

        self.light.draw()

        self.ember_tracker.draw()
