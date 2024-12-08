import math
import random
import time
from random import randint

import game_framework


from pico2d import load_image, get_time, draw_rectangle

import game_world
import play_mode
from chicken import Chicken
from skeleton import Skeleton
from wanderer import Wanderer
from state_machine import StateMachine
from zombie import Zombie


class Obelisk2:
    image = None
    def __init__(self,map, dir, x, y, difficulty):
        self.width_image = 2600
        self.height_image = 400

        self.enemy_factors = [1, 3, 3]
        self.map = map
        self.difficulty = difficulty

        self.count_h = 13
        self.count_v = 1

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.ground = y
        self.center_error_x = 0
        self.pos_x = x * map.tile_size * (dir * 2 - 1)
        self.pos_y = y + 175

        self.frame = 0

        self.index_h = 1 - 1
        self.index_v = 1 - 1

        self.draw_x = self.size_h
        self.draw_y = self.size_v

        self.is_dying = 0

        self.hp = 20
        self.clip_pos_x = 0
        self.clip_pos_y = 0

        self.enemy_count = 0
        self.enemy_count_max = 5 + (self.difficulty ** 5) * 50

        self.dir = self.pos_x / abs(self.pos_x)

        self.spawn_timer = 0
        self.spawn_delay = 1.0

        self.mt = 1000
        self.t = self.mt

        #self.state = Idle
        if Obelisk2.image == None:
            Obelisk2.image = load_image('obelisk2.png')

        self.state = Idle
        self.state_machine = StateMachine(self)
        self.state_machine.start(self.state)

        play_mode.game_world.add_collision_pair('arrow:enemy', None, self)

    def get_bb(self):
        return self.pos_x - self.draw_x / 3.3, self.pos_y - self.draw_y / 2 - 5, self.pos_x + self.draw_x / 3.3, self.pos_y + self.draw_y / 3 + 7



    def destroy(self):
        self.state = Die

    def attacked(self, other):
        self.hp -= 1
        if self.hp <= 0:
            self.is_dying = 1
            self.state = Die
            other.set_target_enemy_none()


    def handle_collision(self, group, other):
        if group == 'arrow:enemy':
            self.attacked(other)
        pass

    def update(self):
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



class Idle:
    @staticmethod
    def enter(obelisk, e):
        obelisk.idle_start_time = get_time()

        obelisk.index_v = 0
        obelisk.index_h = 0

    @staticmethod
    def exit(obelisk, e):
        pass

    @staticmethod
    def do(obelisk):
        obelisk.frame = (obelisk.frame + 13 * 0.5 * game_framework.frame_time) % 13


        if game_world.is_day == True:
            return

        obelisk.spawn_timer = obelisk.spawn_timer + game_framework.frame_time

        if obelisk.enemy_count >= obelisk.enemy_count_max:
           return
        if obelisk.spawn_timer > obelisk.spawn_delay:
            new_enemy = None
            factor = randint(1, 3)
            cost = min( randint(1, 3), obelisk.enemy_count_max -obelisk.enemy_count)
            if factor == 1:
                new_enemy = Zombie(obelisk.pos_x, obelisk.ground, obelisk, cost)
            elif factor == 2:
                new_enemy = Skeleton(obelisk.pos_x, obelisk.ground, obelisk, cost)
            elif factor == 3:
                new_enemy = Skeleton(obelisk.pos_x, obelisk.ground, obelisk, cost)

            play_mode.game_world.add_object(new_enemy, 3)
            obelisk.spawn_timer = 0
            obelisk.enemy_count += factor
        pass

    @staticmethod
    def draw(obelisk):
        if obelisk.dir < 0:
            obelisk.clip_pos_x = 700 - play_mode.character.pos_x + obelisk.pos_x
            obelisk.clip_pos_y = obelisk.pos_y
            Obelisk2.image.clip_composite_draw(int(obelisk.frame) * obelisk.size_h,
                                              25,
                                              obelisk.size_h,
                                              obelisk.size_v,
                                              0,
                                              '',
                                              obelisk.clip_pos_x,
                                              obelisk.clip_pos_y,
                                              obelisk.size_h, obelisk.size_v - 25
                                              )
        else:
            obelisk.clip_pos_x = 700 - play_mode.character.pos_x + obelisk.pos_x
            obelisk.clip_pos_y = obelisk.pos_y
            Obelisk2.image.clip_composite_draw(int(obelisk.frame) * obelisk.size_h,
                                              25,
                                              obelisk.size_h,
                                              obelisk.size_v,
                                              0,
                                              'h',
                                              obelisk.clip_pos_x,
                                              obelisk.clip_pos_y,
                                              obelisk.size_h, obelisk.size_v - 25
                                              )



class Die:
    @staticmethod
    def enter(obelisk, e):
        obelisk.index_v = 0
        obelisk.index_h = 0

    @staticmethod
    def exit(obelisk, e):
        pass

    @staticmethod
    def do(obelisk):
        obelisk.frame = 0
        obelisk.t -= 200 * game_framework.frame_time
        if obelisk.t <= 0:
            obelisk.map.reset_enemy_building(obelisk.dir)


    @staticmethod
    def draw(obelisk):
        if obelisk.dir < 0:
            Obelisk2.image.clip_draw(0,
                                   20 + int(obelisk.size_v  * (1 - obelisk.t/ obelisk.mt)),
                                   obelisk.size_h,
                                   obelisk.size_v,
                                   obelisk.clip_pos_x + obelisk.center_error_x // 2 + (randint(0, 1)*2-1) * randint(1, 3) * 0.4,
                                   obelisk.clip_pos_y + int(obelisk.draw_y  * (obelisk.t/ obelisk.mt - 1)) // 2 -5, obelisk.draw_x + obelisk.center_error_x,  int(obelisk.draw_y  * (obelisk.t/ obelisk.mt)))
        else:
            Obelisk2.image.clip_composite_draw(0,
                                   20 + int(obelisk.size_v  * (1 - obelisk.t/ obelisk.mt)),
                                   obelisk.size_h,
                                   obelisk.size_v,
                                   0,
                                   'h',
                                   obelisk.clip_pos_x + obelisk.center_error_x // 2 + (randint(0, 1)*2-1) * randint(1, 3) * 0.4,
                                   obelisk.clip_pos_y + int(obelisk.draw_y  * (obelisk.t/ obelisk.mt - 1)) // 2 - 5, obelisk.draw_x + obelisk.center_error_x,  int(obelisk.draw_y  * (obelisk.t/ obelisk.mt)))
