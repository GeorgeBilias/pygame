import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)  # call the parent class constructor
        self.image = surf  # set the image
        self.rect = self.image.get_rect(topleft=pos)  # set the rect
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.7)


class Water(Generic):
    def __init__(self, pos, frames, groups):
        # animation setup
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        super().__init__(pos=pos, surf=self.frames[self.frame_index], groups=groups, z=LAYERS['water'])

    # animation

    def animate(self, dt):
        self.frame_index += 5 * dt  # increase frame index
        if self.frame_index >= len(self.frames):  # if we are at the end of the animation
            self.frame_index = 0  # reset frame index
        self.image = self.frames[int(self.frame_index)]  # set image to current frame

    def update(self, dt):
        self.animate(dt)  # animate the sprite


class WildFlower(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height*0.9)


class Tree(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)

