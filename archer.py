import math
import random
import time
from random import randint
from zipfile import BZIP2_VERSION

import game_framework
import game_world

import play_mode

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pico2d import load_image, get_time

from chicken import Chicken
from state_machine import StateMachine

from arrow import Arrow

enemys = ['Skeleton', 'Zombie']


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
        self.pos_y = y + 25
        self.dir = 1
        self.bool_shooting = 0
        self.bool_is_at_home = False
        self.is_dying = 0

        self.hp = 3

        self.index_h = 0
        self.index_v = 3 - 1
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 100
        self.draw_y = 100 * self.size_v / (self.size_h - self.center_error_x)
        self.min_chicken_dir = 10000
        self.state = Walk
        self.chicken_target = None
        self.enemy_target = None
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        self.tag = 'Ally'

        if Archer.image == None:
            Archer.image = load_image('Archer.png')

        play_mode.game_world.add_collision_pair('enemy:ally', None, self)

        self.build_behavior_tree()
        self.bt = self.bt_day
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def get_bb(self):
        return self.pos_x - self.draw_x / 3, self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x / 3, self.pos_y + self.draw_y / 3.5

    def handle_collision(self, group, other):
        if group == 'enemy:ally':

            pass



    def update(self):
        if game_world.is_day:
            self.bt = self.bt_day
        else:
            self.bt = self.bt_night

        if not self.is_dying:
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

    def is_day(self):
        if play_mode.game_world.is_day:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_night(self):
        if not play_mode.game_world.is_day:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    def attacked(self, other):
        self.hp -= 1
        if self.hp <= 0:
            self.is_dying = 1
            self.state = Die
        #play_mode.game_world.remove_object(self)

    def set_target_chicken_none(self):
        self.chicken_target = None

    def set_target_enemy_none(self):
        self.enemy_target = None

    def set_target_location(self, x=None):

        self.tx, self.ty = x, self.pos_y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, x2, r):
        distance2 = abs(x2 - x1)
        return distance2 < 1 * r

    def distance_get(self, x1, x2):
        distance2 = x2 - x1
        return distance2

    def move_slightly_to(self, tx):
        if tx != self.pos_x:
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
                chicken_dir = abs(self.distance_get(chicken.pos_x, self.pos_x))
                if chicken_dir < distance:
                    if chicken_dir < self.min_chicken_dir:
                        self.chicken_target = chicken
        if self.chicken_target == None:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def lockon_enemy(self, distance):
        self.min_enemy_dir = 10000000
        self.enemy_target = None
        for enemy in game_world.objects[3]:
            if enemy.tag == 'Enemy':
                enemy_dir = abs(self.distance_get(enemy.pos_x, self.pos_x))
                if enemy_dir < distance:
                    if enemy_dir < self.min_chicken_dir:
                        self.enemy_target = enemy
        if self.enemy_target == None:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS


    def is_chicken_nearby(self, distance):
        if self.chicken_target == None:
            return BehaviorTree.FAIL

        if self.distance_less_than(self.chicken_target.pos_x, self.pos_x, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def is_enemy_nearby(self, distance):
        if self.enemy_target == None:
            return BehaviorTree.FAIL

        if self.distance_less_than(self.enemy_target.pos_x, self.pos_x, distance):
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

        if self.chicken_target.pos_x == None:
            return BehaviorTree.SUCCESS
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


    def shoot_to_enemy(self):
        if self.enemy_target == None:
            return BehaviorTree.FAIL
        if self.enemy_target.pos_x == None:
            return BehaviorTree.SUCCESS
        self.bool_shooting = 1
        self.state = Shoot
        self.dir = self.enemy_target.pos_x - self.pos_x
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

    def a(self):
        print('db')

    def set_home(self):
        d = randint(0, 1)
        # if self.pos_x > 0:
        #     d = 1
        # else:
        #     d = 0

        for i in range(0, game_world.map.map_size):
            if game_world.map.walls[d][i] is None:
                if i == 0:
                    self.tx = 0 + (randint(0, 1) * 2 - 1) * randint(0, 30)
                else:
                    self.tx = game_world.map.walls[d][i - 1].pos_x - (d * 2 - 1) * randint(30, 120)
                print(f'eb: {self.tx}')
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def is_at_home(self):
        if self.bool_is_at_home:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def get_home(self):
        self.bool_is_at_home = True
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

        c1 = Condition('토끼가 근처에 있는가?', self.is_chicken_nearby, 700)
        CDT_is_shooting = Condition('화살을 발사하고 있는가', self.is_shooting)

        a3 = Action('접근', self.move_to_chicken)
        root = SEQ_chase_chicken = Sequence('토끼를 추적', c1, a3)

        c2  = Condition('토끼가 사정거리 안에 있는가?', self.is_chicken_nearby, 500)
        SEL_in_shoot_state = Selector('발사상태인가', CDT_is_shooting, c2)
        a4 = Action('화살 발사', self.shoot_to_chicken)
        root = SEQ_shoot_chicken = Sequence('토끼를 사냥', SEL_in_shoot_state, a4)


        a5 = Action('시야거리 내에 토끼가 있는가?', self.lockon_chicken, 700)
        #SEQ_lockon_chicken = Sequence('LockOn', c3, a5)
        SEQ_shoot_and_wait = Sequence('화살 발사 및 대기', SEQ_shoot_chicken, SEQ_wait_reload)
        SEL_hunt_chicken = Selector('사냥', SEQ_shoot_and_wait, SEQ_chase_chicken, a5 )


        root = SEL_hunt_or_wander = Selector('사냥 또는 wander', SEL_hunt_chicken, SEQ_wander)



        self.bt_day = BehaviorTree(root)


        ACT_set_home = Action('귀환 위치 설정', self.set_home)
        ACT_get_home = Action('귀환 완료', self.get_home)
        ACT_go_home = Action('Move to', self.move_to)

        SEQ_go_home = Sequence('기지로 이동', ACT_set_home, ACT_go_home, ACT_get_home)

        CDT_is_enemy_nearby = Condition('적이 근처에 있는가?', self.is_enemy_nearby, 700)


        SEL_in_shoot_state = Selector('발사상태인가', CDT_is_shooting, CDT_is_enemy_nearby)
        ACT_shoot_enemy = Action('화살 발사', self.shoot_to_enemy)
        root = SEQ_shoot_enemy = Sequence('적을 사냥', SEL_in_shoot_state, ACT_shoot_enemy)


        ACT_lockon_enemy = Action('시야거리 내에 적이 있는가?', self.lockon_enemy, 700)
        #SEQ_lockon_chicken = Sequence('LockOn', c3, a5)
        SEQ_shoot_and_wait = Sequence('화살 발사 및 대기', SEQ_shoot_enemy, SEQ_wait_reload)
        SEL_hunt_enemy = Selector('사냥', SEQ_shoot_and_wait, ACT_lockon_enemy )
        root = SEL_hunt_or_wait = Selector('사냥 또는 wait', SEL_hunt_enemy, SEQ_wait_time)

        CDT_is_at_home = Condition('집에있', self.is_at_home)
        SEL_go_home = Selector('집에있는가', CDT_is_at_home, SEQ_go_home)

        SEQ_defend = Sequence('방어', SEL_hunt_or_wait)

        root = SEL_go_home_and_defend = Sequence('귀환 또는 방어', SEL_go_home, SEQ_defend)






        self.bt_night = BehaviorTree(root)





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
            Archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.clip_pos_x,
                                   archer.clip_pos_y, archer.draw_x, archer.draw_y)
        else:
            Archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
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
            Archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.clip_pos_x,
                                   archer.clip_pos_y, archer.draw_x, archer.draw_y)
        else:
            Archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.clip_pos_x,
                                             archer.clip_pos_y, archer.draw_x, archer.draw_y)

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
            Archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h - archer.center_error_x,
                                   archer.size_v,
                                   archer.clip_pos_x,
                                   archer.clip_pos_y, archer.draw_x, archer.draw_y)
        else:
            Archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h - archer.center_error_x,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.clip_pos_x,
                                             archer.clip_pos_y, archer.draw_x, archer.draw_y)


class Die:
    @staticmethod
    def enter(archer, e):
        archer.index_v = 1 - 1
        archer.index_h = 0

    @staticmethod
    def exit(archer, e):
        pass

    @staticmethod
    def do(archer):
        if archer.index_h < 5:
            archer.index_h = archer.index_h + 6 * 1.5 * game_framework.frame_time
        else:
            archer.index_h = 5

    @staticmethod
    def draw(archer):
        if archer.dir > 0:
            Archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                                   archer.index_v * archer.size_v,
                                   archer.size_h,
                                   archer.size_v,
                                   archer.clip_pos_x + archer.center_error_x // 2,
                                   archer.clip_pos_y, archer.draw_x + archer.center_error_x, archer.draw_y)
        else:
            Archer.image.clip_composite_draw(int(archer.index_h) * archer.size_h,
                                             archer.index_v * archer.size_v,
                                             archer.size_h,
                                             archer.size_v,
                                             0,
                                             'h',
                                             archer.clip_pos_x - archer.center_error_x // 2,
                                             archer.clip_pos_y, archer.draw_x + archer.center_error_x, archer.draw_y)

