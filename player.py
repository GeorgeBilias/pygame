import sys

import pygame
from settings import *
from sprites import Tree
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, cow_sprites, chicken_sprites, pig_sprites,
                 buffallo_sprites, interaction, soil_layer, toggle_shop):
        super().__init__(group)
        pygame.mouse.set_visible(False)
        self.fatigue = 0
        self.hunger = 100  # max is 100
        self.health = 100  # max is 100
        self.tired = 0  # not tired
        self.animations = {}  # create a directory for animations
        self.import_assets()  # run the function to import the assets
        self.status = 'down_idle'
        self.frame_index = 0
        self.quit_button_displayed = False

        # general setup
        self.image = self.animations[self.status][self.frame_index]  # initialising  player animation

        self.rect = self.image.get_rect(center=pos)  # using parameters to center the player
        self.z = LAYERS['main']
        # movement attributes

        self.direction = pygame.math.Vector2(0, 0)  # default for now (empty)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # collision
        self.hitbox = self.rect.copy().inflate(
            (-126, -70))  # inflate takes a rectangle and changes the dimension while keeping it centered (shrinking it)
        self.collision_sprites = collision_sprites

        # timers
        self.timers = {  # create a directory with timers
            'tool use': Timer(350, self.use_tool),  # timer for using a tool
            'tool switch': Timer(200),  # add a timer to not go out of range
            'seed use': Timer(300, self.use_seed),  # timer for using a seed
            'seed switch': Timer(180),  # add a timer to not go out of range
            'health_decrease': Timer(5000, self.decrease_health)  # Initialize health decrease timer
        }

        # tools
        self.tools = ['hoe', 'axe', 'sword', 'water']  # set the tools available
        self.sword_durability = 5
        self.axe_durability = 5
        self.tool_index = 0  # set default tool
        self.selected_tool = self.tools[self.tool_index]  # set selected tool

        self.seeds = ['corn', 'tomato']
        self.seed_index = 0  # set default seed
        self.selected_seed = self.seeds[self.seed_index]  # set selected seed

        # inventory
        self.item_inventory = {
            'wood': 0,
            'apple': 0,
            'corn': 0,
            'tomato': 0
        }

        self.seed_inventory = {
            'corn': 5,
            'tomato': 5

        }

        self.sword_lvl = 1
        self.axe_lvl = 1

        self.money = 1000

        # interaction
        self.tree_sprites = tree_sprites
        self.cow_sprites = cow_sprites
        self.chicken_sprites = chicken_sprites
        self.pig_sprites = pig_sprites
        self.buffallo_sprites = buffallo_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop

        # water sound
        self.water = pygame.mixer.Sound('Animations/Animations/audio/water.mp3')
        self.water.set_volume(0.2)

        # hunger images
        self.full_steak_img = pygame.image.load("Animations/Animations/graphics/hunger/full.png")
        self.empty_steak_img = pygame.image.load("Animations/Animations/graphics/hunger/empty.png")

        # health images
        self.full_heart_img = pygame.image.load("Animations/Animations/graphics/health/full_heart.png")
        self.empty_heart_img = pygame.image.load("Animations/Animations/graphics/health/empty_heart.png")

    def use_tool(self):  # function for using tool
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)  # hit ground with hoe

        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos) and self.axe_durability > 0:  # if the axe is colliding with tree
                    if isinstance(tree, Tree):  # replace 'Tree' with the correct class name
                        tree.damage(self.axe_lvl)
                        self.axe_durability -= 1
                    else:
                        print("The object is not a Tree instance")
        if (self.selected_tool == 'sword' or self.selected_tool == 'sword1' or self.selected_tool == 'sword2' or
                self.selected_tool == 'sword3' or self.selected_tool == 'sword4' or self.selected_tool == 'sword5'):

            for cow in self.cow_sprites.sprites():
                if cow.rect.collidepoint(self.target_pos) and self.sword_durability > 0:
                    cow.damage(self.sword_lvl)
                    self.sword_durability -= 1

            for chicken in self.chicken_sprites.sprites():
                if chicken.rect.collidepoint(self.target_pos) and self.sword_durability > 0:
                    chicken.damage(self.sword_lvl)
                    self.sword_durability -= 1

            for pig in self.pig_sprites.sprites():
                if pig.rect.collidepoint(self.target_pos) and self.sword_durability > 0:
                    pig.damage(self.sword_lvl)
                    self.sword_durability -= 1

            for buffallo in self.buffallo_sprites.sprites():
                if buffallo.rect.collidepoint(self.target_pos) and self.sword_durability > 0:
                    buffallo.damage(self.sword_lvl)
                    self.sword_durability -= 1

        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
            self.water.play()

    def get_target_(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def use_seed(self):  # function for using tool
        # print(self.selected_tool) # just a print for now
        if self.seed_inventory[self.selected_seed] > 0:
            self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
            self.seed_inventory[self.selected_seed] = self.seed_inventory[self.selected_seed] - 1

    def import_assets(self):
        # adding player states
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_axe2': [], 'left_axe2': [], 'up_axe2': [], 'down_axe2': [],
                           'right_axe3': [], 'left_axe3': [], 'up_axe3': [], 'down_axe3': [],
                           'right_axe4': [], 'left_axe4': [], 'up_axe4': [], 'down_axe4': [],
                           'right_axe5': [], 'left_axe5': [], 'up_axe5': [], 'down_axe5': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': [],
                           'left_sword': [], 'up_sword': [], 'down_sword': [], 'right_sword': [],
                           'left_sword1': [], 'up_sword1': [], 'down_sword1': [], 'right_sword1': [],
                           'left_sword2': [], 'up_sword2': [], 'down_sword2': [], 'right_sword2': [],
                           'left_sword3': [], 'up_sword3': [], 'down_sword3': [], 'right_sword3': [],
                           'left_sword4': [], 'up_sword4': [], 'down_sword4': [], 'right_sword4': [],
                           'left_sword5': [], 'up_sword5': [], 'down_sword5': [], 'right_sword5': []}

        for animation in self.animations.keys():
            full_path = 'Animations/Animations/graphics/character/' + animation  # path of animations
            self.animations[animation] = import_folder(full_path)  # import the right assets

    def animate(self, dt):
        self.frame_index += 4 * dt  # use dt to iterate through phases
        if self.frame_index >= len(self.animations[self.status]):  # if the animation counter is over the limit
            self.frame_index = 0  # back to the beginning to the animation 1 -> 2 -> 3 -> 4 for example

        self.image = self.animations[self.status][int(self.frame_index)]

    # adding input for the player
    # !!!!!!!
    # up is -1 (y)
    # down is 1 (y)
    # left is -1 (x)
    # right is 1 (x)

    def input(self):

        keys = pygame.key.get_pressed()  # fetch all options for keys that can get pressed

        if not self.timers['tool use'].active and not self.sleep:  # if there is no timer active

            # vertical movement
            if keys[pygame.K_w]:  # pressing the w button to go up
                self.direction.y = -1  # set the direction to up
                self.status = 'up'
                self.remove_hunger(0.009)

            elif keys[pygame.K_s]:  # pressing the s button to go down
                self.direction.y = 1  # set the direction to down
                self.status = 'down'
                self.remove_hunger(0.009)

            else:
                self.direction.y = 0  # user stopped pressing key therefore player doesn't move anymore vertically

            # horizontal movement
            if keys[pygame.K_a]:  # pressing the "a" button to go left
                self.direction.x = -1  # setting direction to go left
                self.status = 'left'
                self.remove_hunger(0.009)

            elif keys[pygame.K_d]:  # pressing the d button to go right
                self.direction.x = 1  # setting direction to go right
                self.status = 'right'
                self.remove_hunger(0.009)

            else:
                self.direction.x = 0  # user stopped pressing key therefore player doesn't move anymore horizontal

            if keys[pygame.K_LSHIFT] and (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[
                pygame.K_d]):
                self.remove_hunger(0.02)

            # sprinting
            if keys[pygame.K_LSHIFT] and self.hunger > 20:

                if self.tired == 0:
                    self.speed = 400  # sprinting
                    self.fatigue += 0.1  # getting tired while sprinting

                if self.fatigue > 20:
                    self.tired = 1
                    self.speed = 200

            if not keys[pygame.K_LSHIFT]:  # resting
                self.speed = 200
                if self.fatigue > 0:
                    self.fatigue -= 0.1
                else:
                    self.fatigue = 0  # Ensure fatigue doesn't go below 0

                if self.fatigue == 0:
                    self.tired = 0

            # tool use
            if keys[pygame.K_SPACE]:
                # setting timer for tool use
                self.timers['tool use'].activate()  # activate the use of tool
                self.direction = pygame.math.Vector2()  # stop moving
                self.frame_index = 0  # fix frame issue by resetting the index
                self.remove_hunger(0.02)
            # seed use
            if keys[pygame.K_LCTRL]:
                # setting timer for tool use
                self.timers['seed use'].activate()  # activate the use of tool
                self.direction = pygame.math.Vector2()  # stop moving
                self.frame_index = 0  # fix frame issue by resetting the index

            # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:  # if you press Q key
                self.timers['tool switch'].activate()
                self.tool_index += 1  # Set the next tool
                # if tool index > length of tools => tool index = 0
                if self.tool_index == len(self.tools):
                    self.tool_index = 0

                self.selected_tool = self.tools[self.tool_index]  # set the new selected tool

            # change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:  # if you press Q key
                self.timers['seed switch'].activate()
                self.seed_index += 1  # Set the next tool
                # if seed index > length of seed => tool index = 0
                if self.seed_index == len(self.seeds):
                    self.seed_index = 0

                self.selected_seed = self.seeds[self.seed_index]  # set the new selected tool

            if keys[pygame.K_f]:  # going to sleep in the bed interaction area with f
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Bed':  # if we are in trader area
                        self.status = 'left_idle'
                        self.sleep = True
                    else:
                        self.toggle_shop()

            if keys[pygame.K_ESCAPE]:
                pygame.mouse.set_visible(True)
                if not self.quit_button_displayed:
                    # Display a quit button
                    new_button_width, new_button_height = 200, 50
                    exit_button_image = pygame.image.load("Animations/Animations/exit_button.png")
                    exit_button_image = pygame.transform.scale(exit_button_image, (new_button_width, new_button_height))
                    exit_button_rect = exit_button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    pygame.display.get_surface().blit(exit_button_image, exit_button_rect)
                    pygame.display.flip()
                    self.quit_button_displayed = True

                    # Wait for a button click
                    quit_clicked = False
                    while not quit_clicked:
                        pygame.event.pump()  # Process events internally
                        keys = pygame.key.get_pressed()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                x, y = event.pos
                                if exit_button_rect.collidepoint(x, y):
                                    pygame.quit()
                                    sys.exit()
                        if not keys[pygame.K_ESCAPE]:
                            self.quit_button_displayed = False
                            quit_clicked = True

                    # Remove the quit button
                    pygame.display.get_surface().fill((0, 0, 0))
                    pygame.display.flip()

    def get_status(self):
        # if player is not moving
        if self.direction.magnitude() == 0:
            # add _idle to show he is not moving
            self.status = self.status.split('_')[
                              0] + '_idle'  # we only want _idle once at the end of the name of the status , prevents
            # duplicate for example _idle_idle

        # If tool use is active
        if self.timers['tool use'].active:

            if (self.selected_tool == 'sword' and self.sword_durability > 0 ) or (self.selected_tool == 'axe' and self.axe_durability > 0):

                self.status = self.status.split('_')[
                                  0] + '_' + self.selected_tool  # set the right direction and tool for animation
                if self.sword_lvl > 1 and self.selected_tool == 'sword':
                    self.status = self.status + str(self.sword_lvl)
                if self.axe_lvl > 1 and self.selected_tool == 'axe':
                    self.status = self.status + str(self.axe_lvl)
            elif (self.selected_tool == 'sword' and self.sword_durability == 0) or (self.selected_tool == 'axe' and self.axe_durability == 0):
                    print("Tool is broken")
            else:
                self.status = self.status.split('_')[
                                  0] + '_' + self.selected_tool  # set the right direction and tool for animation
                # TODO maybe add animation for seed planting

    def update_timers(self):  # update timers continuously
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):  # check collision
                if sprite.hitbox.colliderect(self.hitbox):  # check for overlap
                    if direction == 'horizontal':  # check collision when moving horizontally
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx  # updating rect of player (where he appears on
                        # screen , for example behind flower
                        self.pos.x = self.hitbox.centerx

                    # !! EXPLANATION !! , if player is coming towards a flower from the left and his right sprite
                    # collides with left sprite of flower make the players position on the left of the flower ,
                    # vice versa with the other side and vertically

                    if direction == 'vertical':  # check collision when moving vertically
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()  # make the vector have a length of 1 dividing vector by its
            # own Length

        # updating horizontal and vertical movement separately using speed direction and delta time
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)  # updating hitbox var for x
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')  # check for collision after each movement (horizontal)

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)  # updating hitbox var for y
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')  # check for collision after each movement (vertical)

    def add_hunger_pig(self):
        if self.hunger < 100:
            self.hunger += 10
            print("fed player")

    def add_hunger_cow(self):
        if self.hunger < 100:
            self.hunger += 10

    def add_hunger_chicken(self):
        if self.hunger < 100:
            self.hunger += 8

    def add_hunger_buffallo(self):
        if self.hunger < 100:
            self.hunger += 40

    def remove_hunger(self, amount):
        if self.hunger - amount >= 0:
            self.hunger -= amount

    def return_hunger(self):
        return self.hunger

    def draw_hunger_indicator(self, hunger_level):
        x, y = SCREEN_WIDTH - 100, 45  # Top right corner
        steak_size = 0.01  # Size of each steak icon
        spacing = 40  # Spacing between steak icons
        screen = pygame.display.get_surface()

        for i in range(10):
            steak_surface = self.full_steak_img if i < hunger_level // 10 else self.empty_steak_img
            screen.blit(steak_surface, (x, y))
            x -= steak_size + spacing

    def draw_health_indicator(self, health_level):
        x, y = SCREEN_WIDTH - 100, 10  # Top right corner
        heart_size = 0.01  # Size of each steak icon
        spacing = 40  # Spacing between steak icons
        screen = pygame.display.get_surface()

        for i in range(10):
            heart_surface = self.full_heart_img if i < health_level // 10 else self.empty_heart_img
            screen.blit(heart_surface, (x, y))
            x -= heart_size + spacing

    def decrease_health(self):
        # Decrease health by 5 points
        if self.health >= 5:
            self.health -= 5
            print("Health decreased by 5")
        else:
            # If health drops below 5, stop the timer
            self.timers['health_decrease'].deactivate()

    def game_over(self):
        # Load game over image and play sound
        game_over_image = pygame.image.load("Animations/Animations/graphics/game_over/wasted.png")
        game_over_rect = game_over_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Display game over image
        pygame.display.get_surface().blit(game_over_image, game_over_rect)

        # Update the display
        pygame.display.flip()

        # Play game over sound
        game_over_sound = pygame.mixer.Sound("Animations/Animations/audio/wasted.mp3")
        game_over_sound.play()

        # Wait for a few seconds before quitting the game
        pygame.time.delay(5000)

        # Display a button to remove the game over image
        button_image = pygame.image.load("Animations/Animations/graphics/game_over/respawn.png")
        button_rect = button_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        # Display button image
        pygame.display.get_surface().blit(button_image, button_rect)
        # Update the display
        pygame.display.flip()

        # Easter egg

        if self.axe_lvl == 5 and self.sword_lvl == 3:
            easter_egg_sound = pygame.mixer.Sound("Animations/Animations/audio/easter_egg.mp3")
            easter_egg_sound.play()

        # Wait for a button click
        button_clicked = False
        while not button_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if button_rect.collidepoint(x, y):
                        button_clicked = True

        # Remove the game over image and button
        pygame.display.get_surface().fill((0, 0, 0))  # Fill the screen with black to remove previous images
        pygame.display.flip()

        # Reset player health and hunger
        self.health = 100
        self.hunger = 100

        # inventory
        self.item_inventory = {
            'wood': 0,
            'apple': 0,
            'corn': 0,
            'tomato': 0
        }

        self.seed_inventory = {
            'corn': 5,
            'tomato': 5

        }

        if self.money - 100 < 0:
            self.money = 0
        else:
            self.money -= 100

        self.pos = pygame.math.Vector2(4601, 1036)

    def update(self, dt):  # update player input to the screen
        self.input()
        self.get_status()
        self.move(dt)
        self.get_target_()
        self.animate(dt)
        self.update_timers()

        # Check if hunger is under 5
        if self.hunger < 5:
            # Activate timer to decrease health every 5 seconds
            if not self.timers['health_decrease'].active:
                self.timers['health_decrease'] = Timer(5000, self.decrease_health)
                self.timers['health_decrease'].activate()

        if self.health == 0:
            print("Game over")
            self.game_over()

        self.draw_hunger_indicator(self.hunger)
        self.draw_health_indicator(self.health)
