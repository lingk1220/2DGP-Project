import math
import random
import time

import game_framework


from pico2d import load_image, get_time, draw_rectangle

import game_world
import play_mode
from state_machine import StateMachine

class Arrow:
    image = None
    def __init__(self, x, y):
        self.width_image = 30
        self.height_image = 5

        self.count_h = 1
        self.count_v = 1

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.parent = None
        self.center_error_x = 0
        self.pos_x = x
        self.pos_y = y
        self.index_h = 0
        self.index_v = 0
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = self.size_h * 1.5
        self.draw_y = self.size_v * 1.5

        self.dir = 1
        #self.state = Idle
        if Arrow.image == None:
            Arrow.image = load_image('arrow.png')

        play_mode.game_world.add_collision_pair('arrow:chicken', self, None)

    def get_bb(self):
        return self.pos_x - self.draw_x / 2, self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x / 2, self.pos_y + self.draw_y / 2

    def handle_collision(self, group, other):
        if group == 'arrow:chicken':
            play_mode.game_world.remove_object(self)
            self.parent.set_target_none()
            pass






    def update(self):
        self.pos_x += self.dir * 300 * game_framework.frame_time
        pass

    def handle_event(self, event):
        pass


    def draw(self):
        draw_rectangle(*self.get_bb())

        if self.dir < 0:
            self.image.clip_composite_draw(0,
                                           0,
                                           self.size_h,
                                           self.size_v,
                                           0,
                                           'h',
                                           self.pos_x,
                                           self.pos_y,
                                           self.size_h * 1.5, self.size_v * 1.5
                                           )
        else:
            self.image.clip_composite_draw(0,
                                           0,
                                           self.size_h,
                                           self.size_v,
                                           0,
                                           '',
                                           self.pos_x,
                                           self.pos_y,
                                           self.size_h * 1.5, self.size_v * 1.5
                                           )
