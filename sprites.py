import pygame
from settings import *
from random import randint, choice

from timer import Timer


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)  # call the parent class constructor
        self.image = surf  # set the image
        self.rect = self.image.get_rect(topleft=pos)  # set the rect
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.7)

class Interaction(Generic):
    def __init__(self, pos, size, groups, name):  # interact with the environment class
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name

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


class Particle(Generic):  # create particle effect
    def __init__(self, pos, surf, groups, z, duration=200):
        super().__init__(pos, surf, groups, z=LAYERS['main'])
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))  # getting rid of black color
        self.image = new_surf  # make the surface white to display is getting destroyed

    def update(self, dt):
        current_time = pygame.time.get_ticks()  # get time
        if current_time - self.start_time > self.duration:
            self.kill()  # stop the particle animation if time has run out


class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add):
        super().__init__(pos, surf, groups)

        # tree atributes
        self.health = 5
        self.alive = True
        stump_path = f'Animations_stolen/Animations/graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer = Timer(200)

        # apples
        self.apples_surf = pygame.image.load('Animations_stolen/Animations/graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]  # possible apple locations from setting.py
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

    def damage(self):  # method for damaging the tree
        self.health -= 1  # tree loses health

        if len(self.apple_sprites.sprites()) > 0:  # check if tree has apples
            random_apple = choice(self.apple_sprites.sprites())

            # display particle when apple is destroyed
            Particle(random_apple.rect.topleft, random_apple.image, self.groups()[0], LAYERS['fruit'])

            self.player_add('apple')  # give apple to player after destroying tree

            random_apple.kill()


    def check_death(self):
        if self.health <= 0:
            Particle(self.rect.topleft,self.image, self.groups()[0],LAYERS['fruit'], 500)
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add('wood') # give wood after tree is chopped down

    def update(self,dt):
        if self.alive :
            self.check_death()


    def create_fruit(self):
        for pos in self.apple_pos: # spawn apple ins random locations
            if randint(0, 3) < 2:
                # actual pos of apple from the borders
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic((x, y), self.apples_surf, [self.apple_sprites, self.groups()[0]], LAYERS['fruit'])



