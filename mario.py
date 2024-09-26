import pyxel

from locatable import Locatable


# from blocks import Block


class Mario(Locatable):
    """ This class stores all the information needed for Mario"""

    def __init__(self, x: int, y: int, lives: int):
        """ This method creates the Mario object
        @param x the starting x of Mario
        @param y the starting y of Mario
        @param lives the number of lives mario has left
        """
        # Get x and y from Locatable
        super().__init__(x, y)
        # The lives are given in the innit and they are the same to the ones set in the board
        self.lives = lives
        # Where mario is heading
        self.direction = "right"
        # Boolean that determines if mario is jumping or not
        self.is_jumping = False
        # Boolean that determines if mario is falling or not
        self.is_falling = False
        # Boolean that determines if mario is super mario or not
        self.is_super = False
        # Boolean that determines if mario is blinking or not
        # Mario blinks when he is going back to being regular mario
        self.is_blinking = False
        # Boolean that determines when mario is mini_jumping
        # Mini_jumping refers to the movement Mario does when he jumps over an enemy
        self.is_mini_jumping = False
        # Auxiliary variable to create the jump and the blinking
        self.starting_moment_jump = 0
        self.starting_moment_blink = 0
        # Booleans that determine the collisions of mario
        self.blocked_front = False
        self.blocked_below = False
        self.blocked_back = False
        self.blocked_above = False



    # Create the sprite as a read only attribute
    # It changes depending on mario's direction and its status (super or not)
    @property
    def sprite(self):
        if self.direction == 'right':
            if not self.is_super:
                return 0, 0, 48, 16, 16
            else:
                return 0, 32, 48, 16, 16
        else:
            if not self.is_super:
                return 0, 16, 48, 16, 16
            else:
                return 0, 48, 48, 16, 16

    # Check that the local variables are correct with properties and setters
    @property
    def is_jumping(self):
        return self.__is_jumping

    @is_jumping.setter
    def is_jumping(self, is_jumping):
        if type(is_jumping) != bool:
            raise ValueError("is_jumping must be a boolean")
        else:
            self.__is_jumping = is_jumping

    @property
    def is_falling(self):
        return self.__is_falling

    @is_falling.setter
    def is_falling(self, is_falling):
        if type(is_falling) != bool:
            raise ValueError("is_falling must be a boolean")
        else:
            self.__is_falling = is_falling


    @property
    def is_super(self):
        return self.__is_super

    @is_super.setter
    def is_super(self, is_super):
        if type(is_super) != bool:
            raise ValueError("is_super must be a boolean")
        else:
            self.__is_super = is_super

    @property
    def is_blinking(self):
        return self.__is_blinking

    @is_blinking.setter
    def is_blinking(self, is_blinking):
        if type(is_blinking) != bool:
            raise ValueError("is_blinking must be a boolean")
        else:
            self.__is_blinking = is_blinking

    @property
    def is_mini_jumping(self):
        return self.__is_mini_jumping

    @is_mini_jumping.setter
    def is_mini_jumping(self, is_mini_jumping):
        if type(is_mini_jumping) != bool:
            raise ValueError("is_mini_jumping must be a boolean")
        else:
            self.__is_mini_jumping = is_mini_jumping

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
    def blocked_above(self):
        return self.__blocked_above

    @blocked_above.setter
    def blocked_above(self, blocked_above):
        if type(blocked_above) != bool:
            raise ValueError("blocked_above must be a boolean")
        else:
            self.__blocked_above = blocked_above

    @property
    def blocked_front(self):
        return self.__blocked_front

    @blocked_front.setter
    def blocked_front(self, blocked_front):
        if type(blocked_front) != bool:
            raise ValueError("blocked_front must be a boolean")
        else:
            self.__blocked_front = blocked_front

    @property
    def blocked_back(self):
        return self.__blocked_back

    @blocked_back.setter
    def blocked_back(self, blocked_back):
        if type(blocked_back) != bool:
            raise ValueError("blocked_back must be a boolean")
        else:
            self.__blocked_back = blocked_back

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

    @property
    def starting_moment_jump(self):
        return self.__starting_moment_jump

    @starting_moment_jump.setter
    def starting_moment_jump(self, starting_moment):
        if type(starting_moment) != int:
            raise ValueError("starting_moment_jump must be an integer ")
        else:
            self.__starting_moment_jump = starting_moment

    @property
    def starting_moment_blink(self):
        return self.__starting_moment_blink

    @starting_moment_blink.setter
    def starting_moment_blink(self, starting_moment):
        if type(starting_moment) != int:
            raise ValueError("starting_moment_blink must be an integer ")
        else:
            self.__starting_moment_blink = starting_moment

    def move(self, board_size: int):
        """ This method is used to move Mario, it receives the
        direction and the size of the board"""
        # Check the horizontal size of Mario to stop him when he reaches the center of the screen
        mario_x_size = self.sprite[3]
        if self.direction.lower() == 'right' and self.x < board_size / 2 - mario_x_size:
            self.x += 2
        # When the direction is left and the x is bigger than 0 (so that mario can´t leave the screen) ,
        # reduce the x coordinate of Mario until
        elif self.direction.lower() == 'left' and self.x > 0:
            self.x -= 2

    def jump(self, frame_count: int):
        """ This method is used to create the jump of Mario, it receives pyxel.framecount
        at every iteration. It is only used to move Mario up """

        if self.is_jumping:
            if self.starting_moment_jump + 15 > frame_count:
                self.y -= 5
            else:
                self.is_jumping = False
        elif self.is_mini_jumping:
            if self.starting_moment_jump + 5 > frame_count:
                self.y -= 5
            else:
                self.is_mini_jumping = False

    def falling(self):
        """ This method is used so that Mario falls when he is not over something and he is not jumping """
        if not self.blocked_below and not self.is_jumping and not self.is_mini_jumping:
            self.y += 5
            self.is_falling = True
        else:
            self.is_falling = False

    def blinking(self, frame_count: int):
        """ This method is used so that Mario blinks when he is going back from Super Mario
        to regular Mario """
        if self.starting_moment_blink + 30 > frame_count:
            if frame_count % 2 == 0:
                self.is_super = True
            else:
                self.is_super = False

        else:
            self.is_blinking = False
            self.is_super = False
