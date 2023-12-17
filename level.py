# import pygame
# from settings import *

from pytmx.util_pygame import load_pygame

from overlay import Overlay
from player import Player
from soil import SoilLayer
from sprites import *
from support import *
from transition import Transition


class Level:
    def __init__(self):
        # Get the display surface
        self.player = None
        self.display_surface = pygame.display.get_surface()

        # Sprite groups to manage game objects
        self.all_sprites = CameraGroup()  # This is a group for all sprites in the game
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.soil_layer = SoilLayer(self.all_sprites)

        self.setup()
        self.overlay = Overlay(self.player)  # setting up Overlay class
        self.transition = Transition(self.reset, self.player)

    def setup(self):

        tmx_data = load_pygame('Animations_stolen/Animations/data/map.tmx')  # loading tmx file

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
        water_frames = import_folder('Animations_stolen/Animations/graphics/water')  # importing water frames
        for x, y, surface in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)  # adding water

        # wild flowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])  # adding wild flowers

        # trees

        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], obj.name,
                 self.player_add)

        # collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():  # USING SET COLLISIONS FOR MAP MADE IN TILED
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.tree_sprites,
                                     self.interaction_sprites, self.soil_layer)  # initialising player

            if obj.name == 'Bed':  # creating area to sleep
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

        Generic(pos=(0, 0),
                surf=pygame.image.load('Animations_stolen/Animations/graphics/world/ground.png').convert_alpha(),
                groups=self.all_sprites, z=LAYERS['ground'])  # adding ground

    def player_add(self, item):  # add item to inventory after some action
        self.player.item_inventory[item] += 1

    def run(self, dt):
        # This method is called to run the level

        # print("Level running")

        # Fill the display surface with a black color (background)
        self.display_surface.fill('black')

        # Draw all sprites onto the display surface
        self.all_sprites.custom_draw(self.player)

        # Update all sprites in the game, applying any changes
        self.all_sprites.update(dt)  # This updates the sprites in our game

        # Display the overlay

        self.overlay.display()
        # print(self.player.item_inventory)

        if self.player.sleep:
            self.transition.play()  # play animation for sleeping (calls reset too)

    def reset(self):

        # apples reset
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()  # destroy all remaining apples
            if tree.alive:
                tree.create_fruit()
        print("level reset")


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
