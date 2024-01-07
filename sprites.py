import pygame
from settings import *
from random import randint, choice
from menu import Menu

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
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)


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
    def __init__(self, pos, surf, groups, name, player_add,all_sprites):
        super().__init__(pos, surf, groups)

        self.all_sprites = all_sprites

        # tree attributes
        self.health = 5
        self.alive = True
        stump_path = f'Animations/Animations/graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        # self.invul_timer = Timer(200)

        # apples
        self.apples_surf = pygame.image.load('Animations/Animations/graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]  # possible apple locations from setting.py
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

        # import sound
        self.axe_sound = pygame.mixer.Sound('Animations/Animations/audio/axe.mp3')

    def damage(self, lvl):  # method for damaging the tree
        self.health -= lvl  # tree loses health

        # sound effect
        self.axe_sound.play()

        if len(self.apple_sprites.sprites()) > 0:  # check if tree has apples
            random_apple = choice(self.apple_sprites.sprites())

            # display particle when apple is destroyed
            Particle(random_apple.rect.topleft, random_apple.image, self.all_sprites, LAYERS['fruit'])

            self.player_add('apple')  # give apple to player after destroying tree

            random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            Particle(self.rect.topleft, self.image, self.all_sprites, LAYERS['fruit'], 500)
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add('wood')  # give wood after tree is chopped down

    def update(self, dt):
        if self.alive:
            self.check_death()

    def create_fruit(self):
        for pos in self.apple_pos:  # spawn apple ins random locations
            if randint(1, 10) < 5:
                print(randint(1, 10))
                print("creating apples")
                # actual pos of apple from the borders

                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                print(x, y)
                Generic((x, y), self.apples_surf, [self.apple_sprites, self.all_sprites], LAYERS['fruit'])


class Cow(Generic):
    def __init__(self, pos, surf, groups, name, feed_player):
        super().__init__(pos, surf, groups)

        # tree attributes
        self.health = 5
        self.alive = True

        self.feed_player = feed_player

        # import sound
        self.cow_hurt = pygame.mixer.Sound('Animations/Animations/audio/cow_hurt.mp3')
        self.cow_dead = pygame.mixer.Sound('Animations/Animations/audio/cow_death.mp3')
        self.cow_hurt.set_volume(0.3)
        self.rect.inflate_ip(+self.rect.width * 1.3, +self.rect.height * 1.3)
        self.image = pygame.transform.scale(self.image, (70, 70))

    def damage(self, lvl):  # method for damaging the tree

        self.health -= lvl  # cow loses health

        # sound effect
        self.cow_hurt.play()

        print("damaged")

    def check_death(self):
        if self.health <= 0:
            self.cow_dead.play()
            self.feed_player("Cow")
            print("dead")
            self.alive = False
            self.kill()

    def update(self, dt):
        if self.alive:
            self.check_death()

class Chicken(Generic):
    def __init__(self, pos, surf, groups, name, feed_player):
        super().__init__(pos, surf, groups)

        # tree attributes
        self.health = 5
        self.alive = True

        self.feed_player = feed_player

        # import sound
        self.chicken_hurt = pygame.mixer.Sound('Animations/Animations/audio/chicken_hurt.mp3')
        self.chicken_dead = pygame.mixer.Sound('Animations/Animations/audio/chicken_dead.mp3')
        self.chicken_hurt.set_volume(0.3)
        self.rect.inflate_ip(+self.rect.width * 1.3, +self.rect.height * 1.3)
        self.image = pygame.transform.scale(self.image, (70, 70))

    def damage(self, lvl):  # method for damaging the tree

        self.health -= lvl  # cow loses health

        # sound effect
        self.chicken_hurt.play()

        print("damaged")

    def check_death(self):
        if self.health <= 0:
            self.chicken_dead.play()
            self.feed_player("Chicken")
            print("dead")
            self.alive = False
            self.kill()

    def update(self, dt):
        if self.alive:
            self.check_death()

class Pig(Generic):
    def __init__(self, pos, surf, groups, name, feed_player):
        super().__init__(pos, surf, groups)

        # tree attributes
        self.health = 5
        self.alive = True

        self.feed_player = feed_player

        # import sound
        self.pig_hurt = pygame.mixer.Sound('Animations/Animations/audio/pig_hurt.mp3')
        self.pig_dead = pygame.mixer.Sound('Animations/Animations/audio/pig_dead.mp3')
        self.pig_hurt.set_volume(0.3)
        self.rect.inflate_ip(+self.rect.width * 1.3, +self.rect.height * 1.3)
        self.image = pygame.transform.scale(self.image, (70, 70))

    def damage(self, lvl):  # method for damaging the tree

        self.health -= lvl  # cow loses health

        # sound effect
        self.pig_hurt.play()

        print("damaged")

    def check_death(self):
        if self.health <= 0:
            self.pig_dead.play()
            self.feed_player("Pig")
            print("dead")
            self.alive = False
            self.kill()

    def update(self, dt):
        if self.alive:
            self.check_death()


class Buffallo(Generic):
    def __init__(self, pos, surf, groups, name, feed_player):
        super().__init__(pos, surf, groups)

        # tree attributes
        self.health = 5
        self.alive = True

        self.feed_player = feed_player

        # import sound
        self.buffallo_hurt = pygame.mixer.Sound('Animations/Animations/audio/buffallo_hurt.mp3')
        self.buffallo_dead = pygame.mixer.Sound('Animations/Animations/audio/buffallo_dead.mp3')
        self.buffallo_hurt.set_volume(0.3)
        self.rect.inflate_ip(+self.rect.width * 1.3, +self.rect.height * 1.3)
        self.image = pygame.transform.scale(self.image, (70, 70))

    def damage(self, lvl):  # method for damaging the tree

        self.health -= lvl  # cow loses health

        # sound effect
        self.buffallo_hurt.play()

        print("damaged")

    def check_death(self):
        if self.health <= 0:
            self.buffallo_dead.play()
            self.feed_player("Buffallo")
            print("dead")
            self.alive = False
            self.kill()

    def update(self, dt):
        if self.alive:
            self.check_death()



