import random
import game_framework

from pico2d import load_image

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


        self.pos_x = x
        self.pos_y = y
        self.index_h = 0
        self.index_v = 0
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Archer.image == None:
            Archer.image = load_image('Archer.png')

        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)


        self.state_machine.set_transitions(
            {

            }
        )

    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        pass


    def draw(self):
        self.state_machine.draw()


class Idle:
    @staticmethod
    def enter(character, e):
        character.index_v = 5 - 1
        character.index_h = 0

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.index_h = (character.index_h + 5 * 1.5 * game_framework.frame_time) % 5

    @staticmethod
    def draw(archer):
        archer.image.clip_draw(int(archer.index_h) * archer.size_h,
                             archer.index_v * archer.size_v,
                             archer.size_h,
                             archer.size_v,
                             archer.pos_x,
                             archer.pos_y + 26, 110, 110)