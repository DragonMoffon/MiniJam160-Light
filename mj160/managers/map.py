from typing import Protocol

from arcade import Sprite, SpriteList, Sound

from mj160.states import MapState, Tile, EmberState, Brazier, PlayerState
from mj160.util import CONFIG
from mj160.data import load_texture, load_audio

MAP = (
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),
    (1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1),
    (1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
)


class WallTile(Tile):
    pass


class FloorTile(Tile):
    pass


class EntranceTile(Tile):
    pass


class BrazierTile(Tile):
    brazier_sound: Sound = None

    def __init__(self, i_x, i_y):
        super().__init__(i_x, i_y, True, False)
        if BrazierTile.brazier_sound is None:
            BrazierTile.brazier_sound = load_audio("charge")

        self.brazier: Brazier = Brazier(i_x*CONFIG['floor_tile_size'], i_y*CONFIG['floor_tile_size'], 4)
        EmberState.add_brazier(self.brazier)

    def interact(self):
        if self.brazier.embers:
            BrazierTile.brazier_sound.play(CONFIG['game_volume'])
            PlayerState.embers = min(16, PlayerState.embers + self.brazier.pull())
            PlayerState.move_track = PlayerState.move_cost


class UpdatingTile(Protocol):

    def update(self):
        ...


class MapManager:

    def __init__(self):
        self._tile_renderer: SpriteList = None
        self._updating_tiles: tuple[UpdatingTile, ...] = ()
        self.generate()

    def generate(self):
        tiles: dict[tuple[int, int], Tile] = {}
        spawn_tile: tuple[int, int] = (0, 0)
        updating_tiles: list[UpdatingTile] = []
        walkable_tiles = []

        self._tile_renderer = SpriteList()

        for i_y in range(len(MAP)):
            column = MAP[i_y]
            for i_x in range(len(column)):
                match column[i_x]:
                    case 1:
                        tile = Tile(i_x, i_y, False, False)
                        sprite = Sprite(load_texture("game_sheet", width=16, height=16),
                                        center_x=i_x * CONFIG['floor_tile_size'],
                                        center_y=i_y * CONFIG['floor_tile_size'])
                    case 2:
                        tile = BrazierTile(i_x, i_y)
                        sprite = Sprite(load_texture("game_sheet", x=48, width=16, height=16),
                                        center_x=i_x * CONFIG['floor_tile_size'],
                                        center_y=i_y * CONFIG['floor_tile_size'])
                    case 3:
                        tile = Tile(i_x, i_y, False, True)
                        spawn_tile = (i_x, i_y)
                        sprite = Sprite(load_texture("game_sheet", x=32, width=16, height=16),
                                        center_x=i_x * CONFIG['floor_tile_size'],
                                        center_y=i_y * CONFIG['floor_tile_size'])
                    case _:
                        tile = Tile(i_x, i_y,False, True)
                        sprite = Sprite(load_texture("game_sheet", x=16, width=16, height=16),
                                        center_x=i_x * CONFIG['floor_tile_size'],
                                        center_y=i_y * CONFIG['floor_tile_size'])

                if hasattr(tile, "update") and callable(tile.update):
                    updating_tiles.append(tile)

                if tile.walkable:
                    walkable_tiles.append((i_x, i_y))

                tiles[(i_x, i_y)] = tile
                self._tile_renderer.append(sprite)

        MapState.set_tiles(tiles, spawn_tile, tuple(walkable_tiles))
        self._updating_tiles = tuple(updating_tiles)

    def update(self):
        for tile in self._updating_tiles:
            tile.update()

    def draw(self):
        if not self._tile_renderer:
            return
        self._tile_renderer.draw(pixelated=True)
