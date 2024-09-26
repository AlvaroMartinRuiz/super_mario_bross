from locatable import Locatable
from mario import Mario


class Enemy(Locatable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.blocked_below = False
        self.visible = False
        self.direction = "left"

    @property
    def blocked_below(self):
        return self.__blocked_below

    @blocked_below.setter
    def blocked_below(self, blocked_below):
        if type(blocked_below) != bool:
            raise ValueError("blocked_below must be a boolean")
        else:
            self.__blocked_below = blocked_below

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, visible):
        if type(visible) != bool:
            raise ValueError("visible must be a boolean")
        else:
            self.__visible = visible

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        if type(direction) != str:
            raise ValueError("direction must be an string")
        elif direction != "left" and direction != "right":
            raise ValueError("incorrect string")
        else:
            self.__direction = direction

    def falling(self):
        self.y += 5

    def kill_mario(self, mario: Mario):
        if ((abs(self.x - mario.x) <= 10 and self.y >= mario.y > self.y - 5) or (abs(self.y - mario.y) <= 5 and self.x <= mario.x < self.x + 16)) and not mario.is_falling \
                and not mario.is_blinking:
            return True
        else:
            return False

    def mario_kills(self, mario: Mario):
        if abs(self.y - mario.y) <= 5 and self.x <= mario.x < self.x + 16 and mario.is_falling and not mario.is_blinking:
            return True
        else:
            return False
