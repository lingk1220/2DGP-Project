import math
import random
import time

import game_framework
import game_world

import play_mode

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import load_image, get_time

from chicken import Chicken
from state_machine import StateMachine

from arrow import Arrow

class Archer:
    image = None
    def __init__(self, x, y):
        self.width_image = 704
        self.height_image = 320

        self.count_h = 11
        self.count_v = 5

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.center_error_x = 10
        self.pos_x = x
        self.pos_y = y
        self.dir = 1
        self.bool_shooting = 0

        self.index_h = 0
        self.index_v = 3 - 1
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 100
        self.draw_y = 100 * self.size_v / (self.size_h - self.center_error_x)
        self.min_chicken_dir = 10000
        self.state = Walk
        self.chicken_target = None
        if Archer.image == None:
            Archer.image = load_image('Archer.png')

        self.build_behavior_tree()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def get_bb(self):
        return self.pos_x - self.draw_x / 3, self.pos_y - self.draw_y / 3.5, self.pos_x + self.draw_x / 3, self.pos_y + self.draw_y / 2.5



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
        self.chicken_target = None

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

    def lockon_chicken(self, distance):
        self.min_chicken_dir = 10000000
        self.chicken_target = None
        for chicken in game_world.objects[3]:
            if chicken.__class__ == Chicken:
                chicken_dir = self.distance_get(chicken.pos_x, self.pos_x)
                if chicken_dir < distance:
                    if chicken_dir < self.min_chicken_dir:
                        self.chicken_target = chicken
        if self.chicken_target == None:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def is_target_nearby(self, distance):
        if self.chicken_target == None:
            return BehaviorTree.FAIL

        if self.distance_less_than(self.chicken_target.pos_x, self.pos_x, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_shooting(self):
        if self.bool_shooting == 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_chicken(self):
        self.state = Walk
        self.move_slightly_to(self.chicken_target.pos_x)
        if self.distance_less_than(self.chicken_target.pos_x, self.pos_x, 10):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def shoot_to_chicken(self):
        self.bool_shooting = 1
        self.state = Shoot
        self.dir = self.chicken_target.pos_x - self.pos_x
        if self.index_h < 10:
            return BehaviorTree.RUNNING
        if self.index_h >= 10:
            self.bool_shooting = 0
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
        ACT_set_reload_time = Action('Set Wait Time', self.set_wait_time, 30, 30)
        SEQ_wait_time = Sequence('Wait', ACT_set_wait_time, a0)
        SEQ_wait_reload = Sequence('Wait Reload', ACT_set_reload_time, a0)
        a1 = Action('Move to', self.move_to)

        a2 = Action('Set random location', self.set_random_location)
        root = SEQ_wander = Sequence('Wander', a2, a1, SEQ_wait_time)

        c1 = Condition('토끼가 근처에 있는가?', self.is_target_nearby, 700)
        CDT_is_shooting = Condition('화살을 발사하고 있는가', self.is_shooting)

        a3 = Action('접근', self.move_to_chicken)
        root = SEQ_chase_chicken = Sequence('토끼를 추적', c1, a3)

        c2  = Condition('토끼가 사정거리 안에 있는가?', self.is_target_nearby, 500)
        SEL_in_shoot_state = Selector('발사상태인가', CDT_is_shooting, c2)
        a4 = Action('화살 발사', self.shoot_to_chicken)
        root = SEQ_shoot_chicken = Sequence('토끼를 사냥', SEL_in_shoot_state, a4)


        a5 = Action('시야거리 내에 토끼가 있는가?', self.lockon_chicken, 700)
        #SEQ_lockon_chicken = Sequence('LockOn', c3, a5)
        SEQ_shoot_and_wait = Sequence('화살 발사 및 대기', SEQ_shoot_chicken, SEQ_wait_reload)
        SEL_hunt_chicken = Selector('사냥', SEQ_shoot_and_wait, SEQ_chase_chicken, a5 )


        root = SEL_hunt_or_wander = Selector('사냥 또는 wander', SEL_hunt_chicken, SEQ_wander)

        self.bt = BehaviorTree(root)





class Idle:
    @staticmethod
    def enter(archer, e):
        archer.idle_start_time = get_time()
        archer.index_v = 5 - 1
        archer.index_h = 0

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):
        archer.index_h = (archer.index_h + 5 * 1.5 * game_framework.frame_time) % 5


    @staticmethod
    def draw(archer):
        if archer.dir > 0:
            archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.pos_x,
                                   archer.pos_y + 29, archer.draw_x, archer.draw_y)
        else:
            archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.pos_x,
                                             archer.pos_y + 29, archer.draw_x, archer.draw_y)

class Walk:
    @staticmethod
    def enter(archer, e):
        archer.index_v = 3 - 1
        archer.index_h = 0

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):
        archer.index_h = (archer.index_h + 8 * 1.5 * game_framework.frame_time) % 8
        print(f'            {int(archer.index_h)}')

    @staticmethod
    def draw(archer):
        if archer.dir > 0:
            archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.pos_x,
                                   archer.pos_y + 29, archer.draw_x, archer.draw_y)
        else:
            archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.pos_x,
                                             archer.pos_y + 29, archer.draw_x, archer.draw_y)

class Shoot:
    @staticmethod
    def enter(archer, e):
        archer.index_v = 4 - 1
        archer.index_h = 0

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):
        archer.index_h = (archer.index_h + 11 * 1.5 * game_framework.frame_time) % 11

    @staticmethod
    def draw(archer):
        if archer.dir > 0:
            archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.pos_x,
                                   archer.pos_y + 29, archer.draw_x, archer.draw_y)
        else:
            archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.pos_x,
                                             archer.pos_y + 29, archer.draw_x, archer.draw_y)
