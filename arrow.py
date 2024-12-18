import math
import random
import time

import game_framework


from pico2d import load_image, get_time, draw_rectangle

import game_world
import play_mode
from state_machine import StateMachine

class Arrow:
    image = None
    def __init__(self, x, y):
        self.width_image = 30
        self.height_image = 5

        self.count_h = 1
        self.count_v = 1

        self.life_time = 3
        self.shooted_time = time.time()
        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.parent = None
        self.center_error_x = 0
        self.pos_x = x
        self.pos_y = y - 33
        self.index_h = 0
        self.index_v = 0
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = self.size_h * 1.5
        self.draw_y = self.size_v * 1.5

        self.removed = 0

        self.tag = 'arrow'
        self.dir = 1
        #self.state = Idle
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        if Arrow.image == None:
            Arrow.image = load_image('arrow.png')

        play_mode.game_world.add_collision_pair('arrow:chicken', self, None)
        play_mode.game_world.add_collision_pair('arrow:enemy', self, None)


    def get_bb(self):
        return self.pos_x - self.draw_x / 2, self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x / 2, self.pos_y + self.draw_y / 2

    def handle_collision(self, group, other):
        if group == 'arrow:chicken':
            if not self.removed:
                self.parent.set_target_chicken_none()
                self.removed = 1
                play_mode.game_world.remove_object(self)

        if group == 'arrow:enemy':
            if not self.removed:
                if not other.is_dying:
                    self.removed = 1
                    play_mode.game_world.remove_object(self)

    def update(self):
        self.pos_x += self.dir * 300 * game_framework.frame_time
        if time.time() - self.shooted_time > self.life_time:
            play_mode.game_world.remove_object(self)
        pass

    def handle_event(self, event):
        pass

    def set_target_enemy_none(self):
        self.parent.set_target_enemy_none()

    def draw(self):
        if abs(play_mode.character.pos_x - self.pos_x) > 1000:
            return
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        if self.dir < 0:
            self.image.clip_composite_draw(0,
                                           0,
                                           self.size_h,
                                           self.size_v,
                                           0,
                                           'h',
                                           self.clip_pos_x,
                                           self.clip_pos_y,
                                           self.size_h * 1.5, self.size_v * 1.5
                                           )
        else:
            self.image.clip_composite_draw(0,
                                           0,
                                           self.size_h,
                                           self.size_v,
                                           0,
                                           '',
                                           self.clip_pos_x,
                                           self.clip_pos_y,
                                           self.size_h * 1.5, self.size_v * 1.5
                                           )
