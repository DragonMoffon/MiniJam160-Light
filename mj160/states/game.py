class _GameState:

    def __init__(self):
        self._play_count: int = 0
        self._wave_count: int = 0

    def reset_game(self):
        self._play_count: int = 0
        self._wave_count: int = 0

    def next_play(self):
        self._play_count += 1

    def next_wave(self):
        self._wave_count += 1


GameState = _GameState()