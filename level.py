# import pygame
# from settings import *
from player import Player
from overlay import Overlay
from sprites import *
from pytmx.util_pygame import load_pygame
from support import *


class Level:
    def __init__(self):
        # Get the display surface
        self.player = None
        self.display_surface = pygame.display.get_surface()

        # Sprite groups to manage game objects
        self.all_sprites = CameraGroup()  # This is a group for all sprites in the game
        self.setup()
        self.overlay = Overlay(self.player)  # setting up Overlay class

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
            Generic(pos=(x * TILE_SIZE, y * TILE_SIZE), surf=surface, groups=self.all_sprites)

        # water
        water_frames = import_folder('Animations_stolen/Animations/graphics/water')  # importing water frames
        for x, y, surface in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)  # adding water

        # wild flowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, self.all_sprites)  # adding wild flowers

        # trees

        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, self.all_sprites, obj.name)

        self.player = Player((640, 360), self.all_sprites)  # initialising player
        Generic(pos=(0, 0),
                surf=pygame.image.load('Animations_stolen/Animations/graphics/world/ground.png').convert_alpha(),
                groups=self.all_sprites, z=LAYERS['ground'])  # adding ground

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
