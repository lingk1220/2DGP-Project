import random

from pico2d import load_image, get_time

import game_framework
from state_machine import StateMachine

image_counts = [[1, 1, 1, 1], [0, 0, 0, 0]]
wanderer_names = ['man', 'woman']
part_names = ['skin', 'pants', 'shirts', 'boots']

class Wanderer:
    image_wanderer = None
    image_skin = None
    image_pants = None
    image_boots = None
    image_shirts = None


    def load_image(self):
        if self.image_wanderer == None:
            self.image_wanderer = {}
            for wanderer_index in range(2):
                self.image_wanderer[wanderer_index] ={}
                wanderer_name = wanderer_names[wanderer_index]
                for part_index in range (4):
                    part_name = part_names[part_index]
                    self.image_wanderer[wanderer_index][part_index] = {}
                    for part_image_index in range(0, image_counts[wanderer_index][part_index]):
                        print("./wanderer/" + wanderer_name + "/" + part_name + "/" + part_name + "%d" % (part_image_index+1) + ".png")
                        self.image_wanderer[wanderer_index][part_index][part_image_index] = load_image("./wanderer/"+ wanderer_name + "/" + part_name + "/" + part_name + "%d" %(part_image_index+1) + ".png")


        print(f'enq: {self.image_wanderer[0][0][0]}')
        # if Wanderer.image_skin == None:
        #     Wanderer.image_skin = load_image('skin1.png')
        # if Wanderer.image_pants == None:
        #     Wanderer.image_pants = load_image('.\wanderer\pants1.png')
        # if Wanderer.image_shirts == None:
        #     Wanderer.image_shirts = load_image('shirts1.png')
        # if Wanderer.image_boots == None:
        #     Wanderer.image_boots = load_image('boots1.png')


    def __init__(self, x, y):
        self.width_image = 800
        self.height_image = 448

        self.count_h = 10
        self.count_v = 7

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.load_image()
        self.x, self.y = 0, 0
        self.pos_x, self.pos_y = x, y - 5
        self.center_error_x = 0
        self.draw_x = self.size_h * 1.8
        self.draw_y = self.size_v * 1.6
        self.dir = 1


        self.wanderer_index = 0

        self.part_image_indices = [0, 0, 0, 0]




        self.state = Idle
        #self.build_behavior_tree()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)


    def get_bb(self):
        return self.pos_x - self.draw_x / 4, self.pos_y - self.draw_y / 4, self.pos_x + self.draw_x / 4, self.pos_y + self.draw_y / 2


    def update(self):
        #self.bt.run()
        #print(f'{self.state}')
        print(f'{self.state_machine.cur_state}')

        if self.state_machine.cur_state != self.state:
            self.state_machine.start(self.state)
        self.state_machine.update()
        pass

    def draw(self):
        self.state_machine.draw()
        # self.image_skin.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
        # self.image_pants.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
        # self.image_shirts.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
        # self.image_boots.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)


class Idle:
    @staticmethod
    def enter(wanderer, e):
        wanderer.idle_start_time = get_time()
        wanderer.index_v = 7 - 1
        wanderer.index_h = 0

    @staticmethod
    def exit(wanderer, e):
        pass

    @staticmethod
    def do(wanderer):
        wanderer.index_h = (wanderer.index_h + 5 * 1.5 * game_framework.frame_time) % 5


    @staticmethod
    def draw(wanderer):
        if wanderer.dir > 0:
            for part_index in range(4):
                wanderer.image_wanderer[wanderer.wanderer_index][part_index][wanderer.part_image_indices[0]].clip_draw(int(wanderer.index_h) * wanderer.size_h, wanderer.index_v * wanderer.size_v, wanderer.size_h - wanderer.center_error_x, wanderer.size_v, wanderer.pos_x, wanderer.pos_y + 29, wanderer.draw_x, wanderer.draw_y)

            # self.image_skin.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
            # self.image_pants.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
            # self.image_shirts.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
            # self.image_boots.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
        else:
            for part_index in range(4):
                wanderer.image_wanderer[wanderer.wanderer_index][part_index][wanderer.part_image_indices[0]].clip_draw(int(wanderer.index_h) * wanderer.size_h, wanderer.index_v * wanderer.size_v, wanderer.size_h - wanderer.center_error_x, wanderer.size_v, wanderer.pos_x, wanderer.pos_y + 29, wanderer.draw_x, wanderer.draw_y)


class Walk:
    @staticmethod
    def enter(wanderer, e):
        wanderer.index_v = 3 - 1
        wanderer.index_h = 0

    @staticmethod
    def exit(wanderer, e):
        pass

    @staticmethod
    def do(wanderer):
        wanderer.index_h = (wanderer.index_h + 8 * 1.5 * game_framework.frame_time) % 8
        print(f'            {int(wanderer.index_h)}')

    @staticmethod
    def draw(wanderer):
        if wanderer.dir > 0:
            for part_index in range(4):
                wanderer.image_wanderer[wanderer.wanderer_index][part_index].clip_draw(
                    int(wanderer.index_h) * wanderer.size_h, wanderer.index_v * wanderer.size_v,
                    wanderer.size_h - wanderer.center_error_x, wanderer.size_v, wanderer.pos_x, wanderer.pos_y + 29,
                    wanderer.draw_x, wanderer.draw_y)

        else:
            for part_index in range(4):
                wanderer.image_wanderer[wanderer.wanderer_index][part_index].clip_draw(
                    int(wanderer.index_h) * wanderer.size_h, wanderer.index_v * wanderer.size_v,
                    wanderer.size_h - wanderer.center_error_x, wanderer.size_v, wanderer.pos_x, wanderer.pos_y + 29,
                    wanderer.draw_x, wanderer.draw_y)

