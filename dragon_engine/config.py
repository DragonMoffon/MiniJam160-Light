from typing import TypedDict


config: dict = TypedDict(
    "config",
    {
        "win_resolution": tuple[int, int],
        "win_fullscreen": bool,
        "win_name": str,
    }
)

CONFIG: config = {
    "win_resolution": (1280, 720),
    "win_fullscreen": False,
    "win_name": 'DragonEngine'
}


def update_config(_config: config):
    CONFIG.update(_config)
