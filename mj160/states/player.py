from pyglet.math import Vec2

from mj160.util import CLOCK


class _PlayerState:

    def __init__(self):
        self.x: int = 0
        self.y: int = 0

        self.last_move: float = 0.0
        self.move_speed: float = float('inf')

        self.aim: Vec2 = Vec2(0.0, 0.0)
        self.torch: Vec2 = Vec2(0.0, 0.0)

        self.embers: int = 0
        self.move_cost: int = 0
        self.move_track: int = 0

    def reset(self):
        self.x = self.y = self.embers = 0
        self.move_cost = self.move_track = 4

        self.embers = 16

        self.last_move = CLOCK.time
        self.move_speed = 1 / 4.0

        self.aim = Vec2(0.0, 0.0)


PlayerState = _PlayerState()
