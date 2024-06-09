from mj160.util import CONFIG
from random import choice


class Tile:

    def __init__(self, i_x: int, i_y: int, interactable: bool = False, walkable: bool = False):
        self.location: tuple[int, int] = i_x, i_y
        self.interactable: bool = interactable
        self.walkable: bool = walkable and not interactable

    def try_move(self):
        return self.walkable

    def try_interact(self):
        return self.interactable

    def move(self):
        pass

    def interact(self):
        pass


class _MapState:

    def __init__(self):
        self.tiles: dict[tuple[int, int], Tile] = None
        self.spawn_point: tuple[int, int] = None
        self.walkable_tiles: tuple[tuple[int, int], ...] = None

    def try_move(self, x: int, y: int):
        return self.tiles and (x, y) in self.tiles and self.tiles[(x, y)].try_move()

    def try_interact(self, x: int, y: int):
        return self.tiles and (x, y) in self.tiles and self.tiles[(x, y)].try_interact()

    def move(self, x: int, y: int):
        if not self.tiles:
            return 0.0, 0.0

        self.tiles[(x, y)].move()
        return x * CONFIG['floor_tile_size'], y * CONFIG['floor_tile_size']

    def interact(self, x: int, y: int):
        if not self.tiles:
            return

        self.tiles[(x, y)].interact()

    def get_random_walkable_tile(self):
        return choice(self.walkable_tiles)

    def set_tiles(self, tiles: dict[tuple[int, int, Tile]], spawn_point: tuple[int, int], walkable_tiles: tuple[tuple[int, int], ...]):
        self.tiles = tiles
        self.spawn_point = spawn_point
        self.walkable_tiles = walkable_tiles


MapState = _MapState()
