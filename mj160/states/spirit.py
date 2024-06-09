from attr import define
from pyglet.math import Vec2

from mj160.states.light import Light, LightState


class Spirit:

    def __init__(self):
        self.light: Light = None
        self.velocity: Vec2 = Vec2(0.0, 0.0)

    def enable(self):
        pass

    def disable(self):
        pass


class _SpiritState:
    MAX_SPIRITS: int = 16

    def __init__(self):
        self.spirits: list[Spirit] = []
        self.aggression: int = 1


SpiritState = _SpiritState()
