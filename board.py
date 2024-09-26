import random
# Import all the classes we are going to use
from mario import Mario
from floor import Floor
from cloud import Cloud
from green_pipes import Pipes
from pyramid_block import PyramidBlock
from questblock import QuestBlock
from goomba import Goomba
from breakable_block import BreakableBlock
from koopa_troopa import Koopa_troopa
from coins import Coin
from fire_flower import Fire_flower
from mushroom import Mushroom
from flag import Flag

import pyxel


class Board:
    """ This class contains all the information needed to represent the
    board"""

    def __init__(self, w: int, h: int, mario_lives: int, score: int):
        """ This method creates the Board object.
         @param w the witdh of the board x of Mario
         @param h height of the board
         @param mario_lives the number of lives mario has left
         @param score the number of points the player has"""

        # The attributes width and height are not private because we use them in the main class.
        # The same happens with the methods update and draw
        self.width = w
        self.height = h
        self.__mario_lives = mario_lives
        self.__score = score
        # Aux variable to control when the game has to restart
        self.__restart = False
        # Variable that controls the time in the game.
        # It changes every frame, so the initial value doesn't matter
        self.__time = 0
        # This creates a Mario at the middle of the screen in x and at y = 207 facing right
        self.__mario = Mario(round(self.width / 2), 207, self.__mario_lives)
        self.__mario.x = round(self.width / 2 - self.__mario.sprite[3])
        # These variables are used to check if mario has reached the flag (ending point)
        self.__game_ends = False
        self.__blocked_score = False
        self.__final_score = 0
        # Create the floor with a loop and a list
        initial = 0
        self.__floor = []
        for i in range(120):
            if i != 17 and i != 18 and i != 42 and i != 43 and i != 78 and i != 79:
                # The previous sentence is to make some holes on the floor
                self.__floor.append(Floor(initial, 223))
                self.__floor.append(Floor(initial, 239))
            initial += 16

        # Create the clouds with a loop and a list
        self.__clouds = []
        initial_x = 50
        for i in range(9):
            # There will be a cloud every 170 pixels. The height will be random (within a range)
            self.__clouds.append(Cloud(initial_x, random.randint(40, 120)))
            initial_x += 170

        # Create the pipes using a loop and a list
        self.__pipes = []
        self.__x_of_pipes = 173
        for i in range(10):
            self.__pipes.append(Pipes(self.__x_of_pipes, 207))
            self.__x_of_pipes += 140

        # Create the enemies in fixed x positions using a loop
        self.__enemies = []
        enemies_positions_x = (232, 248, 434, 488, 578, 624, 788, 804, 904, 1004, 1114, 1200, 1400, 1500)
        for i in range(len(enemies_positions_x)):
            # Create the third, fourth, seventh and eighth enemies over quest and breakable blocks
            if i == 2 or i == 3 or i == 6 or i == 7:
                enemy_y = 143
            else:
                enemy_y = 207
            # There is a 75 % chance that is a goomba, and 25 that is a koopa troopa
            n = random.randint(0, 3)
            if n == 0:
                self.__enemies.append(Koopa_troopa(enemies_positions_x[i], enemy_y))
            else:
                self.__enemies.append(Goomba(enemies_positions_x[i], enemy_y))
        # Create some auxiliary variables that control the way enemies spawn
        self.__visiblex_right = 255  # X de la derecha de la pantalla visible
        self.__visiblex_left = self.__visiblex_right - 255  # X to the left of the screen
        self.__enemies_on_screen = 0
        # Create the question and breakable blocks, along with the boosts
        self.__quest_blocks = []
        self.__breakable_blocks = []
        self.__boosts = []
        x = 450
        for i in range(4):
            for j in range(3):
                self.__quest_blocks.append(QuestBlock(x, 159))
                self.__breakable_blocks.append(BreakableBlock(x + 16, 159))
                x += 32
            # Create question blocks over an existing row of blocks
            if random.randint(1, 4) == 4:
                self.__quest_blocks.append(QuestBlock(x - 50, 111))
            x += 240

        # Over every questblock, create a boost
        for i in range(len(self.__quest_blocks)):
            # The boost can be a coin or a mushroom. Fire flowers are created once a mushroom is taken
            n = random.randint(0, 6)
            if n < 6:
                self.__boosts.append(Coin(self.__quest_blocks[i].x, self.__quest_blocks[i].y - 16))
            else:
                self.__boosts.append(Mushroom(self.__quest_blocks[i].x, self.__quest_blocks[i].y - 16))

        # Create the pyramid/ladder with a private method
        def __create_pyramid(self, pyramid: list, x_of_pyramid_block: int,
                             y_of_pyramid_block: int, loop_length: int):
            """ This method is used to create the ladder.
            @param pyramid is the list to create the ladder/pyramid
            @param x_of_pyramid_block the starting x coordinate of that level of th pyramid
            @param y_of_pyramid_block he y coordinate of that level of th pyramid
            @param loop_length is the number of blocks that level has"""
            for k in range(loop_length):
                pyramid.append(PyramidBlock(x_of_pyramid_block, y_of_pyramid_block))
                x_of_pyramid_block += 16

        # Create the pyramid/ladder using the previous method
        self.__pyramid = []
        __create_pyramid(self, self.__pyramid, 1650, 207, 4)
        __create_pyramid(self, self.__pyramid, 1666, 191, 3)
        __create_pyramid(self, self.__pyramid, 1682, 175, 2)
        __create_pyramid(self, self.__pyramid, 1698, 159, 1)

        # Final flag
        self.__flag = Flag(1750, 207)

        # Create the coins (the ones that are on the floor)
        self.__coins = []
        self.__x_of_coins = 188
        for i in range(5):
            for j in range(4):
                self.__coins.append(Coin(self.__x_of_coins, 207))
                self.__coins[-1].visible = True
                self.__x_of_coins += 20
            self.__x_of_coins += 206

    def __check_collisions(self):
        # Check all the collisions in just one function out of the update
        # The method spawn enemies is created later
        self.__spawnenemies()
        # Mario and the enemies always started "unblocked" before we check the collisions.
        # In other words, we have to reset the values before the verifications.
        for i in range(len(self.__enemies)):
            if self.__enemies[i].visible:
                self.__enemies[i].blocked_below = False
        self.__mario.blocked_front = False
        self.__mario.blocked_back = False
        self.__mario.blocked_above = False
        self.__mario.blocked_below = False
        # Check if mario is blocked by the floor with a loop.
        # We use 'elifs' because a single block can't block Mario from different sides
        counter = 0
        while counter < len(self.__floor):
            if self.__floor[counter].is_blocking_front(self.__mario):
                self.__mario.blocked_front = True
            elif self.__floor[counter].is_blocking_above(self.__mario):
                self.__mario.blocked_above = True
            elif self.__floor[counter].is_blocking_below(self.__mario):
                self.__mario.blocked_below = True
            # Same check, but with the enemies
            for element in self.__enemies:
                if element.visible:
                    if self.__floor[counter].is_blocking_below(element):
                        element.blocked_below = True
            counter += 1

        # Continue checking if mario or the enemies are blocked by something
        for pipe in self.__pipes:
            for i in range(len(self.__enemies)):
                if self.__enemies[i].visible:
                    if type(self.__enemies[i]) == Goomba:
                        # Here, we could've used an 'or' statement and the code would have less lines,
                        # but using 'elifs' we do less checks.
                        if pipe.is_blocking_front(self.__enemies[i]):
                            # If goomba is blocked on the right,
                            # changes its direction to the left, and vice versa
                            self.__enemies[i].direction = "left"
                        elif pipe.is_blocking_back(self.__enemies[i]):
                            self.__enemies[i].direction = "right"
                        elif pipe.is_blocking_below(self.__enemies[i]):
                            self.__enemies[i].blocked_below = True

                    elif type(self.__enemies[i]) == Koopa_troopa:
                        # Koopa Troopas can jump the blocks
                        if pipe.is_blocking_front(self.__enemies[i]) or \
                                pipe.is_blocking_back(self.__enemies[i]):
                            self.__enemies[i].jumpover()
                        elif pipe.is_blocking_below(self.__enemies[i]):
                            self.__enemies[i].blocked_below = True
            if pipe.is_blocking_front(self.__mario):
                self.__mario.blocked_front = True
            elif pipe.is_blocking_back(self.__mario):
                self.__mario.blocked_back = True
            elif pipe.is_blocking_below(self.__mario):
                self.__mario.blocked_below = True

        # Check with the question blocks
        counter_boosts = 0
        for quest_block in self.__quest_blocks:
            if quest_block.is_blocking_front(self.__mario):
                self.__mario.blocked_front = True
            elif quest_block.is_blocking_back(self.__mario):
                self.__mario.blocked_back = True
            elif quest_block.is_blocking_above(self.__mario):
                self.__mario.blocked_above = True
                quest_block.hit = True
                if not self.__boosts[counter_boosts].hit:
                    self.__boosts[counter_boosts].visible = True
            elif quest_block.is_blocking_below(self.__mario):
                self.__mario.blocked_below = True

            for i in range(len(self.__enemies)):
                if self.__enemies[i].visible:
                    if type(self.__enemies[i]) == Goomba:
                        if quest_block.is_blocking_front(self.__enemies[i]):
                            self.__enemies[i].direction = "right"
                        elif quest_block.is_blocking_back(self.__enemies[i]):
                            self.__enemies[i].direction = "right"
                        elif quest_block.is_blocking_below(self.__enemies[i]):
                            self.__enemies[i].blocked_below = True
                    elif type(self.__enemies[i]) == Koopa_troopa:
                        if quest_block.is_blocking_front(self.__enemies[i]) or\
                                quest_block.is_blocking_back(self.__enemies[i]):
                            self.__enemies[i].jumpover()
                        elif quest_block.is_blocking_below(self.__enemies[i]):
                            self.__enemies[i].blocked_below = True
            counter_boosts += 1

        for pyramid_block in self.__pyramid:
            for i in range(len(self.__enemies)):
                if self.__enemies[i].visible:
                    if type(self.__enemies[i]) == Goomba:
                        if pyramid_block.is_blocking_front(self.__enemies[i]):
                            self.__enemies[i].direction = "left"
                        elif pyramid_block.is_blocking_back(self.__enemies[i]):
                            self.__enemies[i].direction = "right"
                        elif pyramid_block.is_blocking_below(self.__enemies[i]):
                            self.__enemies[i].blocked_below = True
                    elif type(self.__enemies[i]) == Koopa_troopa:
                        if pyramid_block.is_blocking_front(self.__enemies[i]) or \
                                pyramid_block.is_blocking_back(self.__enemies[i]):
                            self.__enemies[i].jumpover()
                        elif pyramid_block.is_blocking_below(self.__enemies[i]):
                            self.__enemies[i].blocked_below = True
            if pyramid_block.is_blocking_front(self.__mario):
                self.__mario.blocked_front = True
            elif pyramid_block.is_blocking_back(self.__mario):
                self.__mario.blocked_back = True
            elif pyramid_block.is_blocking_below(self.__mario):
                self.__mario.blocked_below = True

        for break_block in self.__breakable_blocks:
            if break_block.is_blocking_front(self.__mario):
                self.__mario.blocked_front = True
            elif break_block.is_blocking_back(self.__mario):
                self.__mario.blocked_back = True
            elif break_block.is_blocking_above(self.__mario):
                self.__mario.blocked_above = True
                # The starting moment is needed to do the animation of the 'minijump' of the block
                break_block.starting_moment = pyxel.frame_count
                # When hit 3 times, the breakable block are broken,
                # that is why we need to update their lives
                break_block.lives -= 1
                break_block.hit = True
                # A breakable coin with a block give us 200 points
                self.__score += 200
            elif break_block.is_blocking_below(self.__mario):
                self.__mario.blocked_below = True
            for i in range(len(self.__enemies)):
                if self.__enemies[i].visible:
                    if type(self.__enemies[i]) == Goomba:
                        if break_block.is_blocking_front(self.__enemies[i]):
                            self.__enemies[i].direction = "left"
                        elif break_block.is_blocking_back(self.__enemies[i]):
                            self.__enemies[i].direction = "right"
                        elif break_block.is_blocking_below(self.__enemies[i]):
                            self.__enemies[i].blocked_below = True
                    elif type(self.__enemies[i]) == Koopa_troopa:
                        if break_block.is_blocking_front(self.__enemies[i]) or \
                                break_block.is_blocking_back(self.__enemies[i]):
                            self.__enemies[i].jumpover()
                        elif break_block.is_blocking_below(self.__enemies[i]):
                            self.__enemies[i].blocked_below = True
        # Check if Mario has obtained a coin
        for coin in self.__coins:
            if coin.is_blocking_front(self.__mario) or coin.is_blocking_back(self.__mario) or \
                    coin.is_blocking_above(self.__mario) or coin.is_blocking_below(self.__mario):
                self.__coins.remove(coin)
                self.__score += 200
        # If Mario reaches the final flag, the game ends
        if self.__flag.is_blocking_front(self.__mario) or self.__flag.is_blocking_back(self.__mario)\
                or self.__flag.is_blocking_below(self.__mario):
            self.__game_ends = True


        counter_boosts = 0
        for boost in self.__boosts:
            # If mario is in his normal form, he can obtain a coin or a mushroom from a question blocks,
            # but if mario is in 'super mario' form, the mushrooms must be changed by fire flowers
            if type(boost) == Mushroom and self.__mario.is_super and not boost.hit:
                self.__boosts[counter_boosts] = Fire_flower(boost.x, boost.y)
            elif type(boost) == Fire_flower and not self.__mario.is_super and not boost.hit:
                self.__boosts[counter_boosts] = Mushroom(boost.x, boost.y)

            # Mario obtains the boost if it is they are on the screen (visible), and they haven't
            # been taken yet (which is controlled with the attribute hit)
            if boost.visible and not boost.hit:
                if type(boost) == Coin:
                    if boost.is_blocking_front(self.__mario) or boost.is_blocking_back(self.__mario) \
                            or boost.is_blocking_above(self.__mario) or \
                            boost.is_blocking_below(self.__mario):
                        self.__score += 200
                        boost.hit = True
                else:
                    if boost.is_blocking_front(self.__mario) or boost.is_blocking_back(self.__mario)\
                            or boost.is_blocking_above(self.__mario) \
                            or boost.is_blocking_below(self.__mario):
                        # If Mario eats a Mushroom, he transforms in SuperMario
                        self.__mario.is_super = True
                        boost.hit = True
            counter_boosts += 1

    def __spawnenemies(self):
        """ This method creates the enemies (controlling how many are on screen, the time...)"""
        self.__enemies_on_screen = 0
        counter = 0
        while counter < len(self.__enemies):
            # With the following statement we control the 'visible' part of the game, and how many
            # enemies are in there.
            if self.__visiblex_left <= self.__enemies[counter].x + 16 <= self.__visiblex_right + 32 \
                    and self.__enemies_on_screen < 4:
                self.__enemies[counter].visible = True
                self.__enemies_on_screen += 1
            else:
                self.__enemies[counter].visible = False
            # If mario kills an enemy, that enemy is removed from the list, the core is updated, and
            # Mario also performs an animation of a jump.
            if self.__enemies[counter].visible and self.__enemies[counter].mario_kills(self.__mario):
                self.__enemies.remove(self.__enemies[counter])
                self.__score += 200
                self.__mario.is_mini_jumping = True
                self.__mario.starting_moment_jump = pyxel.frame_count
            # If the enemies hit SuperMario, he returns to the normal form, and if he is already
            # in the normal form, losses a life.
            elif self.__enemies[counter].visible and self.__enemies[counter].kill_mario(self.__mario):
                if not self.__mario.is_super:
                    self.__mario.lives -= 1
                    self.__restart = True
                else:
                    self.__mario.is_super = False
                    # This folowwing attributes are for the animations where Mario transforms from
                    # SuperMario back again to Mario
                    self.__mario.is_blinking = True
                    self.__mario.starting_moment_blink = pyxel.frame_count
            counter += 1

    # UPDATE
    def update(self):

        # We have checked that (in our computer) 30 "pixel frames" last a second.
        # So we have created a timer using this equivalence
        self.__time = 400 - (round(pyxel.frame_count / 30))
        # As frame count does not restart when the time is up, we have to adjust the value of self.time,
        # adding ten until we get a positive value. If we didn't do this, time would be negative
        while self.__time < 0:
            self.__time += 400
        # If Mario falls down or the time is up, he losses a life and the game is restarted
        if self.__mario.y >= 248 or (self.__time == 0 and pyxel.frame_count % 120 == 0):
            self.__restart = True
            self.__mario.lives -= 1
        # This is how we restart the game every time Mario is killed or falls down.
        if self.__restart:
            self.__init__(255, 255, self.__mario.lives, self.__score)

        # These are the two previous methods that we created to check all the possible collisions
        # and to control the enemies
        self.__check_collisions()
        self.__spawnenemies()

        # Movement of the enemies
        for i in range(len(self.__enemies)):
            if self.__enemies[i].visible:
                self.__enemies[i].move()
                if not self.__enemies[i].blocked_below:
                    self.__enemies[i].falling()

        # Control when the breakable blocks are broken
        for element in self.__breakable_blocks:
            if element.lives == 0:
                self.__breakable_blocks.remove(element)
            if element.hit:
                element.mini_jump(pyxel.frame_count)


        # To EXIT the game:
        if pyxel.btnp(pyxel.KEY_Q) or self.__mario_lives == 0:
            pyxel.quit()

        # MARIO MOVEMENT
        # Right key:
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.__mario.direction = "right"
            # If Mario is blocked, he can't move
            if not self.__mario.blocked_front:
                self.__mario.move(self.width)

                # If Mario reaches the half of the screen, is not Mario who moves
                # but the rest of the objects.
                if self.__mario.x > self.width / 2 - self.__mario.sprite[3]:
                    self.__visiblex_right = self.__mario.x + self.width // 2
                    for block in self.__floor:
                        block.x -= 2
                    for cloud1 in self.__clouds:
                        cloud1.x -= 2
                    for pipe in self.__pipes:
                        pipe.x -= 2
                    for break_block in self.__breakable_blocks:
                        break_block.x -= 2
                    for quest_block in self.__quest_blocks:
                        quest_block.x -= 2
                    for element in self.__enemies:
                        element.x -= 2
                    for coin in self.__coins:
                        coin.x -= 2
                    for boost in self.__boosts:
                        boost.x -= 2
                    for pyramid_block in self.__pyramid:
                        pyramid_block.x -= 2
                    self.__flag.x -= 2

        # Left key
        if pyxel.btn(pyxel.KEY_LEFT):
            self.__mario.direction = "left"
            if not self.__mario.blocked_back:
                self.__mario.move(self.width)

        # Up key
        if pyxel.btn(pyxel.KEY_UP):
            # For Mario to jump, we need that Mario is over smth, nothing is blocking from above
            # and that he is not already jumping
            if not self.__mario.is_jumping and not self.__mario.blocked_above and self.__mario.blocked_below:
                self.__mario.starting_moment_jump = pyxel.frame_count
                # If Mario is not jumping yet, he starts jumping:
                self.__mario.is_jumping = True

        # If the variable is_jumping is True and Mario is not blocked from above, we call the jump method
        if (self.__mario.is_jumping or self.__mario.is_mini_jumping) and not self.__mario.blocked_above:
            self.__mario.jump(pyxel.frame_count)

        # Gravity effect
        if self.__mario.blocked_above:
            self.__mario.is_jumping = False
        self.__mario.falling()
        # Blinking effect (when transform SuperMArio to Mario)
        if self.__mario.is_blinking:
            self.__mario.blinking(pyxel.frame_count)

    # DRAW
    def draw(self):
        pyxel.cls(6)
        for element in self.__clouds:
            pyxel.blt(element.x, element.y, *element.sprite)
        # We draw Mario taking the values from the mario object
        # Parameters are x, y, image bank, the starting x and y and the size
        pyxel.blt(self.__mario.x, self.__mario.y, *self.__mario.sprite,  colkey=0)

        # Draw the floor
        for element in self.__floor:
            pyxel.blt(element.x, element.y, *element.sprite)

        # Draw the pyramid/ladder
        for element in self.__pyramid:
            pyxel.blt(element.x, element.y, *element.sprite)

        # Draw the flag
        pyxel.blt(self.__flag.x, self.__flag.y, *self.__flag.sprite, colkey=0)

        # Draw the coins
        for coin in self.__coins:
            pyxel.blt(coin.x, coin.y, *coin.sprite, colkey=0)

        # Draw the pipes
        for element in self.__pipes:
            pyxel.blt(element.x, element.y, *element.sprite)

        # DRAW THE ROW OF BLOCKS
        for quest_block in self.__quest_blocks:
            pyxel.blt(quest_block.x, quest_block.y, *quest_block.sprite, colkey=0)
        for break_block in self.__breakable_blocks:
            pyxel.blt(break_block.x, break_block.y, *break_block.sprite, colkey=0)

        # Draw the boosts (coins and special objects) of the quest blocks
        for i in range(len(self.__boosts)):
            if self.__boosts[i].visible and not self.__boosts[i].hit:
                pyxel.blt(self.__boosts[i].x, self.__boosts[i].y, *self.__boosts[i].sprite, colkey=0)

        # Goomba
        self.__spawnenemies()
        for i in range(len(self.__enemies)):
            if self.__enemies[i].visible:
                pyxel.blt(self.__enemies[i].x, self.__enemies[i].y, *self.__enemies[i].sprite, colkey=6)

        # Here we have the score, timer and the rest of text that it is above
        # with .text(x:int,y:int,text:str,color:int) we draw a text in the screen
        text = "Mario \n " + str(self.__score)
        pyxel.text(10, 10, text, 7)
        pyxel.text(140, 10, "World \n 1-1", 7)
        pyxel.text(200, 10, "Time:", 7)

        pyxel.text(210, 17, str(self.__time), 7)

        if self.__game_ends:
            if not self.__blocked_score:
                # Here, we block the score so that the final scores that appears on the screen
                # doesn't keep updating
                self.__blocked_score = True
                self.__final_score = self.__score + self.__time * 5 + self.__mario_lives * 1000
            x = pyxel.frame_count % pyxel.width
            pyxel.text(x, 50, "Final Score: " + str(self.__final_score), 3)
