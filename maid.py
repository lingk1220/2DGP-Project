import math
import random
import time

import game_framework
import game_world

import play_mode

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import load_image, get_time

from crop import Crop
from state_machine import StateMachine

from arrow import Arrow

class Maid:
    image = None
    def __init__(self, x, y):
        self.width_image = 640
        self.height_image = 320

        self.count_h = 10
        self.count_v = 5

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.center_error_x = 0
        self.pos_x = x
        self.pos_y = y - 2
        self.dir = 1

        self.index_h = 0
        self.index_v = 3 - 1
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 110
        self.draw_y = 110 * self.size_v / (self.size_h - self.center_error_x)
        self.min_crop_dir = 10000
        self.state = Walk
        self.crop_target = None
        if Maid.image == None:
            Maid.image = load_image('Maid.png')

        self.build_behavior_tree()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def get_bb(self):
        return self.pos_x - self.draw_x / 3, self.pos_y - self.draw_y / 3.5, self.pos_x + self.draw_x / 3, self.pos_y + self.draw_y / 2.5 + 5



    def update(self):
        self.bt.run()
        #print(f'{self.state}')
        print(f'{self.state_machine.cur_state}')

        if self.state_machine.cur_state != self.state:
            self.state_machine.start(self.state)
        self.state_machine.update()

        pass

    def handle_event(self, event):
        pass


    def draw(self):
        self.state_machine.draw()


    def set_target_none(self):
        self.crop_target = None

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, x2, r):
        distance2 = abs(x2 - x1)
        return distance2 < 1 * r

    def distance_get(self, x1, x2):
        distance2 = x2 - x1
        return distance2

    def move_slightly_to(self, tx):
        self.dir = (tx - self.pos_x) / abs(tx - self.pos_x)
        self.speed = 100
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
        self.tx, self.ty = self.pos_x + ((2 * random.randint(0, 1)  - 1) *  random.randint(100, 101)), self.pos_y
        print(f'tx = {self.tx}')
        # self.tx, self.ty = 1000, 100
        return BehaviorTree.SUCCESS


    def wait_time(self):
        if get_time() - self.time_wait_started > self.time_wait_for:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def set_wait_time(self, min = 5, max = 30):
        self.state = Idle
        self.time_wait_started = get_time()
        self.time_wait_for = random.randint(min, max) / 10
        return BehaviorTree.SUCCESS

    def lockon_crop(self, distance):
        self.min_crop_dir = 10000000
        self.crop_target = None
        for crop in game_world.objects[2]:
            if crop.__class__ == Crop:
                crop_dir = self.distance_get(crop.pos_x, self.pos_x)
                if crop_dir < distance:
                    if crop_dir < self.min_crop_dir:
                        self.crop_target = crop
        if self.crop_target == None:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def is_target_nearby(self, distance):
        if self.crop_target == None:
            return BehaviorTree.FAIL

        crop_dir = self.distance_get(self.crop_target.pos_x, self.pos_x)
        if crop_dir < distance:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    def move_to_crop(self):
        self.state = Walk
        self.move_slightly_to(self.crop_target.pos_x)
        if self.distance_less_than(self.crop_target.pos_x, self.pos_x, 10):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def reap_crop(self):
        self.state = Reap
        self.dir = self.crop_target.pos_x - self.pos_x
        if self.index_h < 10:
            return BehaviorTree.RUNNING
        if self.index_h >= 10:
            self.dir = self.dir / abs(self.dir)
            print(f'arrow dir: {self.dir}')
            arrow = Arrow(self.pos_x + self.dir * 20, self.pos_y + 20)
            arrow.dir = self.dir
            arrow.parent = self
            play_mode.game_world.add_object(arrow, 3)
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a0 = Action('Wait', self.wait_time)
        ACT_set_wait_time = Action('Set Wait Time', self.set_wait_time)
        ACT_set_reload_time = Action('Set Wait Time', self.set_wait_time, 20, 20)
        SEQ_wait_time = Sequence('Wait', ACT_set_wait_time, a0)
        SEQ_wait_reload = Sequence('Wait Reload', ACT_set_reload_time, a0)
        a1 = Action('Move to', self.move_to)

        a2 = Action('Set random location', self.set_random_location)
        root = SEQ_wander = Sequence('Wander', a2, a1, SEQ_wait_time)

        c1 = Condition('작물이 근처에 있는가?', self.is_target_nearby, 700)
        a3 = Action('접근', self.move_to_crop)
        root = SEQ_chase_crop = Sequence('작물을 추적', c1, a3)

        c2  = Condition('작물이 수확 거리 안에 있는가?', self.is_target_nearby, 100)
        a4 = Action('화살 발사', self.reap_crop)
        root = SEQ_reap_crop = Sequence('작물을 수확', c2, a4)


        a5 = Action('시야거리 내에 작물이 있는가?', self.lockon_crop, 700)
        #SEQ_lockon_crop = Sequence('LockOn', c3, a5)
        SEQ_reap_and_wait = Sequence('작물 수확 및 대기', SEQ_reap_crop, SEQ_wait_reload)
        SEL_farming = Selector('농사', SEQ_reap_and_wait, SEQ_chase_crop, a5 )


        root = SEL_farming_or_wander = Selector('농사 또는 wander', SEL_farming, SEQ_wander)

        self.bt = BehaviorTree(root)





