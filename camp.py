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
        self.pos_y = y + self.size_v * 2.2 / 2 + 2


        self.index_h = 4 - 1
        self.index_v = 26 - 1
        self.tiles_h = 3
        self.tiles_v = 2
        self.draw_x = self.size_h * self.tiles_h * 2.2
        self.draw_y = self.size_v * self.tiles_v * 2.2


        self.clip_pos_x = 0
        self.clip_pos_y = 0

        self.wanderer_count = 0
        self.wanderer_count_cur = 0
        self.wanderer_count_max = 3

        self.dir = self.pos_x / abs(self.pos_x)

        self.tag = 'Camp'
        self.spawn_timer = 0
        self.spawn_delay = 0.0 + randint(10, 100) / 10
        #self.state = Idle
        if Camp.image == None:
            Camp.image = load_image('Props2.png')


    def get_bb(self):
        return self.pos_x - self.draw_x , self.pos_y - self.draw_y / 2 - 5, self.pos_x + self.draw_x, self.pos_y + self.draw_y / 3 + 7

    def handle_collision(self, group, other):
        pass






    def update(self):
        if self.wanderer_count < self.wanderer_count_max:
            self.spawn_timer += game_framework.frame_time

        if self.spawn_timer > self.spawn_delay:
            self.spawn_timer = 10.0
            self.spawn_delay = 10.0 + randint(10, 100) / 10
            self.wanderer_count += 1

        if abs(play_mode.character.pos_x - self.pos_x) > 1000:
            return

        while self.wanderer_count_cur < self.wanderer_count:
            minx, _ , maxx, _ = self.get_bb()
            # chicken = Chicken(randint(int(minx), int(maxx)), self.ground)
            # chicken.dir = self.dir
            # chicken.parent = self
            # play_mode.game_world.add_object(chicken, 2)
            # play_mode.chickens.append(chicken)

            new_wanderer = Wanderer(randint(int(minx), int(maxx)), self.ground, self)
            play_mode.game_world.add_object(new_wanderer, 3)
            self.wanderer_count_cur += 1
        pass

    def handle_event(self, event):
        pass


    def draw(self):
        if abs(play_mode.character.pos_x - self.pos_x) > 1000:
            return
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y
        if self.dir > 0:
            self.image.clip_composite_draw(self.index_h * self.size_h,
                           self.index_v * self.size_v,
                           self.size_h * self.tiles_h,
                           self.size_v * self.tiles_v,
                           0,
                           '',
                           self.clip_pos_x,
                           self.clip_pos_y,
                           self.size_h * self.tiles_h * 2.2, self.size_v * self.tiles_v * 2.2
                           )

        else:
            self.image.clip_composite_draw(self.index_h * self.size_h,
                                           self.index_v * self.size_v,
                                           self.size_h * self.tiles_h,
                                           self.size_v * self.tiles_v,
                                           0,
                                           'h',
                                           self.clip_pos_x,
                                           self.clip_pos_y,
                                           self.size_h * self.tiles_h * 2.2, self.size_v * self.tiles_v * 2.2
                                           )
