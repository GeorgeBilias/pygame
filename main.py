# importing libraries
import pygame
import sys

from level import Level
from settings import *

# main class
class Game:
    def __init__(self):
        pygame.init()  # Initialize the Pygame library
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)  # Set up the game window
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()  # Create a clock object to control the frame rate
        self.level = Level()  # Initialize the level object

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
    pygame.init()

    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Start Menu")

    # Load and scale the start button image
    start_button_image = pygame.image.load("Animations_stolen/Animations/start_button.png")
    new_button_width, new_button_height = 200, 50
    start_button_image = pygame.transform.scale(start_button_image, (new_button_width, new_button_height))

    # Set the position of the start button
    start_button_rect = start_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    # Load and scale the exit button image
    exit_button_image = pygame.image.load("Animations_stolen/Animations/exit_button.png")
    exit_button_image = pygame.transform.scale(exit_button_image, (new_button_width, new_button_height))
    exit_button_rect = exit_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 170))

    # Main menu loop
    start_button_clicked = False
    exit_button_clicked = False
    while not start_button_clicked and not exit_button_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button_rect.collidepoint(x, y):
                    start_button_clicked = True
                elif exit_button_rect.collidepoint(x, y):
                    exit_button_clicked = True
                    pygame.quit()
                    sys.exit()

        # Add an image as a background
        screen.blit(pygame.image.load("Animations_stolen/Animations/background.png"), (0, 0))

        # Display the title
        font = pygame.font.Font('font/LycheeSoda.ttf', 120)

        title = font.render("PixelTerra", True, (109,109,109))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(title, title_rect)

        # Display the buttons
        screen.blit(start_button_image, start_button_rect)
        screen.blit(exit_button_image, exit_button_rect)

        pygame.display.flip()

    if start_button_clicked:
        # Run the game if the start button is clicked
        game = Game()
        game.run()
