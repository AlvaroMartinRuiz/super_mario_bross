from blocks import Block
from mario import Mario


class Pipes(Block):
    """ This class stores all the information needed for the floor blocks"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @property
    def sprite(self):
        return 0, 48, 0, 16, 16
