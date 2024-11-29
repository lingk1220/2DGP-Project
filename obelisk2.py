import math
import random
import time
from random import randint

import game_framework


from pico2d import load_image, get_time, draw_rectangle

import game_world
import play_mode
from chicken import Chicken
from skeleton import Skeleton
from wanderer import Wanderer
from state_machine import StateMachine

class Obelisk2:
    image = None
    def __init__(self,map, dir, x, y):
        self.width_image = 2600
        self.height_image = 400

        self.map = map

        self.count_h = 13
        self.count_v = 1

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.ground = y
        self.center_error_x = 0
        self.pos_x = x * map.tile_size * (dir * 2 - 1)
        self.pos_y = y + 175

        self.frame = 0

        self.index_h = 1 - 1
        self.index_v = 1 - 1

        self.draw_x = self.size_h
        self.draw_y = self.size_v


        self.clip_pos_x = 0
        self.clip_pos_y = 0

        self.enemy_count = 0
        self.enemy_count_max = 3

        self.dir = self.pos_x / abs(self.pos_x)

        self.spawn_timer = 0
        self.spawn_delay = 1.0
        #self.state = Idle
        if Obelisk2.image == None:
            Obelisk2.image = load_image('obelisk2.png')


    def get_bb(self):
        return self.pos_x - self.draw_x , self.pos_y - self.draw_y / 2 - 5, self.pos_x + self.draw_x, self.pos_y + self.draw_y / 3 + 7

    def handle_collision(self, group, other):
        pass






    def update(self):
        self.frame = (self.frame + 13 * 0.5 * game_framework.frame_time) % 13


        self.spawn_timer = self.spawn_timer + game_framework.frame_time
        if self.spawn_timer > self.spawn_delay:
            minx, _ , maxx, _ = self.get_bb()


            new_enemy = Skeleton((minx + maxx) // 2, self.ground, self)
            play_mode.game_world.add_object(new_enemy, 3)
            self.spawn_timer = 0
            self.enemy_count += 1

        pass

    def handle_event(self, event):
        pass


    def draw(self):
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y
        Obelisk2.image.clip_composite_draw(int(self.frame) * self.size_h,
                            25,
                           self.size_h,
                           self.size_v,
                           0,
                           '',
                           self.clip_pos_x,
                           self.clip_pos_y,
                           self.size_h , self.size_v - 25
                           )
