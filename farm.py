import math
import random
import time
from random import randint

import game_framework


from pico2d import load_image, get_time, draw_rectangle

import game_world
import play_mode
from chicken import Chicken
from crop import Crop
from wanderer import Wanderer
from state_machine import StateMachine

class Farm:
    image = None
    def __init__(self,map, dir, x, y):
        self.width_image = 864
        self.height_image = 1280

        self.map = map

        self.count_h = 27
        self.count_v = 40

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.ground = y
        self.center_error_x = 0
        self.pos_x = x * map.tile_size * (dir * 2 - 1)
        self.pos_y = y - 5


        self.index_h = 10 - 1
        self.index_v = 34 - 1
        self.tiles_h = 3
        self.tiles_v = 2
        self.draw_x = self.size_h * 1.5
        self.draw_y = self.size_v * 1.5

        self.crops = [Crop(self, self.pos_x + 40 * i - 80, self.ground) for i in range(5)]

        self.clip_pos_x = 0
        self.clip_pos_y = 0

        self.chicken_count = 0
        self.chicken_count_cur = 0
        self.chicken_count_max = 5

        self.dir = self.pos_x / abs(self.pos_x)

        self.tag = 'Farm'
        self.spawn_timer = 0
        self.spawn_delay = 0.0 + randint(10, 100) / 10
        #self.state = Idle
        if Farm.image == None:
            Farm.image = load_image('Props2.png')


    def get_bb(self):
        return self.pos_x - self.draw_x * 3 , self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x * 3, self.pos_y + self.draw_y / 2 + 7

    def handle_collision(self, group, other):
        pass






    def update(self):
        for crop in self.crops:
            crop.update()
        pass

    def handle_event(self, event):
        pass


    def draw(self):
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        for crop in self.crops:
            crop.draw()
