class Locatable:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if type(x) != int and type(x) != float:
            raise ValueError("X must be an integer or a float")
        # elif x > 255:
        #   raise ValueError("Eres bobo")
        else:
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if type(y) != int and type(y) != float:
            raise ValueError("y must be an integer or a float")
        elif y < 0:
            raise ValueError("y can't be smaller than zero")

        else:
            self.__y = y
