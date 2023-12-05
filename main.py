# importing libraries
import pygame
import sys

from level import Level
from settings import *


# main class
class Game:
    def __init__(self):
        pygame.init()  # Initialize the Pygame library
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set up the game window
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()  # Create a clock object to control the frame rate
        self.level = Level()  # initialise the level object

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Quit Pygame
                    sys.exit()  # Exit the program if the window is closed

            dt = self.clock.tick(60) / 1000  # set frames
            self.level.run(dt)  # run the level
            # Update game logic and draw on the screen
            # (Game logic and drawing code would be added here in a complete game)

            pygame.display.update()  # Update the display


# Check if the script is being run as the main program
if __name__ == "__main__":
    game = Game()  # Create a Game object
    game.run()  # Run the game loop
