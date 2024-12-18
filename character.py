import random
from types import NoneType

import end_game_mode
import game_framework

from pico2d import *

import game_world
import pause_mode
import play_mode
from state_machine import StateMachine, right_down, right_up, left_down, left_up, lshift_down, lshift_up, interact_down, \
    interact_up, run_shift, right_down_with_shift, left_down_with_shift, time_out_interact, right_up_with_shift, \
    left_up_with_shift, change_mode_play

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
#FRAMES_PER_ACTION = 8



class Character:

    image = None
    image_interaction = None
    def __init__(self, x, y):
        self.width_image = 3626
        self.height_image = 594

        self.width_image_interact = 4576
        self.height_image_interact = 2166

        self.pos_x = x
        self.pos_y = y

        self.speed_walk = 150
        self.speed_run = 350
        self.frame = 0
        self.need_update_frame = 0

        self.dir = 0
        self.run = 0
        self.shift_pressed = 0
        self.flip_h = ''

        self.count_h = 37
        self.count_v = 9

        self.interact_count_h = 16
        self.interact_count_v = 19

        self.ground = y
        self.clip_pos_x = 700
        self.clip_pos_y = y

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.interact_size_h = (self.width_image_interact // self.interact_count_h)
        self.interact_size_v = (self.height_image_interact // self.interact_count_v)

        self.nearest_interactor = None
        self.nearest_wanderer = None
        self.wanderer_dist_min = 10000

        self.interactor_dist_min = 10000


        self.index_h = 0
        self.index_v = 8
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = self.size_h * 2
        self.draw_y = self.size_v * 2

        self.is_dying = 0

        self.money = 40
        self.money_max = 100

        self.hp = 10
        self.hp_max = 10
        if Character.image == None:
            Character.image = load_image('character.png')
        if Character.image_interaction == None:
            Character.image_interaction = load_image('character_interact.png')

        play_mode.game_world.add_collision_pair('character:wanderer', self, None)
        play_mode.game_world.add_collision_pair('character:building', self, None)
        play_mode.game_world.add_collision_pair('enemy:ally', None, self)

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)


        self.state_machine.set_transitions(
            {

                Idle : {right_down_with_shift: Run, right_down : Walk , right_up_with_shift: Run, right_up : Walk, left_down_with_shift:Run, left_down : Walk, left_up_with_shift: Run, left_up : Walk, lshift_down: Idle, lshift_up: Idle, interact_down:Interact},
                Interact: {time_out_interact:Idle, right_down_with_shift: Run, right_down : Walk, left_down_with_shift: Run, left_down : Walk, lshift_down: Interact, lshift_up: Interact},
                Walk: {right_down: Idle, right_up: Idle, left_down: Idle, left_up: Idle, lshift_down: Run, run_shift:Run},
                Run: {right_down: Idle, right_up: Idle, left_down: Idle, left_up: Idle, lshift_up: Walk},

            }
        )

    def get_bb(self):
        return self.pos_x - self.draw_x / 4.3 + self.dir * 7 + 25, self.pos_y - self.draw_y / 4, self.pos_x + self.draw_x / 4.3 + self.dir * 7 - 25, self.pos_y + self.draw_y / 2.5

    def handle_collision(self, group, other):
        if group == 'character:wanderer':

            if self.wanderer_dist_min > self.pos_x - other.pos_x:
                self.nearest_wanderer = other
                self.wanderer_dist_min = self.pos_x - other.pos_x

            return
        if group == 'character:building':

            if other.__class__ == 'Wall':
                return
            if self.interactor_dist_min > self.pos_x - other.pos_x:
                self.nearest_interactor = other
                self.interactor_dist_min = self.pos_x - other.pos_x

            return

    def update(self):

        self.wanderer_dist_min = 10000
        self.state_machine.update()
        pass

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event, self.shift_pressed))
        pass

    def change_mode(self):
        self.state_machine.clear_event()

    def draw(self):
        self.state_machine.draw()

    def get_money(self, amount):
        self.money += amount
        if self.money > self.money_max:
            self.money = self.money_max

    def lose_money(self, amount):
        self.money -= amount
        if self.money < 0:
            self.money = 0

    def attacked(self, other):
        self.hp -= 1
        if self.hp <= 0:
            self.is_dying = 1
            game_framework.push_mode(end_game_mode)