class Idle:
    @staticmethod
    def enter(maid, e):
        maid.idle_start_time = get_time()
        maid.index_v = 5 - 1
        maid.index_h = 0

    @staticmethod
    def exit(maid, e):
        pass

    @staticmethod
    def do(maid):
        maid.index_h = (maid.index_h + 5 * 1.5 * game_framework.frame_time) % 5


    @staticmethod
    def draw(maid):
        if maid.dir > 0:
            maid.image.clip_draw(int(maid.index_h) * maid.size_h,
                                   maid.index_v * maid.size_v,
                                   maid.size_h - maid.center_error_x,
                                   maid.size_v,
                                   maid.pos_x,
                                   maid.pos_y + 29, maid.draw_x, maid.draw_y)
        else:
            maid.image.clip_composite_draw(int(maid.index_h) * maid.size_h,
                                             maid.index_v * maid.size_v,
                                             maid.size_h - maid.center_error_x,
                                             maid.size_v,
                                             0,
                                             'h',
                                             maid.pos_x,
                                             maid.pos_y + 29, maid.draw_x, maid.draw_y)

class Walk:
    @staticmethod
    def enter(maid, e):
        maid.index_v = 3 - 1
        maid.index_h = 0

    @staticmethod
    def exit(maid, e):
        pass

    @staticmethod
    def do(maid):
        maid.index_h = (maid.index_h + 8 * 1.5 * game_framework.frame_time) % 8
        print(f'            {int(maid.index_h)}')

    @staticmethod
    def draw(maid):
        if maid.dir > 0:
            maid.image.clip_draw(int(maid.index_h) * maid.size_h,
                                   maid.index_v * maid.size_v,
                                   maid.size_h - maid.center_error_x,
                                   maid.size_v,
                                   maid.pos_x,
                                   maid.pos_y + 29, maid.draw_x, maid.draw_y)
        else:
            maid.image.clip_composite_draw(int(maid.index_h) * maid.size_h,
                                             maid.index_v * maid.size_v,
                                             maid.size_h - maid.center_error_x,
                                             maid.size_v,
                                             0,
                                             'h',
                                             maid.pos_x,
                                             maid.pos_y + 29, maid.draw_x, maid.draw_y)

class Reap:
    @staticmethod
    def enter(maid, e):
        maid.index_v = 4 - 1
        maid.index_h = 0

    @staticmethod
    def exit(maid, e):
        pass

    @staticmethod
    def do(maid):
        maid.index_h = (maid.index_h + 11 * 1.5 * game_framework.frame_time) % 11

    @staticmethod
    def draw(maid):
        if maid.dir > 0:
            maid.image.clip_draw(int(maid.index_h) * maid.size_h,
                                   maid.index_v * maid.size_v,
                                   maid.size_h - maid.center_error_x,
                                   maid.size_v,
                                   maid.pos_x,
                                   maid.pos_y + 29, maid.draw_x, maid.draw_y)
        else:
            maid.image.clip_composite_draw(int(maid.index_h) * maid.size_h,
                                             maid.index_v * maid.size_v,
                                             maid.size_h - maid.center_error_x,
                                             maid.size_v,
                                             0,
                                             'h',
                                             maid.pos_x,
                                             maid.pos_y + 29, maid.draw_x, maid.draw_y)