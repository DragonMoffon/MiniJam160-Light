from __future__ import annotations

from logging import getLogger
from typing import Generator

from arcade import get_window, SpriteList, Sprite

from mj160.util import CONFIG
from mj160.data import load_texture

logger = getLogger("mj160")


class Tile:

    def __init__(self, walkable: bool, interactable: bool, sprite: Sprite):
        self.sprite: Sprite = sprite
        self.sprite.depth = -1
        self.walkable: bool = walkable
        self.interactable: bool = interactable
        self.location: tuple[int, int] = None
        self.neighbors: set[tuple[int, int]] = set()

    @property
    def world_pos(self):
        return self.location[0] * CONFIG['floor_tile_size'], self.location[1] * CONFIG['floor_tile_size']

    def place(self, location: tuple[int, int], neighbors: set[tuple[int, int]]):
        self.location = location
        self.neighbors = neighbors
        self.sprite.position = self.world_pos

    def try_step(self, from_x, from_y):
        return self.walkable and (from_x, from_y) in self.neighbors

    def try_interact(self, from_x, from_y):
        return self.interactable and not self.try_step(from_x, from_y)

    def on_interact(self):
        pass

    def on_step(self):
        pass


class Room:
    """
    A pre-made construct used in random generation (maybe)???
    """

    def __init__(self):
        pass


class WallSimple(Tile):

    def __init__(self):
        super().__init__(False, False, Sprite(load_texture("game_sheet", width=16, height=16)))


class GroundSimple(Tile):

    def __init__(self):
        super().__init__(True, False, Sprite(load_texture("game_sheet", x=16, width=16, height=16)))


class Floor:

    def __init__(self, seed_: int):
        self.seed: int = seed_

        self.generator = None
        self.generated: bool = False
        self._is_enabled: bool = False

        self.tile_sprites: SpriteList = SpriteList()

        self.tiles: dict[tuple[int, int], Tile] = {}
        self.spawn_tile: Tile = None

    def enable(self):
        if self._is_enabled:
            return
        self._is_enabled = True

        win = get_window()
        win.push_handlers(on_update=self.update, on_draw=self.draw)

    def disable(self):
        if not self._is_enabled:
            return
        self._is_enabled = False

        win = get_window()
        win.remove_handlers(on_update=self.update, on_draw=self.draw)

    def update(self, dt: float):
        pass

    def draw(self):
        self.tile_sprites.draw(pixelated=True)

    def cleanup(self):
        raise NotImplementedError()

    def _generate_floor(self) -> Generator[bool, None, bool]:
        raise NotImplementedError()

    def generate(self):
        if self.generated:
            self.generator = None
            return True

        if not self.generator:
            self.generator = self._generate_floor()
        self.generated = next(self.generator, True)

        if self.generated:
            self.generator = None

        return self.generated

    def try_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        if not ((from_x, from_y) in self.tiles and (to_x, to_y) in self.tiles):
            return False

        to_tile = self.tiles[(to_x, to_y)]

        return to_tile.try_step(from_x, from_y)

    def try_interact(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        if not ((from_x, from_y) in self.tiles and (to_x, to_y) in self.tiles):
            return False

        to_tile = self.tiles[(to_x, to_y)]
        return to_tile.try_interact(from_x, from_y)

    def move(self, to_x: int, to_y: int) -> tuple[float, float]:
        to_tile = self.tiles[(to_x, to_y)]
        to_tile.on_step()

        return to_tile.world_pos

    def interact(self, to_x: int, to_y: int):
        to_tile = self.tiles[(to_x, to_y)]
        to_tile.on_interact()

    def spawn_point(self) -> tuple[int, int]:
        if not self.spawn_tile:
            return (0, 0)

        return self.spawn_tile.location


class Tutorial(Floor):

    def _generate_floor(self):
        yield False
        for i_x in range(0, 10):
            for i_y in range(0, 10):
                if i_x == 0 or i_x == 9 or i_y == 0 or i_y == 9:
                    tile = WallSimple()
                else:
                    tile = GroundSimple()

                self.tiles[i_x, i_y] = tile

                if i_x == 1 and i_y == 1:
                    self.spawn_tile = tile
        yield False
        for location, tile in self.tiles.items():
            l, r, u, d, (x, y) = location[0] - 1, location[0] + 1, location[1] + 1, location[1] - 1, location
            dirs = (
                (l, y), (r, y), (x, u), (x, d),
                (l, u), (r, u), (l, d), (r, r)
            )

            tile.place(location, neighbors=set(loc for loc in dirs if (0 <= loc[0] < 10) and (0 <= loc[1] < 10)))
            self.tile_sprites.append(tile.sprite)

        return True


class Dungeon1(Floor):
    pass


class Dungeon2(Floor):
    pass


class Abyss1(Floor):
    pass


class Abyss2(Floor):
    pass


class Dark(Floor):
    pass


floors = (
    Tutorial,
    Dungeon1,
    Dungeon2,
    Abyss1,
    Abyss2,
    Dark
)
