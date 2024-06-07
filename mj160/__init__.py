import mj160.util.config as cfg
from mj160.data import load_font

from mj160.window import DragonWindow, DragonView


def initialise(_config: cfg.config):
    cfg.update_config(_config)
    load_font("gohu")


def launch(next_view: type[DragonView]):
    win = DragonWindow(next_view)
    win.run()
