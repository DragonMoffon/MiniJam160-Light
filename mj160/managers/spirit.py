from math import ceil
from random import randint, choice, random

from pyglet.math import Vec2

from mj160.util import CLOCK, CONFIG
from mj160.data import load_audio
from mj160.states import PlayerState, MapState, EmberState, SpiritState, MAP
from mj160.states.spirit import SpiritMode


class SpiritManager:
    LEVEL_UP_TIME: int = 6  # Increase the strength of the spirit every x seconds
    MAX_STRENGTH: int = 6

    def __init__(self):
        self._hurt_sound = load_audio("hurt")
        self._kill_sound = load_audio("kill")
        self._spawn_sound = load_audio("pulse")
        self._hunt_sound = load_audio("target")

    def update(self):
        dt = CLOCK.dt
        tile_size = CONFIG['floor_tile_size']
        brazier_max = EmberState.max_brazier()

        # Iterate over every enemy and if the spawn timer is up
        for spirit in tuple(SpiritState.alive_spirits):
            # Use their mode and their target location to pick where they go next check
            # if they are hitting the player etc etc
            new_pos = spirit.animator.update(dt, spirit.target)

            t_x, t_y = round(spirit.target.x / tile_size), round(spirit.target.y / tile_size)
            i_x, i_y = round(new_pos.x / tile_size), round(new_pos.y / tile_size)

            if not spirit.mode == SpiritMode.KILL and i_x - 1 <= PlayerState.x <= i_x + 1 and i_y + 1 <= PlayerState.y <= i_y + 1:
                spirit.animator.dy = new_pos - Vec2(PlayerState.x * tile_size, PlayerState.y * tile_size)

            spirit.light.x, spirit.light.y = new_pos

            has_reached_target = t_x == i_x and t_y == i_y
            do_level_up = CLOCK.time_since(spirit.level_time) >= SpiritManager.LEVEL_UP_TIME

            match spirit.mode:
                case SpiritMode.IDLE:
                    # Move to a random spot within the level
                    # When Leveling up choose to orbit a brazier or the player
                    # Also if the player gets too close move to orbit them
                    if do_level_up:
                        pick = random()
                        ratio = PlayerState.embers / (PlayerState.embers + brazier_max)

                        if pick <= ratio:
                            spirit.mode = SpiritMode.PLAYER
                        else:
                            spirit.mode = SpiritMode.BRAZIER
                    elif has_reached_target:
                        if i_x - 2 <= PlayerState.x <= i_x + 2 and i_y - 2 <= PlayerState.y <= i_y + 2:
                            spirit.mode = SpiritMode.PLAYER
                        else:
                            spirit.target = spirit.target + Vec2.from_polar(100 + 250.0 * random(), random() * 2.0 * 3.1415962)

                case SpiritMode.BRAZIER:
                    # Move to a spot near a target brazier
                    # If no brazier is selected choose a new brazier
                    # If leveling up choose to IDLE or FOLLOW player based on how many embers the player has
                    # If the player come near either start orbiting the player or run away to another brazier

                    if do_level_up:
                        pick = random()
                        ratio = PlayerState.embers / (PlayerState.embers + brazier_max)
                        if pick <= ratio:
                            spirit.mode = SpiritMode.PLAYER
                        else:
                            spirit.mode = SpiritMode.BRAZIER
                        spirit.target_brazier = None

                    elif spirit.target_brazier is None:
                        spirit.target_brazier = EmberState.get_weighted_brazier()
                        x, y = spirit.target_brazier.light.x, spirit.target_brazier.light.y
                        spirit.target = Vec2(x, y) + Vec2.from_polar(4 * tile_size, random() * 2.0 * 3.1415962)
                    elif has_reached_target:
                        if i_x - 2 <= PlayerState.x <= i_x + 2 and i_y - 2 <= PlayerState.y <= i_y + 2:
                            spirit.mode = SpiritMode.PLAYER
                            spirit.target_brazier = None
                        else:
                            x, y = spirit.target_brazier.light.x, spirit.target_brazier.light.x
                            spirit.target = Vec2(x, y) + Vec2.from_polar(4 * tile_size, random() * 2.0 * 3.1415962)
                case SpiritMode.PLAYER:
                    # Move around the player while keeping their distance
                    # If the player gets too close move to a brazier
                    # If the player gets too big or the spirit levels up go into attack mode

                    if i_x - 1 <= PlayerState.x <= i_x + 1 and i_y - 1 <= PlayerState.y <= i_y + 1:
                        spirit.mode = SpiritMode.BRAZIER
                    elif do_level_up:
                        self._hunt_sound.play(CONFIG['game_volume'])
                        spirit.mode = SpiritMode.KILL
                        spirit.target = Vec2(PlayerState.x * tile_size, PlayerState.y * tile_size)
                    elif has_reached_target:
                        if PlayerState.embers >= 14:
                            self._hunt_sound.play(CONFIG['game_volume'])
                            spirit.mode = SpiritMode.KILL
                            spirit.target = Vec2(PlayerState.x * tile_size, PlayerState.y * tile_size)
                        else:
                            x, y = PlayerState.x * tile_size, PlayerState.y * tile_size
                            spirit.target = Vec2(x, y) + Vec2.from_polar(PlayerState.embers * tile_size, random() * 2.0 * 3.1415962)
                case SpiritMode.KILL:
                    # Start moving towards the player's current location, then go to the idle state
                    if has_reached_target:
                        if PlayerState.embers <= 4:
                            spirit.mode = SpiritMode.IDLE
                        else:
                            self._hunt_sound.play(CONFIG['game_volume'])
                            spirit.mode = SpiritMode.KILL
                            spirit.target = Vec2(PlayerState.x * tile_size, PlayerState.y * tile_size)

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

