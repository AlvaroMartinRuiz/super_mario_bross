from blocks import Block


class Flag(Block):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @property
    def sprite(self):
        return 0, 32, 80, 16, 16
