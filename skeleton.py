import math
import random
import time

import game_framework
import game_world

import play_mode

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import load_image, get_time

from character import Character
from chicken import Chicken
from maid import Maid
from state_machine import StateMachine

from arrow import Arrow

allys = ['Archer', 'Maid', 'Character']

class Skeleton:
    image = None
    def __init__(self, x, y, parent, cost = 1):
        self.width_image = 640
        self.height_image = 448

        self.count_h = 10
        self.count_v = 7

        self.cost = 0.75 + cost / 4
        self.hp = cost

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.center_error_x = 0
        self.pos_x = x
        self.pos_y = y + 38
        self.dir = 1

        self.can_attack = 0

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
        self.bool_attack = 0
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y
        self.is_dying = 0

        self.tag = 'Enemy'

        if Skeleton.image == None:
            Skeleton.image = load_image('./enemy/skeleton.png')

        play_mode.game_world.add_collision_pair('enemy:ally', self, None)
        play_mode.game_world.add_collision_pair('arrow:enemy', None, self)

        self.build_behavior_tree()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def get_bb(self):
        if self.bool_attacking:
            return self.pos_x - self.draw_x / 4 + self.draw_x * self.dir / 4, self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x / 4  + self.draw_x * self.dir / 4, self.pos_y + self.draw_y / 4
        else:
            return self.pos_x - self.draw_x / 4, self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x / 4, self.pos_y + self.draw_y / 4

    def handle_collision(self, group, other):
        if group == 'enemy:ally':

            if not other.is_dying:
                if self.bool_attack:
                    other.attacked(self)
                    self.bool_attack = 0

                if not other.is_dying and self.bool_attacking == 0:
                    self.can_attack = 1


        if group == 'arrow:enemy':
            self.attacked(other)


    def update(self):
        if not self.is_dying:
            self.bt.run()

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


    def attacked(self, other):
        self.hp -= 1
        if self.hp <= 0:
            self.is_dying = 1
            self.state = Die
            other.set_target_enemy_none()


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
        if tx == self.pos_x:
            return
        self.dir = (tx - self.pos_x) / abs(tx - self.pos_x)
        self.speed = 100 * self.cost
        self.pos_x += self.speed * self.dir * game_framework.frame_time

    def move_to(self, r=10):
        self.state = Walk
        self.move_slightly_to(self.tx)
        if self.distance_less_than(self.tx, self.pos_x, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx, self.ty = self.pos_x + ((2 * random.randint(0, 1)  - 1) *  random.randint(100, 101)), self.pos_y

        # self.tx, self.ty = 1000, 100
        return BehaviorTree.SUCCESS

    def set_center_location(self):
        self.tx, self.ty = 0, self.pos_y
        # self.tx, self.ty = 1000, 100
        return BehaviorTree.SUCCESS


    def wait_time(self):
        self.state = Idle
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




    # def is_target_nearby(self, distance):
    #     for ally in game_world.objects[3]:
    #         if ally.__class__ in allys :
    #             if self.distance_less_than(ally.pos_x, self.pos_x, distance):
    #                 return BehaviorTree.SUCCESS
    #             else:
    #                 return BehaviorTree.FAIL
    #         return BehaviorTree.FAIL

    def is_target_nearby(self, distance):
        if self.can_attack:
            self.can_attack = 0

            self.bool_attacking = 1
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL




    def is_attacking(self):
        if self.bool_attacking == 1:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    def attack_ally(self):
        self.state = Attack
        self.dir = - self.pos_x / abs(self.pos_x)
        if self.index_h < 5:
            return BehaviorTree.RUNNING
        elif self.index_h >= 5 and self.state == Attack:
            self.bool_attacking = 0
            self.bool_attack = 1

            return BehaviorTree.SUCCESS


    def build_behavior_tree(self):
        a0 = Action('Wait', self.wait_time)
        ACT_set_wait_time = Action('Set Wait Time', self.set_wait_time)
        ACT_set_reload_time = Action('Set Wait Time', self.set_wait_time, 15, 15)
        SEQ_wait_time = Sequence('Wait', ACT_set_wait_time, a0)
        SEQ_wait_reload = Sequence('Wait Reload', ACT_set_reload_time, a0)
        a1 = Action('Move to', self.move_to)

        ACT_set_center = Action('Set Center Location', self.set_center_location)
        root = SEL_approach_center = Sequence('approach to center', ACT_set_center, a1)




        CDT_target_nearby = Condition('사거리 안에 공격대상이 있는가?', self.is_target_nearby, 100)
        CDT_is_attacking = Condition('공격을 하고 있는가?', self.is_attacking)
        ACT_attack = Action('공격', self.attack_ally)
        SEL_in_attack_state = Selector('공격 상태인가?', CDT_is_attacking, CDT_target_nearby)


        root = SEQ_attack_ally = Sequence('아군을 공격', SEL_in_attack_state, ACT_attack, SEQ_wait_reload)

        SEQ_attack_and_wait = Sequence('공격 및 대기', SEQ_attack_ally)


        root = SEL_attack_approach = Selector('공격 또는 approach', SEQ_attack_and_wait, SEL_approach_center)

        self.bt = BehaviorTree(root)





class Idle:
    @staticmethod
    def enter(skeleton, e):
        skeleton.idle_start_time = get_time()
        skeleton.index_v = 4 - 1
        skeleton.index_h = 0

    @staticmethod
    def exit(skeleton, e):
        pass

    @staticmethod
    def do(skeleton):
        skeleton.index_h = (skeleton.index_h + 10 * skeleton.cost * 1.5 * game_framework.frame_time) % 10


    @staticmethod
    def draw(skeleton):
        if skeleton.dir < 0:
            Skeleton.image.clip_draw(int(skeleton.index_h) * skeleton.size_h,
                                   skeleton.index_v * skeleton.size_v,
                                   skeleton.size_h - skeleton.center_error_x,
                                   skeleton.size_v,
                                   skeleton.clip_pos_x,
                                   skeleton.clip_pos_y, skeleton.draw_x, skeleton.draw_y)
        else:
            Skeleton.image.clip_composite_draw(int(skeleton.index_h) * skeleton.size_h,
                                             skeleton.index_v * skeleton.size_v,
                                             skeleton.size_h - skeleton.center_error_x,
                                             skeleton.size_v,
                                             0,
                                             'h',
                                             skeleton.clip_pos_x,
                                             skeleton.clip_pos_y, skeleton.draw_x, skeleton.draw_y)

class Walk:
    @staticmethod
    def enter(skeleton, e):
        skeleton.index_v = 7 - 1
        skeleton.index_h = 0

    @staticmethod
    def exit(skeleton, e):
        pass

    @staticmethod
    def do(skeleton):
        skeleton.index_h = (skeleton.index_h + 8 * skeleton.cost *  1.5 * game_framework.frame_time) % 8


    @staticmethod
    def draw(skeleton):
        if skeleton.dir < 0:
            Skeleton.image.clip_draw(int(skeleton.index_h) * skeleton.size_h,
                                   skeleton.index_v * skeleton.size_v,
                                   skeleton.size_h - skeleton.center_error_x,
                                   skeleton.size_v,
                                   skeleton.clip_pos_x,
                                   skeleton.clip_pos_y, skeleton.draw_x, skeleton.draw_y)
        else:
            Skeleton.image.clip_composite_draw(int(skeleton.index_h) * skeleton.size_h,
                                             skeleton.index_v * skeleton.size_v,
                                             skeleton.size_h - skeleton.center_error_x,
                                             skeleton.size_v,
                                             0,
                                             'h',
                                             skeleton.clip_pos_x,
                                             skeleton.clip_pos_y, skeleton.draw_x, skeleton.draw_y)



class Attack:
    @staticmethod
    def enter(skeleton, e):
        skeleton.index_v = 3 - 1
        skeleton.index_h = 0

    @staticmethod
    def exit(skeleton, e):
        pass

    @staticmethod
    def do(skeleton):
        skeleton.index_h = (skeleton.index_h + 6 * skeleton.cost * 1.5 * game_framework.frame_time) % 6

    @staticmethod
    def draw(skeleton):
        if skeleton.dir < 0:
            Skeleton.image.clip_draw(int(skeleton.index_h) * skeleton.size_h,
                                   skeleton.index_v * skeleton.size_v,
                                   skeleton.size_h - skeleton.center_error_x,
                                   skeleton.size_v,
                                   skeleton.clip_pos_x,
                                   skeleton.clip_pos_y, skeleton.draw_x, skeleton.draw_y)
        else:
            Skeleton.image.clip_composite_draw(int(skeleton.index_h) * skeleton.size_h,
                                             skeleton.index_v * skeleton.size_v,
                                             skeleton.size_h - skeleton.center_error_x,
                                             skeleton.size_v,
                                             0,
                                             'h',
                                             skeleton.clip_pos_x,
                                             skeleton.clip_pos_y, skeleton.draw_x, skeleton.draw_y)




class Die:
    @staticmethod
    def enter(skeleton, e):
        skeleton.index_v = 3 - 1
        skeleton.index_h = 7 - 1

    @staticmethod
    def exit(skeleton, e):
        pass

    @staticmethod
    def do(skeleton):
        if skeleton.index_h < 13:
            skeleton.index_h = skeleton.index_h + 13 * 1.5 * game_framework.frame_time
        else:
            skeleton.index_h = 13
            game_world.remove_object(skeleton)

    @staticmethod
    def draw(skeleton):
        if skeleton.dir < 0:
            Skeleton.image.clip_draw(int(skeleton.index_h % 13) * skeleton.size_h,
                                   (skeleton.index_v - int(skeleton.index_h / 13)) * skeleton.size_v,
                                   skeleton.size_h,
                                   skeleton.size_v,
                                   skeleton.clip_pos_x + skeleton.center_error_x // 2,
                                   skeleton.clip_pos_y, skeleton.draw_x + skeleton.center_error_x, skeleton.draw_y)
        else:
            Skeleton.image.clip_composite_draw(int(skeleton.index_h % 13) * skeleton.size_h,
                                               (skeleton.index_v - int(skeleton.index_h / 13)) * skeleton.size_v,
                                             skeleton.size_h,
                                             skeleton.size_v,
                                             0,
                                             'h',
                                             skeleton.clip_pos_x - skeleton.center_error_x // 2,
                                             skeleton.clip_pos_y, skeleton.draw_x + skeleton.center_error_x, skeleton.draw_y)


