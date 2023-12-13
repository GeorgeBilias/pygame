import pygame


class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration  # duration of timer
        self.func = func  # execute code after time runs out
        self.start_time = 0  # start time is 0 by default
        self.active = False  # active is false by default

    def activate(self):
        self.active = True  # set as active
        self.start_time = pygame.time.get_ticks()  # get current time

    def deactivate(self):
        self.active = False  # set as inactive
        self.start_time = 0  # reset the time to 0

    def update(self):
        current_time = pygame.time.get_ticks()  # get current time
        if current_time - self.start_time >= self.duration:  # check if timer has run out

            if self.func and self.start_time != 0:  # if there is a function
                self.func()  # execute it
            self.deactivate()  # if there is, deactivate the timer
