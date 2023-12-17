import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer):
        super().__init__(group)

        self.fatigue = 0
        self.tired = 0  # not tired
        self.animations = {}  # create a directory for animations
        self.import_assets()  # run the function to import the assets
        self.status = 'down_idle'
        self.frame_index = 0

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
            'seed switch': Timer(180)  # add a timer to not go out of range

        }

        # tools
        self.tools = ['hoe', 'axe', 'water']  # set the tools available
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

        # interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer

    def use_tool(self):  # function for using tool
        print("tool use")
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)  # hit ground with hoe

        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):  # if the axe is colliding with tree
                    tree.damage()

        if self.selected_tool == 'water':
            pass

    def get_target_(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def use_seed(self):  # function for using tool
        # print(self.selected_tool) # just a print for now
        pass

    def import_assets(self):
        # adding player states
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [],
                           'left_idle': [], 'up_idle': [], 'down_idle': [], 'right_hoe': [],
                           'left_hoe': [], 'up_hoe': [], 'down_hoe': [], 'right_axe': [],
                           'left_axe': [], 'up_axe': [], 'down_axe': [], 'right_water': [],
                           'left_water': [], 'up_water': [], 'down_water': []}

        for animation in self.animations.keys():
            full_path = 'Animations_stolen/Animations/graphics/character/' + animation  # path of animations
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
                print("up")
            elif keys[pygame.K_s]:  # pressing the s button to go down
                self.direction.y = 1  # set the direction to down
                self.status = 'down'
            else:
                self.direction.y = 0  # user stopped pressing key therefore player doesn't move anymore vertically

            # horizontal movement
            if keys[pygame.K_a]:  # pressing the "a" button to go left
                self.direction.x = -1  # setting direction to go left
                self.status = 'left'
            elif keys[pygame.K_d]:  # pressing the d button to go right
                self.direction.x = 1  # setting direction to go right
                self.status = 'right'
            else:
                self.direction.x = 0  # user stopped pressing key therefore player doesn't move anymore horizontal

            # sprinting
            if keys[pygame.K_LSHIFT]:
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

    def get_status(self):
        # if player is not moving
        if self.direction.magnitude() == 0:
            # add _idle to show he is not moving
            self.status = self.status.split('_')[
                              0] + '_idle'  # we only want _idle once at the end of the name of the status , prevents
            # duplicate for example _idle_idle

        # If tool use is active
        if self.timers['tool use'].active:
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
                    if direction == 'horizontal':  # check collision when moving horizontaly
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx  # updating rect of player (where he appears on screen , for example behind flower)
                        self.pos.x = self.hitbox.centerx

                    # !! EXPLANATION !! , if player is coming towards a flower from the left and his right sprite
                    # collides with left sprite of flower make the players position on the left of the flower , vice verca with the other side and vertically

                    if direction == 'vertical':  # check collision when moving verticaly
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

    def update(self, dt):  # update player input to the screen
        self.input()
        self.get_status()
        self.move(dt)
        self.get_target_()
        self.animate(dt)
        self.update_timers()
