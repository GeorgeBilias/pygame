import pygame
from settings import *
from player import Player


class Level:
    def __init__(self):
        # Get the display surface
        self.player = None
        self.display_surface = pygame.display.get_surface()

        # Sprite groups to manage game objects
        self.all_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        self.player = Player((640, 360), self.all_sprites)  # initialising player

    def run(self, dt):
        # This method is called to run the level

        # print("Level running")

        # Fill the display surface with a black color (background)
        self.display_surface.fill('black')

        # Draw all sprites onto the display surface
        self.all_sprites.draw(self.display_surface)

        # Update all sprites in the game, applying any changes
        self.all_sprites.update(dt)  # This updates the sprites in our game
