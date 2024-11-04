import math
import random
import time

import game_framework
import play_mode

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import load_image, get_time, draw_rectangle

from state_machine import StateMachine

class Rabbit:
    image = None
    def __init__(self, x, y):
        self.width_image = 2000
        self.height_image = 2000

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
        self.draw_x = 50
        self.draw_y = 50

        #self.state = Idle
        if Rabbit.image == None:
            Rabbit.image = load_image('Rabbit.png')

        play_mode.game_world.add_collision_pair('arrow:rabbit', None, self)
        #self.build_behavior_tree()
        #self.state_machine = StateMachine(self)
        #self.state_machine.start(Idle)

    def get_bb(self):
        return self.pos_x - self.draw_x / 2, self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x / 2, self.pos_y + self.draw_y / 2

    def handle_collision(self, group, other):
        if group == 'arrow:rabbit':
            #play_mode.game_world.remove_object(self)
            pass


    def update(self):

        pass

    def handle_event(self, event):
        pass


    def draw(self):

        self.image.clip_draw(0,
                               0,
                               self.size_h,
                               self.size_v,
                               self.pos_x,
                               self.pos_y, self.draw_x,self.draw_y)
        draw_rectangle(*self.get_bb())