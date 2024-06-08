from random import seed, randint


from mj160.floors import Floor, floors


class _RunState:

    def __init__(self):
        self.run_started: bool = False
        self.runs: int = 0

        self.run_seed: int = None
        self.floor_seed: int = None

        self.floor_num = 0
        self.floor: Floor = None

    def hard_reset(self):
        """
        Reset as if the game just launched
        """
        self.run_started: bool = False
        self.runs = 0

        self.run_seed: int = None
        self.floor_seed: int = None

        self.floor_num = 0
        self.floor: Floor = None

    def run_reset(self):
        """
        reset as if a new run started
        """
        self.run_started: bool = False
        self.floor_num = 0
        if self.floor:
            self.floor.cleanup()
        self.floor = None

    def run_start(self):
        self.run_started: bool = True
        self.floor_num = 0

        seed(randint(0, 0xFFFFFF))
        self.run_seed = randint(0, 0xFFFFFF)

    def floor_start(self):
        if self.floor_num >= len(floors):
            raise ValueError("Gone past the final floor")

        seed(self.run_seed << self.floor_num)
        self.floor_seed = randint(0, 0xFFFFFF)

        self.floor = floors[self.floor_num](self.floor_seed)
        self.floor_num += 1


RunState = _RunState()