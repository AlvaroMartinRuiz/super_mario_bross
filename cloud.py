from locatable import Locatable


class Cloud(Locatable):
    """ This class stores all the information needed for the clouds"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @property
    def sprite(self):
        return 0, 0, 80, 32, 32