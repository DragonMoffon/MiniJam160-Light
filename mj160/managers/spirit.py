from math import ceil
from random import randint, choice, random

from pyglet.math import Vec2

from mj160.util import CLOCK, CONFIG
from mj160.data import load_audio
from mj160.states import PlayerState, MapState, EmberState, SpiritState
from mj160.states.spirit import SpiritMode


class SpiritManager:
    LEVEL_UP_TIME: int = 6  # Increase the strength of the spirit every x seconds
    MAX_STRENGTH: int = 6

    def __init__(self):
        self._hurt_sound = load_audio("hurt")
        self._kill_sound = load_audio("kill")
        self._spawn_sound = load_audio("pulse")

    def update(self):
        dt = CLOCK.dt
        tile_size = CONFIG['floor_tile_size']
        # Iterate over every enemy and if the spawn timer is up
        for spirit in tuple(SpiritState.alive_spirits):
            # Use their mode and their target location to pick where they go next check
            # if they are hitting the player etc etc
            new_pos = spirit.animator.update(dt, spirit.target, Vec2(0.0, 0.0))

            t_x, t_y = round(spirit.target.x / tile_size), round(spirit.target.y / tile_size)
            i_x, i_y = round(new_pos.x / tile_size), round(new_pos.y / tile_size)

            spirit.light.x, spirit.light.y = new_pos

            has_reached_target = t_x == i_x and t_y == i_y
            do_level_up = spirit.strength < SpiritManager.MAX_STRENGTH and CLOCK.time_since(spirit.level_time) >= SpiritManager.LEVEL_UP_TIME

            match spirit.mode:
                case SpiritMode.IDLE:
                    # Move to a spot, and then pick another spot near it to move towards
                    # If the player gets too big go into attack mode
                    # if the spirit levels up choose to either orbit a brazier or the player (based on which is bigger)

                    spirit.mode = SpiritMode.BRAZIER
                case SpiritMode.BRAZIER:
                    # Move to a spot near the brazier
                    # If the player come near either start orbiting the player or run away to another brazier
                    # If the player gets too big move to attack player (or another brazier if the brazier is bigger)
                    # When level up continue orbiting the brazier or pick between orbiting the player or idling

                    pass

                    if has_reached_target and do_level_up:
                        next_brazier = EmberState.get_weighted_brazier()
                        spirit.target = Vec2(next_brazier.light.x, next_brazier.light.y) + Vec2.from_polar(4 * tile_size, random() * 2.0 * 3.1415962)
                case SpiritMode.PLAYER:
                    # Move around the player while keeping their distance
                    # If the player gets too close move away
                    # If the player gets too big or the spirit levels up go into attack mode

                    spirit.mode = SpiritMode.BRAZIER
                case SpiritMode.KILL:
                    # Start moving towards the player's current location, then go to the idle state
                    spirit.mode = SpiritMode.BRAZIER

            # If on the player's location deal damage equal to strength and kill spirit
            # If on the torch's tile then kill the ghost and deal one ember of damage and kill spirit
            if i_x == PlayerState.x and i_y == PlayerState.y:
                self._hurt_sound.play(CONFIG['game_volume'])
                PlayerState.embers = max(0, PlayerState.embers - spirit.strength)
                SpiritState.kill_spirit(spirit)
                continue

            if i_x == round(PlayerState.torch.x / tile_size) and i_y == round(PlayerState.torch.y / tile_size):
                self._kill_sound.play(CONFIG['game_volume'])
                PlayerState.embers = max(0, PlayerState.embers - 1)
                SpiritState.kill_spirit(spirit)
                continue

            if do_level_up:
                spirit.level_up()

        if CLOCK.time >= SpiritState.next_aggression_time:
            SpiritState.increase_aggro()

        if CLOCK.time >= SpiritState.next_spawn_time:
            i_x, i_y = MapState.get_random_walkable_tile()
            strength = ceil(SpiritState.aggression / SpiritState.MAX_AGGRESSION * SpiritManager.MAX_STRENGTH) + randint(0, 2)
            self._spawn_sound.play(CONFIG['game_volume'] * 0.5 * (1 + strength / SpiritState.MAX_AGGRESSION))
            SpiritState.spawn_spirit(i_x, i_y, strength)

