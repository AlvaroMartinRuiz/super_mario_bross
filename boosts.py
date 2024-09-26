from blocks import Block


class Boost(Block):

    def __init__(self, x: int, y: int):
        # Get x and y from Block
        super().__init__(x, y)
        # Boolean that determines if the boost is visible or not
        self.visible = False


    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, visible):
        if type(visible) != bool:
            raise ValueError("visible must be a boolean")
        else:
            self.__visible = visible

