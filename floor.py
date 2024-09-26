from mario import Mario
from blocks import Block


class Floor(Block):
    """ This class stores all the information needed for the floor blocks"""

    def __init__(self, x: int, y: int):
        """ This method creates the Floor object
        @param x the starting x of one ot the floor's blocks
        @param y the starting y of one ot the floor's blocks"""
        super().__init__(x, y)

    @property
    def sprite(self):
        return 0, 16, 64, 16, 16


