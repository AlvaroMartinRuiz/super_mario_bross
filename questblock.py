from blocks import Block


class QuestBlock(Block):
    """ This class stores all the information needed for the questblock"""

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @property
    def sprite(self):
        if not self.hit:
            return 0, 0, 0, 16, 16
        else:
            return 0, 32, 0, 16, 16
