import logging
from logging import WARN, DEBUG

from digiformatter import logger as digilogger

from mj160 import initialise, launch
from mj160.main_menu import MainMenuView


def setup_logging():
    logging.basicConfig(level=WARN)
    dfhandler = digilogger.DigiFormatterHandler()

    logger = logging.getLogger("mj160")
    logger.setLevel(DEBUG)
    logger.handlers = []
    logger.propagate = False
    logger.addHandler(dfhandler)


def main():
    setup_logging()

    initialise(
        {
            "win_resolution": (320, 180),
            "win_min_size": (1280, 720),
            "win_name": "Mini-Jam 160: Rogue-Light",
            "win_fullscreen": False
        }
    )
    launch(MainMenuView)


if __name__ == '__main__':
    main()
