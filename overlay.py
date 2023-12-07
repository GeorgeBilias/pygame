import pygame
from settings import *


class Overlay:
    def __init__(self, player):
        # setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        overlay_path = 'Animations_stolen/Animations/graphics/overlay/'  # path for the graphics of overlays
        self.tools_surface = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in
                              player.tools}  # tools overlay surface
        self.seeds_surface = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in
                              player.seeds}  # seeds overlay surface
        print(self.tools_surface)  # testing print
        print(self.seeds_surface)  # testing print

    def display(self):  # Display the seeds

        # tool
        tool_surface = self.tools_surface[self.player.selected_tool]  # get the tool
        tool_rectangle = tool_surface.get_rect(midbottom=OVERLAY_POSITIONS['tool'])  # and the surface destination
        self.display_surface.blit(tool_surface, tool_rectangle)  # blip
        # seeds
        seed_surface = self.seeds_surface[self.player.selected_seed]  # get the seed
        seed_rectangle = seed_surface.get_rect(midbottom=OVERLAY_POSITIONS['seed'])  # and the surface destination
        self.display_surface.blit(seed_surface, seed_rectangle)
