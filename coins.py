from boosts import Boost


class Coin(Boost):
    """ This class stores all the information needed for the clouds"""

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @property
    def sprite(self):
        return 2, 16, 56, 16, 16




