from random import choice

from mj160.util import CLOCK
from mj160.states import PlayerState, MapState, EmberState, SpiritState


class SpiritManager:
    LEVEL_UP_TIME: int = 0
    MAX_STRENGTH: int = 0
    MAX_AGGRESSION: int = 24

    def update(self):
        # Iterate over every enemy and if the spawn timer is up
        for spirit in SpiritState.alive_spirits:
            # Use their mode and their target location to pick where they go next check
            # if they are hitting the player etc etc

            pass
