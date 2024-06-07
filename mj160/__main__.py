from mj160 import initialise, launch

from mj160.main_menu import MainMenuView


def main():
    initialise(
        {
            "win_resolution": (320, 180),
            "win_min_size": (1280, 820),
            "win_name": "Mini-Jam 160: Rogue-Light",
            "win_fullscreen": False
        }
    )
    launch(MainMenuView)


if __name__ == '__main__':
    main()
