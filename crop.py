import math
import random
import time

import game_framework


from pico2d import load_image, get_time, draw_rectangle

import game_world
import play_mode
from state_machine import StateMachine

class Crop:
    image = None
    def __init__(self, x, y):
        self.width_image = 768
        self.height_image = 512

        self.count_h = 24
        self.count_v = 16

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.parent = None
        self.center_error_x = 0
        self.pos_x = x
        self.pos_y = y + 3
        self.index_h = 1
        self.index_v = 13
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = self.size_h * 1.5
        self.draw_y = self.size_v * 1.5

        self.growth = 0
        self.max_growth = 10
        self.growth_level = 0
        self.dir = 1
        #self.state = Idle
        if Crop.image == None:
            Crop.image = load_image('Crops.png')


    def get_bb(self):
        return self.pos_x - self.draw_x / 2, self.pos_y - self.draw_y / 2 - 5, self.pos_x + self.draw_x / 2 - 7, self.pos_y + self.draw_y / 2 + 7

    def handle_collision(self, group, other):
        pass






    def update(self):
        if self.growth < self.max_growth:
            self.growth += game_framework.frame_time
        print(f'growth: {self.growth}')
        if self.growth > self.max_growth / 3 * 1:
            self.growth_level = 12
            self.index_h = 2

        if self.growth >= self.max_growth / 3 * 2:
            self.growth_level = 2
            self.index_h = 3

        if self.growth >= self.max_growth:
            self.growth_level = 3
            self.index_h = 4


    def handle_event(self, event):
        pass


    def draw(self):

        self.image.clip_draw(self.index_h * self.size_h,
                           self.index_v * self.size_v,
                           self.size_h,
                           self.size_v,
                           self.pos_x,
                           self.pos_y,
                           self.size_h * 1.8, self.size_v * 1.8
                           )
