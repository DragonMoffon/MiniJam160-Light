from enum import Enum
from random import random

from pyglet.math import Vec2


from mj160.util import CLOCK, CONFIG, ProceduralAnimator
from mj160.states.light import Light, LightState
from mj160.states.ember import Brazier


class SpiritMode(Enum):
    IDLE = 0
    BRAZIER = 1
    PLAYER = 2
    KILL = 3


class Spirit:

    def __init__(self):
        self.strength: int = 0
        self.light: Light = Light(-1.0, -1.0, 0.05, 0.0, 0.0, 0.0)
        self.level_time: float = 0.0
        self.mode: SpiritMode = SpiritMode.IDLE
        self.target: Vec2 = Vec2(0.0, 0.0)
        self.target_brazier: Brazier = None
        self.animator: ProceduralAnimator = ProceduralAnimator(0.75, 0.5, 2.0, Vec2(0.0, 0.0), Vec2(0.0, 0.0), Vec2(0.0, 0.0))

    def spawn(self, i_x: int, i_y: int, s: int):
        self.strength = s
        self.level_time = CLOCK.time
        x = i_x * CONFIG['floor_tile_size']
        y = i_y * CONFIG['floor_tile_size']

        self.animator.y = self.animator.xp = self.target = Vec2(x, y)
        self.mode: SpiritMode.IDLE
        self.light.x, self.light.y = x, y

        self.light.r = -1.0
        self.light.g = -1.0
        self.light.b = 0.1

        self.light.s = s * CONFIG['floor_tile_size']

        self.target_brazier: Brazier = None
        LightState.add_light(self.light)

    def level_up(self):
        self.level_time = CLOCK.time

        if self.strength >= _SpiritState.MAX_STRENGTH:
            return

        self.strength += 1
        self.light.s = self.strength * CONFIG['floor_tile_size']

        if self.strength > 4:
            self.light.g = 0.1

        if self.strength >= 6:
            self.light.b = -1.0

    def kill(self):
        if self.light in LightState.lights:
            LightState.remove_light(self.light)


class _SpiritState:
    MAX_SPIRITS: int = 16
    MAX_STRENGTH: int = 6

    SPAWN_RATE: float = 3.0
    SPAWN_RATE_VARIATION: float = 1.5

    MAX_AGGRESSION: int = 24
    AGGRO_RATE: float = 10.0
    AGGRO_RATE_VARIATION: float = 2.5

    def __init__(self):
        self.waiting_spirits: list[Spirit] = []
        self.alive_spirits: list[Spirit] = []

        # Determines the strength of newly spawned enemies, and how likely an enemy is to attack the player or level up
        self.aggression: int = 1

        self.next_spawn_time: float = 0.0
        self.next_aggression_time: float = 0.0

    def reset(self):
        for spirit in self.alive_spirits:
            spirit.kill()

        for _ in range(_SpiritState.MAX_SPIRITS):
            self.waiting_spirits.append(Spirit())

        self.aggression = 1

        self.next_spawn_time: float = CLOCK.time + _SpiritState.SPAWN_RATE + random() * _SpiritState.SPAWN_RATE_VARIATION
        self.next_aggression_time: float = CLOCK.time + _SpiritState.AGGRO_RATE + random() * _SpiritState.AGGRO_RATE_VARIATION

    def spawn_spirit(self, i_x: int, i_y: int, s: int):
        self.next_spawn_time = CLOCK.time + _SpiritState.SPAWN_RATE + random() * _SpiritState.SPAWN_RATE_VARIATION
        if not self.waiting_spirits:
            return

        next_spirit = self.waiting_spirits.pop()
        next_spirit.spawn(i_x, i_y, s)
        self.alive_spirits.append(next_spirit)

    def kill_spirit(self, spirit: Spirit):
        if spirit not in self.alive_spirits:
            return

        spirit.kill()
        self.alive_spirits.remove(spirit)
        self.waiting_spirits.append(spirit)

    def increase_aggro(self):
        self.aggression = min(_SpiritState.MAX_AGGRESSION, self.aggression + 1)
        self.next_aggression_time: float = CLOCK.time + _SpiritState.AGGRO_RATE + random() * _SpiritState.AGGRO_RATE_VARIATION


SpiritState = _SpiritState()
