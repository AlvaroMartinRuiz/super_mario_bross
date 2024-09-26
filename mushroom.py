from boosts import Boost


class Mushroom(Boost):
    """ This class stores all the information needed for the clouds"""

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @property
    def sprite(self):
        return 0, 0, 16, 16, 16