class Idle:
    @staticmethod
    def enter(character, e):
        if lshift_down(e):
            character.shift_pressed = 1
        elif lshift_up(e):
            character.shift_pressed = 0
        else:
            character.index_v = 9 - 1
            character.index_h = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.index_h = (character.index_h + 6 * 1.5 * game_framework.frame_time) % 6

    @staticmethod
    def draw(character):
        Character.image.clip_composite_draw(int(character.index_h) * character.size_h,
                                  character.index_v * character.size_v,
                                  character.size_h,
                                  character.size_v,
                                  0,
                                  character.flip_h,
                                  character.clip_pos_x, character.clip_pos_y, character.size_h * 2, character.size_v * 2)



class Walk:
    @staticmethod
    def enter(character, e):
        if lshift_up(e):
            character.shift_pressed = 0

        elif right_down(e) or left_up(e):
            character.dir = 1
            character.flip_h = ''
        elif left_down(e) or right_up(e):
            character.dir = -1
            character.flip_h = 'h'

        character.index_v = 8 - 1
        character.index_h = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):

        character.index_h = (character.index_h + 18 * 1 * game_framework.frame_time)
        if character.index_h >= 20:
            character.index_h = 2


        if game_world.map.left_enemy_building.building.pos_x + 100 < character.pos_x + game_framework.frame_time * character.dir * character.speed_walk < game_world.map.right_enemy_building.building.pos_x - 100:
            character.pos_x = character.pos_x +game_framework.frame_time * character.dir * character.speed_walk

    @staticmethod
    def draw(character):

        Character.image.clip_composite_draw(int(character.index_h) * character.size_h,
                                  character.index_v * character.size_v,
                                  character.size_h,
                                  character.size_v,
                                  0,
                                  character.flip_h,
                                  character.clip_pos_x, character.clip_pos_y, character.size_h * 2, character.size_v * 2)


class Run:
    @staticmethod
    def enter(character, e):
        character.shift_pressed = 1
        if right_down(e) or right_down_with_shift(e) or left_up(e):
            character.dir = 1
            character.flip_h = ''
        elif left_down(e) or left_down_with_shift(e) or right_up(e):
            character.dir = -1
            character.flip_h = 'h'

        character.index_v = 7 - 1
        character.index_h = 0

    @staticmethod
    def exit(character, e):
        pass
    @staticmethod
    def do(character):
        character.index_h = (character.index_h + 7 * 2 * game_framework.frame_time)
        if character.index_h >= 9:
            character.index_h = 2

        if game_world.map.left_enemy_building.building.pos_x + 100 < character.pos_x + game_framework.frame_time * character.dir * character.speed_run < game_world.map.right_enemy_building.building.pos_x - 100:
            character.pos_x =   character.pos_x +game_framework.frame_time * character.dir * character.speed_run

    @staticmethod
    def draw(character):
        Character.image.clip_composite_draw(int(character.index_h) * character.size_h,
                                  character.index_v * character.size_v,
                                  character.size_h,
                                  character.size_v,
                                  0,
                                  character.flip_h,
                                  character.clip_pos_x, character.clip_pos_y, character.size_h * 2, character.size_v * 2)


class Interact:
    @staticmethod
    def enter(character, e):
        if lshift_down(e):
            character.shift_pressed = 1
        elif lshift_up(e):
            character.shift_pressed = 0
        elif interact_down(e):
            character.index_v = 10 - 1
            character.index_h = 0

    @staticmethod
    def exit(character, e):
        pass
    @staticmethod
    def do(character):
        character.index_h = (character.index_h + 22 * 0.8 * game_framework.frame_time)


        if character.index_v == 10 - 1 and character.index_h >= 6:
            character.index_v = 9 - 1
            character.index_h = 0
        elif character.index_v == 9 - 1 and character.index_h >= 7:
            character.index_v = 8 - 1
            character.index_h = 0
        elif character.index_v == 8 - 1 and character.index_h >= 9:
            character.state_machine.add_event(('TIME_OUT', 0))

            if character.nearest_wanderer is not None:
                character.nearest_wanderer.interact()
            elif character.nearest_interactor is not None:
                character.nearest_interactor.interact()



            character.index_v = 10 - 1
            character.index_h = 0
        character.nearest_interactor = None
        character.nearest_wanderer = None


    @staticmethod
    def draw(character):
        Character.image_interaction.clip_composite_draw(int(character.index_h) * character.interact_size_h,
                                  character.index_v * character.interact_size_v,
                                  character.interact_size_h - 155,
                                  character.interact_size_v,
                                  0,
                                  character.flip_h,
                                  character.clip_pos_x, character.clip_pos_y + 30, (character.interact_size_h-155) * 2, character.interact_size_v * 2)