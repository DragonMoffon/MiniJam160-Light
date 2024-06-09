class Brazier:

    def __init__(self):
        self._map_location: tuple[int, int]
        self._embers: int = 0
        self._last_increase: float = 0.0
        self._last_pull: float = 0.0


class _EmberState:

    def __init__(self):
        self.braziers: list[Brazier] = []


EmberState = _EmberState()
