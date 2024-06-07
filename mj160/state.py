from typing import TYPE_CHECKING
from random import randint, seed

from arcade import Sprite, SpriteList

from mj160.floors import Floor, floors

if TYPE_CHECKING:
    from mj160.window import DragonWindow


class _RunState:

    def __init__(self):
        self.run_started: bool = False
        self.runs: int = 0

        self.run_seed: int = None
        self.floor_seed: int = None

        self.floor_num = 0
        self.floor: Floor = None

    def hard_reset(self):
        """
        Reset as if the game just launched
        """
        self.run_started: bool = False
        self.runs = 0

        self.run_seed: int = None
        self.floor_seed: int = None

        self.floor_num = 0
        self.floor: Floor = None

    def run_reset(self):
        """
        reset as if a new run started
        """
        self.run_started: bool = False
        self.floor_num = 0
        if self.floor:
            self.floor.cleanup()
        self.floor = None

    def run_start(self):
        self.run_started: bool = True
        self.floor_num = 0

        seed(randint(0, 0xFFFFFF))
        self.run_seed = randint(0, 0xFFFFFF)

    def floor_start(self):
        if self.floor_num >= len(floors):
            raise ValueError("Gone past the final floor")

        seed(self.run_seed << self.floor_num)
        self.floor_seed = randint(0, 0xFFFFFF)

        self.floor = floors[self.floor_num](self.floor_seed)
        self.floor_num += 1


RunState = _RunState()


class _PlayerState:

    def __init__(self):
        self.sprite_renderer: SpriteList = None

    def hard_reset(self):
        """
        Reset as if the game just launched
        """
        self.sprite_renderer: SpriteList = SpriteList()

    def run_reset(self):
        """
        reset as if a new run started
        """
        pass

    def floor_reset(self):
        """
        reset as if entering a new floor
        """
        pass


PlayerState = _PlayerState()
