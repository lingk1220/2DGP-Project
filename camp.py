import math
import random
import time
from random import randint

import game_framework


from pico2d import load_image, get_time, draw_rectangle

import game_world
import play_mode
from chicken import Chicken
from wanderer import Wanderer
from state_machine import StateMachine

class Camp:
    image = None
    def __init__(self, x, y):
        self.width_image = 864
        self.height_image = 1280

        self.count_h = 27
        self.count_v = 40

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.ground = y
        self.center_error_x = 0
        self.pos_x = x
        self.pos_y = y + self.size_v * 2.2 / 2 + 6


        self.index_h = 4 - 1
        self.index_v = 26 - 1
        self.tiles_h = 3
        self.tiles_v = 2
        self.draw_x = self.size_h * self.tiles_h * 2.2
        self.draw_y = self.size_v * self.tiles_v * 2.2

        self.growth = 0
        self.max_growth = 1
        self.growth_level = 0
        self.dir = -self.pos_x / abs(self.pos_x)

        self.spawn_timer = 10.0
        self.spawn_delay = 10.0
        #self.state = Idle
        if Camp.image == None:
            Camp.image = load_image('Props2.png')


    def get_bb(self):
        return self.pos_x - self.draw_x , self.pos_y - self.draw_y / 2 - 5, self.pos_x + self.draw_x, self.pos_y + self.draw_y / 3 + 7

    def handle_collision(self, group, other):
        pass






    def update(self):
        self.spawn_timer += game_framework.frame_time

        if self.spawn_timer > self.spawn_delay:
            minx, _ , maxx, _ = self.get_bb()
            # chicken = Chicken(randint(int(minx), int(maxx)), self.ground)
            # chicken.dir = self.dir
            # chicken.parent = self
            # play_mode.game_world.add_object(chicken, 2)
            # play_mode.chickens.append(chicken)

            man = Wanderer(randint(int(minx), int(maxx)), self.ground)
            play_mode.game_world.add_object(man, 2)
            self.spawn_timer = 0
        pass

    def handle_event(self, event):
        pass


    def draw(self):
        if dir == 1:
            self.image.clip_composite_draw(self.index_h * self.size_h,
                           self.index_v * self.size_v,
                           self.size_h * self.tiles_h,
                           self.size_v * self.tiles_v,
                           0,
                           '',
                           self.pos_x,
                           self.pos_y,
                           self.size_h * self.tiles_h * 2.2, self.size_v * self.tiles_v * 2.2
                           )

        else:
            self.image.clip_composite_draw(self.index_h * self.size_h,
                                           self.index_v * self.size_v,
                                           self.size_h * self.tiles_h,
                                           self.size_v * self.tiles_v,
                                           0,
                                           'h',
                                           self.pos_x,
                                           self.pos_y,
                                           self.size_h * self.tiles_h * 2.2, self.size_v * self.tiles_v * 2.2
                                           )
