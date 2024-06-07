from dragon_engine.config import update_config
from dragon_engine.window import DragonWindow


def main():
    update_config(
        {
            "win_resolution": (1280, 720),
            "win_name": "Mini-Jam 160: Rogue-Light",
            "win_fullscreen": False
        }
    )
    win = DragonWindow()
    win.run()


if __name__ == '__main__':
    main()
