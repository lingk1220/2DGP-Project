import random
import game_framework

from pico2d import *

from state_machine import StateMachine, right_down, right_up, left_down, left_up, lshift_down, lshift_up

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
#FRAMES_PER_ACTION = 8

class Character:

    image = None
    def __init__(self, x, y):
        self.width_image = 3626
        self.height_image = 594

        self.pos_x = x
        self.pos_y = y + 3

        self.speed_walk = 3
        self.speed_run = 7
        self.frame = 0
        self.need_update_frame = 0

        self.dir = 0
        self.run = 0

        self.flip_h = ''

        self.count_h = 37
        self.count_v = 9

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = 0
        self.index_v = 8
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Character.image == None:
            Character.image = load_image('JoannaD\'ArcIII-Sheet#1.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)


        self.state_machine.set_transitions(
            {

                Idle : {right_down : Walk, right_up : Walk, left_down : Walk, left_up : Walk, lshift_down: Idleshift},
                Idleshift: {right_down: Run, right_up: Run, left_down: Run, left_up: Run, lshift_up: Idle},

                Walk: {right_down: Idle, right_up: Idle, left_down: Idle, left_up: Idle, lshift_down: Run},
                Run: {right_down: Idleshift, right_up: Idleshift, left_down: Idleshift, left_up: Idleshift, lshift_up: Walk},
                #Sleep: { space_down : Idle, right_down : Run, right_up : Idle, left_down : Run, left_up : Idle,},

            }
        )


    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
        pass


    def draw(self):
        self.state_machine.draw()


class Idle:
    @staticmethod
    def enter(character, e):
        if not lshift_up(e):
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
        character.image.clip_composite_draw(int(character.index_h) * character.size_h,
                                  character.index_v * character.size_v,
                                  character.size_h,
                                  character.size_v,
                                  0,
                                  character.flip_h,
                                  character.pos_x, character.pos_y, character.size_h * 2, character.size_v * 2)

class Idleshift:
    @staticmethod
    def enter(character, e):
        if not lshift_down(e):
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
        character.image.clip_composite_draw(int(character.index_h)  * character.size_h,
                                  character.index_v * character.size_v,
                                  character.size_h,
                                  character.size_v,
                                  0,
                                  character.flip_h,
                                  character.pos_x, character.pos_y, character.size_h * 2, character.size_v * 2)


class Walk:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.dir = 1
            character.flip_h = ''
        elif left_down(e) or right_up(e):
            character.dir = -1
            character.flip_h = 'h'

        character.index_v = 8 - 1
        character.index_h = 0
        print('Character Walk Enter')

    @staticmethod
    def exit(character, e):
        print('Character Walk Exit')

    @staticmethod
    def do(character):

        character.index_h = (character.index_h + 18 * 1 * game_framework.frame_time)
        if character.index_h >= 20:
            character.index_h = 2


        character.pos_x += character.dir * character.speed_walk

    @staticmethod
    def draw(character):

        character.image.clip_composite_draw(int(character.index_h) * character.size_h,
                                  character.index_v * character.size_v,
                                  character.size_h,
                                  character.size_v,
                                  0,
                                  character.flip_h,
                                  character.pos_x, character.pos_y, character.size_h * 2, character.size_v * 2)


class Run:
    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.dir = 1
            character.flip_h = ''
        elif left_down(e) or right_up(e):
            character.dir = -1
            character.flip_h = 'h'

        character.index_v = 7 - 1
        character.index_h = 0
        print('Character Run Enter')

    @staticmethod
    def exit(character, e):
        print('Character Run Exit')

    @staticmethod
    def do(character):
        character.index_h = (character.index_h + 7 * 2 * game_framework.frame_time)
        if character.index_h >= 9:
            character.index_h = 2

        character.pos_x += character.dir * character.speed_run

    @staticmethod
    def draw(character):
        character.image.clip_composite_draw(int(character.index_h) * character.size_h,
                                  character.index_v * character.size_v,
                                  character.size_h,
                                  character.size_v,
                                  0,
                                  character.flip_h,
                                  character.pos_x, character.pos_y, character.size_h * 2, character.size_v * 2)
