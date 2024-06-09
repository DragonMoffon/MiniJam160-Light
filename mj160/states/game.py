from mj160.util import CLOCK


class _GameState:

    def __init__(self):
        self.play_count: int = 0
        self.play_start: float = 0.0
        self.play_end: float = 0.0
        self.total_spirit_strength: int = 0

    def reset_game(self):
        self.play_count: int = 0
        self.play_start: float = 0.0
        self.play_end: float = 0.0
        self.total_spirit_strength: int = 0

    def next_play(self):
        self.play_count += 1
        self.play_start = CLOCK.time

    def end_play(self):
        self.play_end = CLOCK.time


GameState = _GameState()