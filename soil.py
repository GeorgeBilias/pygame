import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *
from random import choice


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']

class Plant(pygame.sprite.Sprite):
    def __init__(self,plant_type, groups, soil,check_watered):
        super().__init__(groups)
        #setup the plan
        self.grow_speed = GROW_SPEED[plant_type]
        self.plant_type = plant_type
        self.frames = import_folder(f'Animations_stolen/Animations/graphics/fruit/{plant_type}')
        self.soil = soil
        self.check_watered = check_watered
        #plant age and growing speed
        self.age = 0
        self.max_age = len(self.frames)-1
        self.grow_speed: GROW_SPEED[plant_type]

        self.harvestable = False

        #sprite setup
        self.image = self.frames[self.age]
        if plant_type == 'corn':
            self.y_offset = -16
        else:
            self.y_offset = -8
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))
        self.z = LAYERS['ground plant']

    def grow(self):
        if self.check_watered(self.rect.center):

            #if the plant age > 0 the plan should be in the main layer

            if int(self.age) >0:
                self.z = LAYERS['main']
                #seting a hitbox so collision will work on the plans
                self.hitbox = self.rect.copy().inflate(-26,-self.rect.height*0.4)
            self.age += self.grow_speed
            #check if the plan is reaching max age
            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True

            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))



class SoilLayer:
    def __init__(self, all_sprites,collision_sprites):

        # sprite groups
        self.all_sprites = all_sprites
        self.collision_sprites =collision_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        # graphics
        self.soil_surfs = import_folder_dict('Animations_stolen/Animations/graphics/soil/')
        self.water_surfs = import_folder('Animations_stolen/Animations/graphics/soil_water/')
        print(self.soil_surfs)

        self.create_soil_grid()
        self.create_hit_rects()

        # requirements :
        # if area is farm able or not ( defined in tiled program)
        # if the soil has been watered
        # if soil has a plant already or not

    def create_soil_grid(self):  # creating a grid that represents tiles in the map to manage the data
        ground = pygame.image.load('Animations_stolen/Animations/graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE
        # print(h_tiles)
        # print(v_tiles)

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
                    if self.raining:
                        self.water_all()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):

                # adding entry to soil grid -> 'W'

                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')

                # creating water sprite
                WaterTile(soil_sprite.rect.topleft,choice(self.water_surfs), [self.all_sprites, self.water_sprites])

    def water_all(self):
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    WaterTile((x, y), choice(self.water_surfs), [self.all_sprites])

    def remove_water(self):

        # destroy water sprites

        for sprite in self.water_sprites.sprites():
            sprite.kill()

        # cleaning up grid

        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    #we need to check if the plans are getting water
    def check_watered(self,pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.grid[y][x]
        is_watered = 'W' in cell
        return  is_watered
    def plant_seed(self,target_pos,seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):

                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(seed,[self.all_sprites, self.plant_sprites,self.collision_sprites],soil_sprite,self.check_watered)
    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()
    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):  # enumerate helps us keep track which row we are on
            for index_col, cell in enumerate(row):
                if 'X' in cell:

                    # tile options
                    t = 'X' in self.grid[index_row - 1][index_col]
                    b = 'X' in self.grid[index_row + 1][index_col]
                    r = 'X' in row[index_col + 1]
                    l = 'X' in row[index_col - 1]

                    tile_type = 'o'

                    # if statements to check neighbour soil to decide the right png

                    # all sides
                    if all((t, b, r, l)) : tile_type = 'x'

                    # horizontal tiles only
                    if l and not any((t, r, b)):
                        tile_type = 'r'
                    if r and not any((t, l, b)):
                        tile_type = 'l'
                    if r and l and not any((t, b)):
                        tile_type = 'lr'

                    # vertical tiles only

                    if t and not any((r,l,b)):
                        tile_type = 'b'
                    if b and not any((r, l, t)):
                        tile_type = 't'
                    if b and t and not any((r, l)):
                        tile_type = 'tb'

                    # corners

                    if l and b and not any((t, r)):
                        tile_type = 'tr'
                    if l and b and not any((t, l)):
                        tile_type = 'tl'
                    if l and t and not any((b, r)):
                        tile_type = 'br'
                    if r and t and not any((b, l)):
                        tile_type = 'bl'

                    # T shapes

                    if all((t, b, r)) and not l: tile_type = 'tbr'
                    if all((t, b, l)) and not r: tile_type = 'tbl'
                    if all((l, r, t)) and not b: tile_type = 'lrb'
                    if all((l, r, b)) and not t: tile_type = 'lrt'




                    SoilTile((index_col * TILE_SIZE, index_row * TILE_SIZE), self.soil_surfs[tile_type],
                             [self.all_sprites, self.soil_sprites])
