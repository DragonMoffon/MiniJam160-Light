from random import random

from mj160.util import CLOCK, CONFIG
from mj160.states.light import LightState, Light


class Brazier:

    def __init__(self, x, y, embers):
        self.embers: int = embers
        self.last_increase: float = CLOCK.time
        self.last_pull: float = CLOCK.time
        self.light: Light = Light(1.0, 0.4, 0.0, x, y, embers * CONFIG['floor_tile_size'])

    def pull(self):
        embers = self.embers
        self.embers = 0
        self.last_pull = CLOCK.time
        return embers

    def update(self):
        if self.embers >= _EmberState.EMBER_MAX:
            return

        if CLOCK.time_since(self.last_pull) < _EmberState.PULL_RECOVER:
            return

        if CLOCK.time_since(self.last_increase) < _EmberState.EMBER_RECHARGE + random() * _EmberState.EMBER_RANGE:
            return
        self.last_increase = CLOCK.time

        self.embers += 1
        self.light.s = self.embers * CONFIG['floor_tile_size']


class _EmberState:
    MAX_BRAZIERS: int = 8
    EMBER_MAX: int = 16
    PULL_RECOVER: float = 2.0
    EMBER_RECHARGE: float = 1.0
    EMBER_RANGE: float = 0.2

    def __init__(self):
        self.braziers: list[Brazier] = []

    def reset_braziers(self):
        for brazier in self.braziers:
            if brazier.light in LightState.lights:
                LightState.remove_lights(brazier.light)
        self.braziers = []

    def add_brazier(self, brazier: Brazier):
        if len(self.braziers) >= _EmberState.MAX_BRAZIERS:
            raise ValueError("Trying to add too many braziers")

        self.braziers.append(brazier)

    def remove_brazier(self, brazier: Brazier):
        self.braziers.remove(brazier)

    def update(self):
        for brazier in self.braziers:
            brazier.update()


EmberState = _EmberState()
