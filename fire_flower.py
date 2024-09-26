from boosts import Boost


class Fire_flower(Boost):
    """ This class stores all the information needed for the clouds"""

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @property
    def sprite(self):
        return 2, 32, 0, 16, 16
