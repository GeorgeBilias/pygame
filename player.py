import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)


        # general setup
        self.image = pygame.Surface((32,64)) # initialising size of player
        self.image.fill('green') # player colour
        self.rect = self.image.get_rect(center = pos) # using parameters to center the player

        # movement attributes

        self.direction = pygame.math.Vector2(0,0) # default for now (empty)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    # adding input for the player
    # !!!!!!!
    # up is -1 (y)
    # down is 1 (y)
    # left is -1 (x)
    # right is 1 (x)
    def input(self):
        keys = pygame.key.get_pressed() # fetch all options for keys that can get pressed

        # vertical movement
        if keys[pygame.K_w]: # pressing the w button to go up
            self.direction.y = -1 # set the direction to up
        elif keys[pygame.K_s]: # pressing the s button to go down
            self.direction.y = 1 # set the direction to down
        else :
            self.direction.y = 0 # user stopped pressing key therefore player doesn't move anymore vertically



        # horizontal movement
        if keys[pygame.K_a]: # pressing the a button to go left
            self.direction.x = -1 # setting direction to go left
        elif keys[pygame.K_d]: # pressing the d button to go right
            self.direction.x = 1 # setting direction to go right
        else :
            self.direction.x = 0 # user stopped pressing key therefore player doesn't move anymore horizontal


    def move(self,dt):
        # normalizing a vector
        if (self.direction.magnitude() > 0):
            self.direction = self.direction.normalize() # make the vector have a length of 1 (dividing vector by its own Length)

        # updating horizontal and vertical movement seperately using speed direction and delta time
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y


    def update(self,dt): # update player input to the screen
        self.input()
        self.move(dt)

