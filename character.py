import random

from pico2d import *

from state_machine import StateMachine
#from main import width, height

width = 1400
height = 800

class Character:
    global width, height
    image = None
    def __init__(self, x, y):
        self.width_image = 3626
        self.height_image = 594

        self.frame = 0

        self.dir = 0
        self.run = 0

        self.count_h = 37
        self.count_v = 9

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = x
        self.index_v = y
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Character.image == None:
            Character.image = load_image('JoannaD\'ArcIII-Sheet#1.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir += 1
            elif event.key == SDLK_LEFT:
                self.dir -= 1
            elif event.key == SDLK_LSHIFT:
                self.run = 1
            elif event.key == SDLK_ESCAPE:
                running = False


        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.dir -= 1
            elif event.key == SDLK_LEFT:
                self.dir += 1
            elif event.key == SDLK_LSHIFT:
                self.run = 0

        if self.dir == 0 and self.state_machine.cur_state != Idle:
            self.state_machine.start(Idle)

        elif self.dir != 0:
            if self.run == 0 and self.state_machine.cur_state != Walk:
                self.state_machine.start(Walk)
            elif self.run == 1 and self.state_machine.cur_state != Run:
                self.state_machine.start(Run)

        pass


    def draw(self):
        self.image.clip_draw(self.index_h * self.size_h,
                             self.index_v * self.size_v,
                             self.size_h,
                             self.size_v,
                             width // 2 + 64,
                             height // 2 + 64, self.size_h, self.size_v)


class Idle:
    @staticmethod
    def enter(character):
        character.index_v = 9 - 1
        character.index_h = 0
        print('Character Idle Enter')

    @staticmethod
    def exit(character):
        print('Character Idle Exit')

    @staticmethod
    def do(character):
        character.index_h = (character.index_h + 1) % 6

    @staticmethod
    def draw(character):
        character.image.clip_draw(character.index_h * character.size_h,
                                  character.index_v * character.size_v,
                                  character.size_h,
                                  character.size_v,
                                  width // 2 + 64,
                                  height // 2 + 64, character.size_h * 2, character.size_v * 2)


class Walk:
    @staticmethod
    def enter(character):
        character.index_v = 8 - 1
        character.index_h = 1
        print('Character Walk Enter')

    @staticmethod
    def exit(character):
        print('Character Walk Exit')

    @staticmethod
    def do(character):
        character.index_h = character.index_h + 1
        if character.index_h >= 20:
            character.index_h = 2

    @staticmethod
    def draw(character):
        character.image.clip_draw(character.frame * character.size_h,
                                  character.index_v * character.size_v,
                                  character.size_h,
                                  character.size_v,
                                  width // 2 + 64,
                                  height // 2 + 64, character.size_h * 4, character.size_v * 4)


class Run:
    @staticmethod
    def enter(character):
        character.index_v = 7 - 1
        character.index_h = 0
        print('Character Run Enter')

    @staticmethod
    def exit(character):
        print('Character Run Exit')

    @staticmethod
    def do(character):
        character.index_h = (character.index_h + 1) % 6

    @staticmethod
    def draw(character):
        character.image.clip_draw(character.index_h * character.size_h,
                                  character.index_v * character.size_v,
                                  character.size_h,
                                  character.size_v,
                                  width // 2 + 64,
                                  height // 2 + 64, character.size_h * 2, character.size_v * 2)
