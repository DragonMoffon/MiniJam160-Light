class Clock:

    def __init__(self):
        self._elapsed_time: float = 0.0
        self._elapsed_dt: float = 0.0
        self._elapse_speed: float = 1.0
        self._current_time: float = 0.0
        self._current_dt: float = 0.0

        self._current_frame: int = 0

    def tick(self, dt: float):
        self._current_frame += 1
        self._elapsed_time += dt * self._elapse_speed
        self._current_time += dt

        self._elapsed_dt = dt * self._elapse_speed
        self._current_dt = dt

    def time_since(self, t: float):
        return self._elapsed_time - t

    def frame_since(self, f: int):
        return self._current_frame - f

    @property
    def time(self):
        return self._elapsed_time

    @property
    def dt(self):
        return self._elapsed_dt

    @property
    def engine_time(self):
        return self._current_time

    @property
    def engine_dt(self):
        return self._current_dt

    @property
    def frame(self):
        return self._current_frame


CLOCK: Clock = Clock()
