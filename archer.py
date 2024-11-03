import math
import random
import time

import game_framework

import play_mode

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import load_image, get_time

from state_machine import StateMachine



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

        self.index_h = 0
        self.index_v = 3 - 1
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        self.min_rabbit_dir = 10000
        self.state = Walk
        self.rabbit_target = None
        if Archer.image == None:
            Archer.image = load_image('Archer.png')

        self.build_behavior_tree()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)




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



    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (1 * r) ** 2

    def distance_pow_get(self, x1, y1, x2, y2):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.pos_y, tx - self.pos_x)
        self.speed = 100
        self.pos_x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.pos_y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=10):
        self.state = Walk
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.pos_x, self.pos_y, r):
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

    def set_wait_time(self):
        self.state = Idle
        self.time_wait_started = get_time()
        self.time_wait_for = random.randint(5, 30) / 10
        return BehaviorTree.SUCCESS

    def lockon_rabbit(self, distance):
        self.min_rabbit_dir = 10000000
        self.rabbit_target = None
        for rabbit in play_mode.rabbits:
            print('bbbb')
            rabbit_dir = self.distance_pow_get(rabbit.pos_x, rabbit.pos_y, self.pos_x, self.pos_y)
            if rabbit_dir < distance ** 2:
                if rabbit_dir < self.min_rabbit_dir:
                    self.rabbit_target = rabbit
        if self.rabbit_target == None:
            return BehaviorTree.FAIL
        else:
            print('asdfasdf')
            return BehaviorTree.SUCCESS

    def is_target_nearby(self, distance):

        if self.rabbit_target == None:
            return BehaviorTree.FAIL

        rabbit_dir = self.distance_pow_get(self.rabbit_target.pos_x, self.rabbit_target.pos_y, self.pos_x, self.pos_y)
        if rabbit_dir < distance ** 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    def move_to_rabbit(self):
        self.state = Walk
        self.move_slightly_to(self.rabbit_target.pos_x, self.rabbit_target.pos_y)
        if self.distance_less_than(self.rabbit_target.pos_x, self.rabbit_target.pos_y, self.pos_x, self.pos_y, 10):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def shoot_to_rabbit(self):
        self.state = Shoot
        self.dir = self.rabbit_target.pos_x - self.pos_x
        print(f'index_h: {self.index_h}')
        if self.index_h < 10:
            return BehaviorTree.RUNNING
        if self.index_h >= 10:
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a0 = Action('Wait', self.wait_time)
        ACT_set_wait_time = Action('Set Wait Time', self.set_wait_time)
        SEQ_wait_time = Sequence('Wait', ACT_set_wait_time, a0)
        a1 = Action('Move to', self.move_to)

        a2 = Action('Set random location', self.set_random_location)
        root = SEQ_wander = Sequence('Wander', a2, a1, SEQ_wait_time)

        c1 = Condition('토끼가 근처에 있는가?', self.is_target_nearby, 700)
        a3 = Action('접근', self.move_to_rabbit)
        root = SEQ_chase_rabbit = Sequence('토끼를 추적', c1, a3)

        c2  = Condition('토끼가 사정거리 안에 있는가?', self.is_target_nearby, 500)
        a4 = Action('화살 발사', self.shoot_to_rabbit)
        root = SEQ_shoot_rabbit = Sequence('토끼를 사냥', c2, a4)


        a5 = Action('시야거리 내에 토끼가 있는가?', self.lockon_rabbit, 700)
        #SEQ_lockon_rabbit = Sequence('LockOn', c3, a5)
        SEQ_shoot_and_wait = Sequence('화살 발사 및 대기', SEQ_shoot_rabbit, SEQ_wait_time)
        SEL_hunt_rabbit = Selector('사냥', SEQ_shoot_and_wait, SEQ_chase_rabbit, a5 )


        root = SEL_hunt_or_wander = Selector('사냥 또는 wander', SEL_hunt_rabbit, SEQ_wander)

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
        if math.cos(archer.dir) > 0:
            archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.pos_x,
                                   archer.pos_y + 29, 100,
                                   100 * archer.size_v / (archer.size_h - archer.center_error_x))
        else:
            archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.pos_x,
                                             archer.pos_y + 29, 100,
                                             100 * archer.size_v / (archer.size_h - archer.center_error_x))

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
        if math.cos(archer.dir) > 0:
            archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.pos_x,
                                   archer.pos_y + 29, 100,
                                   100 * archer.size_v / (archer.size_h - archer.center_error_x))
        else:
            archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.pos_x,
                                             archer.pos_y + 29, 100,
                                             100 * archer.size_v / (archer.size_h - archer.center_error_x))

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
        if math.cos(archer.dir) > 0:
            archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.pos_x,
                                   archer.pos_y + 29, 100,
                                   100 * archer.size_v / (archer.size_h - archer.center_error_x))
        else:
            archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.pos_x,
                                             archer.pos_y + 29, 100,
                                             100 * archer.size_v / (archer.size_h - archer.center_error_x))
