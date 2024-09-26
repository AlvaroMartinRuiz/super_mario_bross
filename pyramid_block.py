from blocks import Block


class PyramidBlock(Block):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @property
    def sprite(self):
        return 0, 32, 64, 16, 16
