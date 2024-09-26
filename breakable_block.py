from blocks import Block


class BreakableBlock(Block):
    """ This class stores all the information needed for the questblock"""
    def __init__(self, x: int, y: int):
        # Get x and y from Block
        super().__init__(x, y)
        # The "lives" of the block are the times it can be hit until it dissapears
        self.lives = 3


    @property
    def sprite(self):
        if self.hit:
            return 1, 48, 0, 16, 32
        else:
            return 1, 48, 16, 16, 16

    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, lives):
        if type(lives) != int:
            raise ValueError("lives must be an integer ")
        elif lives > 3:
            raise ValueError("lives can't be higher than 3")
        else:
            self.__lives = lives

