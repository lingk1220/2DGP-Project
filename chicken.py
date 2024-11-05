import math
import random
import time

import game_framework
import play_mode

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import load_image, get_time, draw_rectangle

from state_machine import StateMachine

class Chicken:
    image = None
    def __init__(self, x, y):
        self.width_image = 576
        self.height_image = 32

        self.count_h = 18
        self.count_v = 1

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)


        self.center_error_x = 0
        self.pos_x = x
        self.pos_y = y + 10
        self.index_h = 0
        self.index_v = 0
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 70
        self.draw_y = 70
        self.color = 'white'
        self.state = Idle

        if Chicken.image == None:
            Chicken.image = load_image('chicken_' + self.color + '.png')

        play_mode.game_world.add_collision_pair('arrow:chicken', None, self)
        self.build_behavior_tree()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def get_bb(self):
        return self.pos_x - self.draw_x / 2 + 18, self.pos_y - self.draw_y / 2 , self.pos_x + self.draw_x / 2 - 18, self.pos_y + self.draw_y / 2 - 20

    def handle_collision(self, group, other):
        if group == 'arrow:chicken':
            #play_mode.game_world.remove_object(self)
            pass


    def update(self):
        self.bt.run()

        if self.state_machine.cur_state != self.state:
            self.state_machine.start(self.state)
        self.state_machine.update()
        pass

    def handle_event(self, event):
        pass


    def draw(self):

        self.state_machine.draw()







    def distance_less_than(self, x1, x2, r):
        distance2 = abs(x2 - x1)
        return distance2 < 1 * r

    def distance_get(self, x1, x2):
        distance2 = x2 - x1
        return distance2

    def move_slightly_to(self, tx):
        self.dir = (tx - self.pos_x) / abs(tx - self.pos_x)
        print(f'chic:{self.dir}')
        self.speed = 50
        self.pos_x += self.speed * self.dir * game_framework.frame_time

    def move_to(self, r=10):
        self.state = Walk
        self.move_slightly_to(self.tx)
        print(f'tx: {self.tx}, pos_x: {self.pos_x}')
        if self.distance_less_than(self.tx, self.pos_x, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        print('chick!')
        self.tx, self.ty = self.pos_x + ((2 * random.randint(0, 1)  - 1) *  random.randint(50, 120)), self.pos_y
        print(f'tx = {self.tx}')
        # self.tx, self.ty = 1000, 100
        return BehaviorTree.SUCCESS


    def wait_time(self):
        if get_time() - self.time_wait_started > self.time_wait_for:
            print("qwer")
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def set_wait_time(self, min = 5, max = 30, rnd = 0):
        if rnd:
            if random.randint(0, 1):
                self.time_wait_for = 0

                return BehaviorTree.SUCCESS

        self.state = Idle
        self.time_wait_started = get_time()
        self.time_wait_for = random.randint(min, max) / 10
        #self.time_wait_for = 100000
        return BehaviorTree.SUCCESS

    def beak_ground(self):
        self.state = Beak
        if get_time() - self.time_wait_started > self.time_wait_for:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def build_behavior_tree(self):
        a0 = Action('Wait', self.wait_time)
        ACT_wait2 = Action('Wait2', self.wait_time)
        ACT_set_wait_time = Action('Set Wait Time', self.set_wait_time, 5, 15)
        ACT_set_wait_time2 = Action('Set Wait Time2', self.set_wait_time, 5, 15)
        SEQ_wait_time = Sequence('Wait', ACT_set_wait_time, a0)

        SEQ_wait_time2 = Sequence('Wait2', ACT_set_wait_time2, ACT_wait2)
        a1 = Action('Move to', self.move_to)
        ACT_set_Beak_time = Action('Set Beak Time', self.set_wait_time, 10, 10, 1)

        ACT_Beak = Action('Beak', self.beak_ground)
        #SEL_beak = Selector('Choose Beak', )
        SEQ_beak = Sequence('Beak', ACT_set_Beak_time, ACT_Beak)
        a2 = Action('Set random location', self.set_random_location)
        root = SEQ_wander = Sequence('Wander', a2, a1, SEQ_wait_time, SEQ_beak, SEQ_wait_time2)
        self.bt = BehaviorTree(root)

class Idle:
    @staticmethod
    def enter(chicken, e):
        chicken.idle_start_time = get_time()
        chicken.index_v = 0
        chicken.index_h = 0

    @staticmethod
    def exit(chicken, e):
        pass

    @staticmethod
    def do(chicken):
        chicken.index_h = (chicken.index_h + 8 * 1.0 * game_framework.frame_time) % 8

    @staticmethod
    def draw(chicken):
        if chicken.dir > 0:
            chicken.image.clip_draw(int(chicken.index_h) * chicken.size_h,
                                   chicken.index_v * chicken.size_v,
                                   chicken.size_h - chicken.center_error_x,
                                   chicken.size_v,
                                   chicken.pos_x,
                                   chicken.pos_y, chicken.draw_x, chicken.draw_y)
        else:
            chicken.image.clip_composite_draw(int(chicken.index_h) * chicken.size_h,
                                             chicken.index_v * chicken.size_v,
                                             chicken.size_h - chicken.center_error_x,
                                             chicken.size_v,
                                             0,
                                             'h',
                                             chicken.pos_x,
                                             chicken.pos_y, chicken.draw_x, chicken.draw_y)

class Walk:
    @staticmethod
    def enter(chicken, e):
        chicken.index_v = 0
        chicken.index_h = 8

    @staticmethod
    def exit(chicken, e):
        pass

    @staticmethod
    def do(chicken):
        chicken.index_h = 8 + (chicken.index_h - 8 + 6 * 1.0 * game_framework.frame_time) % 6
        print(f'            {int(chicken.index_h)}')

    @staticmethod
    def draw(chicken):
        if chicken.dir > 0:
            chicken.image.clip_draw(int(chicken.index_h) * chicken.size_h,
                                   chicken.index_v * chicken.size_v,
                                   chicken.size_h - chicken.center_error_x,
                                   chicken.size_v,
                                   chicken.pos_x,
                                   chicken.pos_y, chicken.draw_x, chicken.draw_y)
        else:
            chicken.image.clip_composite_draw(int(chicken.index_h) * chicken.size_h,
                                             chicken.index_v * chicken.size_v,
                                             chicken.size_h - chicken.center_error_x,
                                             chicken.size_v,
                                             0,
                                             'h',
                                             chicken.pos_x,
                                             chicken.pos_y, chicken.draw_x, chicken.draw_y)


class Beak:
    @staticmethod
    def enter(chicken, e):
        chicken.index_v = 0
        chicken.index_h = 13

    @staticmethod
    def exit(chicken, e):
        pass

    @staticmethod
    def do(chicken):
        chicken.index_h = 14 + (chicken.index_h - 14 + 4 * 1.0 * game_framework.frame_time) % 4
        print(f'            {int(chicken.index_h)}')

    @staticmethod
    def draw(chicken):
        if chicken.dir > 0:
            chicken.image.clip_draw(int(chicken.index_h) * chicken.size_h,
                                   chicken.index_v * chicken.size_v,
                                   chicken.size_h - chicken.center_error_x,
                                   chicken.size_v,
                                   chicken.pos_x,
                                   chicken.pos_y, chicken.draw_x, chicken.draw_y)
        else:
            chicken.image.clip_composite_draw(int(chicken.index_h) * chicken.size_h,
                                             chicken.index_v * chicken.size_v,
                                             chicken.size_h - chicken.center_error_x,
                                             chicken.size_v,
                                             0,
                                             'h',
                                             chicken.pos_x,
                                             chicken.pos_y, chicken.draw_x, chicken.draw_y)

