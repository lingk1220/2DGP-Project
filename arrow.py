import math
import random
import time

import game_framework


from pico2d import load_image, get_time

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

        self.center_error_x = 0
        self.pos_x = x
        self.pos_y = y
        self.index_h = 0
        self.index_v = 0
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0

        self.dir = 1
        #self.state = Idle
        if Arrow.image == None:
            Arrow.image = load_image('arrow.png')






    def update(self):
        self.pos_x += self.dir * 10
        pass

    def handle_event(self, event):
        pass


    def draw(self):
        print('what')

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
