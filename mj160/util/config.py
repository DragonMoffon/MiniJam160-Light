from typing import TypedDict


config: dict = TypedDict(
    "config",
    {
        "win_resolution": tuple[int, int],
        "win_min_size": tuple[int, int],
        "win_fullscreen": bool,
        "win_name": str,
        "game_fps": float,
        "game_dps": float
    }
)

CONFIG: config = {
    "win_resolution": (640, 360),
    "win_min_size": (1280, 720),
    "win_fullscreen": False,
    "win_name": 'DragonEngine',
    "game_fps": 1.0 / 120.0,
    "game_dps": 1.0 / 60.0
}


def update_config(_config: config):
    CONFIG.update(_config)
