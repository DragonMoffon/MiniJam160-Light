from typing import TYPE_CHECKING

from pyglet.math import Vec2

from mj160.player import Player
from mj160.util import CLOCK



class _PlayerState:

    def __init__(self):
        self.player_manager: Player = None

        self.x: int = None
        self.y: int = None

        self.last_move: float = 0.0
        self.move_speed: float = float('inf')

        self.aim: Vec2 = Vec2(0.0, 0.0)

        self.embers: int = 0
        self.ember_strength: int = 0
        self.move_cost: int = 0
        self.move_track: int = 0

    def hard_reset(self):
        """
        Reset as if the game just launched
        """
        if self.player_manager:
            self.player_manager.disable()
        self.player_manager: Player = None

        self.x = None
        self.y = None

        self.last_move: float = CLOCK.time
        self.move_speed: float = float('inf')

        self.aim: Vec2 = Vec2(0.0, 0.0)

        self.embers: int = 0  # Your health / radius of light / mana for abilities
        self.move_cost: int = 0  # Number of moves it takes to lose an ember
        self.move_track: int = 0  # The number of moves left till you lose an ember

    def run_reset(self):
        """
        reset as if a new run started
        """
        if self.player_manager:
            self.player_manager.disable()
        self.player_manager = Player(self)

        self.x = 0
        self.y = 0

        self.last_move: float = CLOCK.time
        self.move_speed: float = 1.0 / 4.0

        self.aim: Vec2 = Vec2(0.0, 0.0)

        self.embers = 16
        self.move_cost = 4
        self.move_track = 4

    def floor_reset(self):
        """
        reset as if entering a new floor
        """
        self.x = 0
        self.y = 0

        self.last_move: float = CLOCK.time

        self.aim: Vec2 = Vec2(0.0, 0.0)

        self.move_track = 4


PlayerState = _PlayerState()
