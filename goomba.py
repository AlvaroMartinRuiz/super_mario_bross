from enemies import Enemy


class Goomba(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def move(self):
        if self.direction == "right":
            self.x += 1

        elif self.direction == 'left':
            self.x -= 1

    @property
    def sprite(self):
        return 0, 48, 16, 16, 16
