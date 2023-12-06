import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.animations = None
        self.import_assets()  # run the function to import the assets
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]  # initialising  player animation

        self.rect = self.image.get_rect(center=pos)  # using parameters to center the player

        # movement attributes

        self.direction = pygame.math.Vector2(0, 0)  # default for now (empty)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

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

    def use_tool(self):  # function for using tool
        # print(self.selected_tool) # just a print for now
        pass

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

        if not self.timers['tool use'].active:  # if there is no timer active

            # vertical movement
            if keys[pygame.K_w]:  # pressing the w button to go up
                self.direction.y = -1  # set the direction to up
                self.status = 'up'
            elif keys[pygame.K_s]:  # pressing the s button to go down
                self.direction.y = 1  # set the direction to down
                self.status = 'down'
            else:
                self.direction.y = 0  # user stopped pressing key therefore player doesn't move anymore vertically

            # horizontal movement
            if keys[pygame.K_a]:  # pressing the a button to go left
                self.direction.x = -1  # setting direction to go left
                self.status = 'left'
            elif keys[pygame.K_d]:  # pressing the d button to go right
                self.direction.x = 1  # setting direction to go right
                self.status = 'right'
            else:
                self.direction.x = 0  # user stopped pressing key therefore player doesn't move anymore horizontal

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

    def move(self, dt):
        # normalizing a vector
        if (self.direction.magnitude() > 0):
            self.direction = self.direction.normalize()  # make the vector have a length of 1 (dividing vector by its
            # own Length)

        # updating horizontal and vertical movement separately using speed direction and delta time
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):  # update player input to the screen
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        self.update_timers()
