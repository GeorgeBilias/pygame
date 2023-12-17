import pygame
from settings import *
from pytmx.util_pygame import load_pygame


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']


class SoilLayer:
    def __init__(self, all_sprites):

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # graphics
        self.soil_surf = pygame.image.load('Animations_stolen/Animations/graphics/soil/o.png')

        self.create_soil_grid()
        self.create_hit_rects()

        # requirements :
        # if area is farm able or not ( defined in tiled program)
        # if the soil has been watered
        # if soil has a plant already or not

    def create_soil_grid(self):  # creating a grid that represents tiles in the map to manage the data
        ground = pygame.image.load('Animations_stolen/Animations/graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE
        print(h_tiles)
        print(v_tiles)

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame('Animations_stolen/Animations/data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

        # created soil grid

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):  # enumerate helps us keep track which row we are on
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):  # enumerate helps us keep track which row we are on
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    SoilTile((index_col * TILE_SIZE, index_row * TILE_SIZE), self.soil_surf,
                             [self.all_sprites, self.soil_sprites])
