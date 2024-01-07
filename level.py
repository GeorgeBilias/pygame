# import pygame
# from settings import *

from pytmx.util_pygame import load_pygame

from overlay import Overlay
from player import Player
from soil import SoilLayer
from sprites import *
from support import *
from transition import Transition
from sky import Rain, Sky
from random import randint
from menu import Menu


class Level:
    def __init__(self):
        # Get the display surface
        self.player = None
        self.display_surface = pygame.display.get_surface()

        # Sprite groups to manage game objects
        self.all_sprites = CameraGroup()  # This is a group for all sprites in the game
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.cow_sprites = pygame.sprite.Group()
        self.chicken_sprites = pygame.sprite.Group()
        self.pig_sprites = pygame.sprite.Group()
        self.buffallo_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)

        self.setup()
        self.overlay = Overlay(self.player)  # setting up Overlay class
        self.transition = Transition(self.reset, self.player)

        # sky
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) > 3
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        # shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False

        self.success = pygame.mixer.Sound('Animations/Animations/audio/success.wav')
        self.success.set_volume(0.2)

        self.music = pygame.mixer.Sound('Animations/Animations/audio/music.mp3')
        self.music.play(loops=-1)
        self.music.set_volume(0.1)

    def setup(self):

        tmx_data = load_pygame('Animations/Animations/data/map.tmx')  # loading tmx file

        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surface in tmx_data.get_layer_by_name(layer).tiles():
                Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surface, groups=self.all_sprites,
                        z=LAYERS['house bottom'])  # adding house bottom

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surface in tmx_data.get_layer_by_name(layer).tiles():
                Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surface, groups=self.all_sprites)  # adding house top

        # fence
        for x, y, surface in tmx_data.get_layer_by_name('Fence').tiles():
            Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surface, groups=[self.all_sprites, self.collision_sprites])

        # water
        water_frames = import_folder('Animations/Animations/graphics/water')  # importing water frames
        for x, y, surface in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)  # adding water

        # wild flowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])  # adding wild flowers

        # trees

        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], obj.name,
                 self.player_add, self.all_sprites)

        # cows
        for obj in tmx_data.get_layer_by_name('Cows'):
            Cow((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.cow_sprites], obj.name,
                self.feed_player)

        # chicken
        for obj in tmx_data.get_layer_by_name('Chickens'):
            Chicken((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.chicken_sprites],
                    obj.name,
                    self.feed_player)

        # pigs
        for obj in tmx_data.get_layer_by_name('Pigs'):
            Pig((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.pig_sprites], obj.name,
                self.feed_player)

        # buffallos
        for obj in tmx_data.get_layer_by_name('Buffallos'):
            Buffallo((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.buffallo_sprites],
                     obj.name,
                     self.feed_player)

        # collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():  # USING SET COLLISIONS FOR MAP MADE IN TILED
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.tree_sprites,
                                     self.cow_sprites, self.chicken_sprites, self.pig_sprites, self.buffallo_sprites,
                                     self.interaction_sprites, self.soil_layer, self.toggle_shop)  # initialising player

            if obj.name == 'Bed':  # creating area to sleep
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

            if obj.name == 'Trader':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

        Generic(pos=(0, 0),
                surf=pygame.image.load('Animations/Animations/graphics/world/ground.png').convert_alpha(),
                groups=self.all_sprites, z=LAYERS['ground'])  # adding ground

    def player_add(self, item):  # add item to inventory after some action
        self.player.xp += 10
        self.player.item_inventory[item] += 1
        self.success.play()

    def feed_player(self, animal):
        self.player.xp += 10
        if animal == "Cow":
            self.player.add_hunger_cow()
            if self.player.health + 5 > 100:
                self.player.health = 100
            else:
                self.player.health += 5
            # fed player
            print(self.player.hunger)
        if animal == "Chicken":
            self.player.add_hunger_chicken()
            if self.player.health + 5 > 100:
                self.player.health = 100
            else:
                self.player.health += 5
            # fed player
            print(self.player.hunger)
        if animal == "Pig":
            self.player.add_hunger_pig()
            if self.player.health + 5 > 100:
                self.player.health = 100
            else:
                self.player.health += 5
            # fed player
            print(self.player.hunger)
        if animal == "Buffallo":
            self.player.add_hunger_buffallo()
            if self.player.health + 10 > 100:
                self.player.health = 100
            else:
                self.player.health += 10
            # fed player
            print(self.player.hunger)

    def toggle_shop(self):
        self.shop_active = not self.shop_active

    def run(self, dt):
        # This method is called to run the level

        # Fill the display surface with a black color (background)
        self.display_surface.fill('black')

        # Draw all sprites onto the display surface
        self.all_sprites.custom_draw(self.player)

        # Update all sprites in the game, applying any changes
        if self.shop_active:
            self.menu.update()
        else:
            self.all_sprites.update(dt)  # This updates the sprites in our game
            self.plant_collision()

        # weather
        self.overlay.set_image_sword(self.player.sword_lvl)
        self.overlay.set_image_axe(self.player.axe_lvl)
        self.overlay.display()

        if self.raining and not self.shop_active:
            self.rain.update()

        self.sky.display(dt)

        # transition overlay
        if self.player.sleep:
            self.transition.play()  # play animation for sleeping (calls reset too)

    def respawn_animals(self, tmx_data):
        # cows
        for obj in tmx_data.get_layer_by_name('Cows'):
            Cow((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.cow_sprites], obj.name,
                self.feed_player)
            # chicken
        for obj in tmx_data.get_layer_by_name('Chickens'):
            Chicken((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.chicken_sprites],
                    obj.name,
                    self.feed_player)

            # pigs
        for obj in tmx_data.get_layer_by_name('Pigs'):
            Pig((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.pig_sprites], obj.name,
                self.feed_player)

            # buffallos
        for obj in tmx_data.get_layer_by_name('Buffallos'):
            Buffallo((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.buffallo_sprites],
                     obj.name,
                     self.feed_player)

    def reset(self):

        # respawn animals
        self.respawn_animals(load_pygame('Animations/Animations/data/map.tmx'))

        # reset player health
        self.player.health = 100

        # plants
        self.soil_layer.update_plants()

        # soil
        self.soil_layer.remove_water()

        self.raining = randint(0, 10) > 3
        self.soil_layer.raining = self.raining
        if self.raining:  # if its raining , drop water to all already existing soils
            self.soil_layer.water_all()

        # apples reset
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()  # destroy all remaining apples
            if tree.alive:
                tree.create_fruit()
        print("level reset")

        # sky
        self.sky.start_color[0] = 255
        self.sky.start_color[1] = 255
        self.sky.start_color[2] = 255

    def plant_collision(self):
        # check if we have plants
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                # checking if the plant can be collect, and it collided with the player
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    # adding the plan to player inventory
                    self.player_add(plant.plant_type)
                    plant.kill()
                    # effect when the plan is collected
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, z=LAYERS['main'])
                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')


# camera class
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()  # call the parent class constructor
        self.display_surface = pygame.display.get_surface()  # get the display surface
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # draw the sprites
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2  # calculate the offset
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2  # calculate the offset

        for item in LAYERS:  # iterate through the layers
            for sprite in sorted(self.sprites(), key=lambda sprites: sprites.rect.center):  # iterate through the
                # sprites
                if sprite.z == LAYERS[item]:  # if the sprite is in the layer
                    offset_rect = sprite.rect.copy()  # copy the sprite rect
                    offset_rect.center -= self.offset  # apply the offset
                    self.display_surface.blit(sprite.image, offset_rect)  # blit the sprite image onto the sprite rect
