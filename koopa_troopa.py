from enemies import Enemy

class Koopa_troopa(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        self.initialx = self.x
        self.actualx = self.x

        # When Mario hits them, this variable will be False

    def move(self):
        if self.actualx == self.initialx + 128:
            self.direction = "left"
        elif self.actualx == self.initialx - 128:
            self.direction = "right"
        if self.direction == "right":
            self.x += 1
            self.actualx += 1
        elif self.direction == 'left':
            self.x -= 1
            self.actualx -= 1

    def jumpover(self):
        self.y -= 30

    @property
    def sprite(self):
        if self.direction == 'right':
            return 0, 0, 32, 16, 16  # la posición del madio mirando a la derecha
        else:
            return 0, 16, 32, 16, 16
