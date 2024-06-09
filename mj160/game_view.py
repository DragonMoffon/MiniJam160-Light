from arcade import Text

from mj160.window import DragonView

from mj160.states import GameState, PlayerState, EmberState
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

    def on_show_view(self):
        self.setup()

    def on_hide_view(self):
        pass

    def setup(self):
        if not self.light:
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
            self.spirit = SpiritManager()

    def on_update(self, delta_time: float):
        self.ember.update()
        self.map.update()
        self.player.update()
        self.spirit.update()

    def on_draw(self):
        self.map.draw()

        self.player.draw()

        self.light.draw()

        self.ember_tracker.draw()
