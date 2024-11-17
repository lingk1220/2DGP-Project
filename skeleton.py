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

class Skeleton:
    image = None
    def __init__(self, x, y):
        self.width_image = 640
        self.height_image = 448

        self.count_h = 10
        self.count_v = 7

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.center_error_x = 0
        self.pos_x = x
        self.pos_y = y + 38
        self.dir = 1

        self.index_h = 0
        self.index_v = 3 - 1
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 140
        self.draw_y = 140 * self.size_v / (self.size_h - self.center_error_x)
        self.min_chicken_dir = 10000
        self.state = Walk
        self.chicken_target = None
        self.bool_shooting = 0
        self.bool_attacking = 0
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y


        if Skeleton.image == None:
            Skeleton.image = load_image('./enemy/skeleton.png')

        self.build_behavior_tree()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def get_bb(self):
        return self.pos_x - self.draw_x / 3, self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x / 3, self.pos_y + self.draw_y / 3.5



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
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y
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

    def set_center_location(self):
        self.tx, self.ty = 0, self.pos_y
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

    def is_attacking(self):
        if self.bool_attacking == 1:
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

    def attack_ally(self):
        self.bool_attacking = 1
        self.state = Attack
        self.dir = 0 - self.pos_x
        if self.index_h < 6:
            return BehaviorTree.RUNNING
        if self.index_h >= 6:
            self.bool_attacking = 0
            self.dir = self.dir / abs(self.dir)
            print('ATTACK!')
            return BehaviorTree.SUCCESS


    def build_behavior_tree(self):
        a0 = Action('Wait', self.wait_time)
        ACT_set_wait_time = Action('Set Wait Time', self.set_wait_time)
        ACT_set_reload_time = Action('Set Wait Time', self.set_wait_time, 30, 30)
        SEQ_wait_time = Sequence('Wait', ACT_set_wait_time, a0)
        SEQ_wait_reload = Sequence('Wait Reload', ACT_set_reload_time, a0)
        a1 = Action('Move to', self.move_to)

        ACT_set_center = Action('Set Center Location', self.set_center_location)
        root = SEL_approach_center = Sequence('approach to center', ACT_set_center, a1)




        CDT_target_nearby = Condition('사거리 안에 공격대상이 있는가?', self.is_target_nearby, 100)
        CDT_is_attacking = Condition('공격을 하고 있는가?', self.is_attacking)
        ACT_attack = Action('공격', self.attack_ally)
        SEL_in_attack_state = Selector('공격 상태인가?', CDT_is_attacking, CDT_target_nearby)

        SEL_attack = Selector('공격', CDT_target_nearby, )

        root = SEQ_attack_ally = Sequence('아군을 공격', SEL_in_attack_state, ACT_attack)

        SEQ_attack_and_wait = Sequence('공격 및 대기', SEQ_attack_ally, SEQ_wait_reload)


        root = SEL_attack_approach = Selector('공격 또는 approach', SEQ_attack_and_wait, SEL_approach_center)

        self.bt = BehaviorTree(root)





class Idle:
    @staticmethod
    def enter(archer, e):
        archer.idle_start_time = get_time()
        archer.index_v = 4 - 1
        archer.index_h = 0

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):
        archer.index_h = (archer.index_h + 10 * 1.5 * game_framework.frame_time) % 10


    @staticmethod
    def draw(archer):
        if archer.dir < 0:
            archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.clip_pos_x,
                                   archer.clip_pos_y, archer.draw_x, archer.draw_y)
        else:
            archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.clip_pos_x,
                                             archer.clip_pos_y, archer.draw_x, archer.draw_y)

class Walk:
    @staticmethod
    def enter(archer, e):
        archer.index_v = 7 - 1
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
        if archer.dir < 0:
            archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.clip_pos_x,
                                   archer.clip_pos_y, archer.draw_x, archer.draw_y)
        else:
            archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.clip_pos_x,
                                             archer.clip_pos_y, archer.draw_x, archer.draw_y)



class Attack:
    @staticmethod
    def enter(archer, e):
        archer.index_v = 3 - 1
        archer.index_h = 0

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):
        archer.index_h = (archer.index_h + 6 * 1.5 * game_framework.frame_time) % 6

    @staticmethod
    def draw(archer):
        if archer.dir < 0:
            archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.clip_pos_x,
                                   archer.clip_pos_y, archer.draw_x, archer.draw_y)
        else:
            archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.clip_pos_x,
                                             archer.clip_pos_y, archer.draw_x, archer.draw_y)
