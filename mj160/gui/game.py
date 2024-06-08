from arcade import Sprite, SpriteList

from mj160.data import load_texture
from mj160.player_state import PlayerState


class EmberTracker:

    def __init__(self):
        self._renderer: SpriteList = SpriteList()