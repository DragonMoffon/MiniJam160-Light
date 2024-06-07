from arcade import Sprite, SpriteList, get_window, Window
from arcade.experimental.input import ActionState

from mj160.window import DragonWindow
from mj160.state import PlayerState
from mj160.util import CLOCK, CONFIG


class Torch:

    def __init__(self, renderer: SpriteList):
        self._torch_sprite: Sprite = Sprite()
        renderer.append(self._torch_sprite)


class Player:

    def __init__(self):
        self._window: DragonWindow = get_window()

        self._sprite_list: SpriteList = SpriteList()

        self._body_sprite: Sprite = Sprite()
        self._sprite_list.append(self._body_sprite)

        self._torch: Torch = Torch(self._sprite_list)

        self._window.input_manager.register_action_handler(self.on_action)

    def reset(self):
        pass

    def on_action(self, action: str, state: ActionState):
        print(action, state)
