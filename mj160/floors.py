from logging import getLogger
from typing import Generator

logger = getLogger("mj160")

class Floor:

    def __init__(self, seed_: int):
        self.seed: int = seed_

        self.generator = None
        self.generated: bool = False

    def cleanup(self):
        raise NotImplementedError()

    def _generate_floor(self) -> Generator[bool, None, bool]:
        raise NotImplementedError()

    def generate(self):
        if self.generated:
            self.generator = None
            return True

        if not self.generator:
            self.generator = self._generate_floor()
        self.generated = next(self.generator, True)

        if self.generated:
            self.generator = None

        return self.generated


class Tutorial(Floor):

    def _generate_floor(self):
        yield False
        logger.info("one two baby")

        for _ in range(1000):
            yield False

        logger.info("done yeah")

        return True


class Dungeon1(Floor):
    pass


class Dungeon2(Floor):
    pass


class Abyss1(Floor):
    pass


class Abyss2(Floor):
    pass


class Dark(Floor):
    pass


floors = (
    Tutorial,
    Dungeon1,
    Dungeon2,
    Abyss1,
    Abyss2,
    Dark
)
