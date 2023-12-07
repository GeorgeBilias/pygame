import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)  # call the parent class constructor
        self.image = surf  # set the image
        self.rect = self.image.get_rect(topleft=pos)  # set the rect
        self.z = z
