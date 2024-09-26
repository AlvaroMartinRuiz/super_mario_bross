from blocks import Block


class ClearBlock(Block):
# Question blocks become clear blocks after being hit
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.sprite = (0, 32, 0, 16, 16)
