from locatable import Locatable
from mario import Mario
from goomba import Goomba
from koopa_troopa import Koopa_troopa


class Block(Locatable):
    """ This class stores all the common information needed for every different block"""

    def __init__(self, x: int, y: int):
        """ This method creates the common aspects of every block object
        @param x the starting x of the block
        @param y the starting y of the block
        """
        # Get a and y from locatable
        super().__init__(x, y)
        # Boolean that determines whether a block has been hit or not
        self.hit = False
        #
        self.starting_moment = 0

    def is_blocking_above(self, mario: Mario or Goomba or Koopa_troopa) -> bool:
        """ This method is used to know if an enemy or Mario is below a block """
        # The y coordinate of the block + 16 and the y coordinate of Mario or the enemy has to be very close
        # and the x of Mario has to be in a range around the block
        if 0 <= (mario.y - (self.y + 16)) < 5 and (self.x - 15 <= mario.x <= self.x + 14):
            mario.y = self.y + 16
            return True
        else:
            return False

    def is_blocking_below(self, mario: Mario or Goomba or Koopa_troopa) -> bool:
        """ This method is used to know if an enemy or Mario is over a block """
        # The y coordinate of the block - 16 and the y coordinate of Mario or the enemy has to be very close
        # and the x of Mario has to be in a range around the block
        if 0 <= ((self.y - 16) - mario.y) < 5 and (self.x - 15 <= mario.x <= self.x + 14):
            mario.y = self.y - 16
            return True
        else:
            return False

    def is_blocking_front(self, mario: Mario or Goomba or Koopa_troopa):
        """ This method is used to know if an enemy or Mario are next to a block from the left side of the block """
        # As Mario and the enemies do not move the same way, we have to use different booleans to check their collisions
        if type(mario) == Mario:
            # With Mario, the x of Mario and the block's x has to be either the same or have a difference of one unit,
            # while the y of Mario has to be in a range of the block's y and the block's y - 1
            if 2 > abs(mario.x + 16 - self.x) and self.y >= mario.y > self.y - 16:
                mario.x = self.x - 16
                return True
            else:
                return False
        # With koopa_troopas and goombas the x and y has to be the same
        elif type(mario) == Goomba:
            if mario.x + 16 == self.x and self.y == mario.y:
                mario.direction = "left"
                return True
            else:
                return False
        elif type(mario) == Koopa_troopa:

            if mario.x + 16 == self.x and self.y == mario.y:
                return True
            else:
                return False

    def is_blocking_back(self, mario: Mario or Goomba or Koopa_troopa):
        """ This method is used to know if an enemy or Mario are next to a block from the right side of the block """
        # In this case, the conditions are very similar to the previous function
        if type(mario) == Mario:
            if 2 > abs(mario.x - 16 - self.x) and self.y >= mario.y > self.y - 16:
                if type(mario) == Mario:
                    mario.x = self.x + 16
                return True
            else:
                return False
        elif type(mario) == Goomba:
            if mario.x - 16 == self.x and self.y == mario.y:
                mario.direction = "right"
                return True
            else:
                return False
        elif type(mario) == Koopa_troopa:
            if mario.x - 16 == self.x and self.y == mario.y:
                return True
            else:
                return False

    def mini_jump(self, frame_count):
        """ This method is used to simulate a block's jump when the block are hit """
        # The first time mini_jump is called, the y coordinate of the object is changed
        # because we change the sprite to show a coin over it
        if self.starting_moment == frame_count:
            self.y -= 16
        # Then, we do the same we did in Mario's jump but in a "shorter" way
        if self.starting_moment + 5 > frame_count:
            self.y -= 2
        elif self.starting_moment + 10 > frame_count:
            self.y += 2
        # At the end, we change the y coordinate again because the sprite is back to normal and revert the value of hit
        else:
            # Adjust the y coordinate and say that the block is no longer hit
            self.y += 16
            self.hit = False

    # Check that the local variables are correct with properties and setters

    @property
    def hit(self):
        return self.__hit

    @hit.setter
    def hit(self, hit):
        if type(hit) != bool:
            raise ValueError("hit must be a boolean")
        else:
            self.__hit = hit

    @property
    def starting_moment(self):
        return self.__starting_moment

    @starting_moment.setter
    def starting_moment(self, starting_moment):
        if type(starting_moment) != int:
            raise ValueError("starting_moment must be an integer ")
        else:
            self.__starting_moment = starting_moment
