import random
from random import randint

from pico2d import load_image, get_time

import game_framework
import play_mode
from archer import Archer

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from maid import Maid
from state_machine import StateMachine

image_counts = [[1, 4, 3, 1, 1], [1, 4, 1, 1, 1]]
wanderer_names = ['man', 'woman']
part_names = ['skin', 'hair', 'pants', 'shirts', 'boots']

class Wanderer:
    image_wanderer = None
    image_skin = None
    image_hair = None
    image_pants = None
    image_boots = None
    image_shirts = None


    def load_image(self):
        if self.image_wanderer == None:
            self.image_wanderer = {}
            for wanderer_index in range(2):
                self.image_wanderer[wanderer_index] ={}
                wanderer_name = wanderer_names[wanderer_index]
                for part_index in range (5):
                    part_name = part_names[part_index]
                    self.image_wanderer[wanderer_index][part_index] = {}
                    for part_image_index in range(0, image_counts[wanderer_index][part_index]):
                        print("./wanderer/" + wanderer_name + "/" + part_name + "/" + part_name + "%d" % (part_image_index+1) + ".png")
                        self.image_wanderer[wanderer_index][part_index][part_image_index] = load_image("./wanderer/"+ wanderer_name + "/" + part_name + "/" + part_name + "%d" %(part_image_index+1) + ".png")


        # if Wanderer.image_skin == None:
        #     Wanderer.image_skin = load_image('skin1.png')
        # if Wanderer.image_pants == None:
        #     Wanderer.image_pants = load_image('.\wanderer\pants1.png')
        # if Wanderer.image_shirts == None:
        #     Wanderer.image_shirts = load_image('shirts1.png')
        # if Wanderer.image_boots == None:
        #     Wanderer.image_boots = load_image('boots1.png')


    def __init__(self, x, y, camp):
        self.camp = camp

        self.width_image = 800
        self.height_image = 448

        self.count_h = 10
        self.count_v = 7

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.ground = y
        self.load_image()
        self.x, self.y = 0, 0
        self.pos_x, self.pos_y = x, y + 22
        self.center_error_x = 0
        self.draw_x = 145
        self.draw_y = 135 * self.size_v / (self.size_h - self.center_error_x)
        self.dir = 1

        self.selected = 0

        self.wanderer_index = randint(0, 1)

        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        if self.wanderer_index == 0:
            self.part_image_indices = [0, randint(0, 3), 2, 0, 0]
        else:
            self.part_image_indices = [0, randint(0, 3), 0, 0, 0]



        play_mode.game_world.add_collision_pair('character:wanderer', None, self)

        self.state = Idle
        self.build_behavior_tree()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)




    def get_bb(self):
        return self.pos_x - self.draw_x , self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x, self.pos_y + self.draw_y / 2

    def handle_collision(self, group, other):
        if group == 'character:wanderer':

            pass

    def update(self):
        self.bt.run()
        #print(f'{self.state}')
        print(f'{self.state_machine.cur_state}')

        if self.state_machine.cur_state != self.state:
            self.state_machine.start(self.state)
        self.state_machine.update()
        pass

    def draw(self):
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        self.state_machine.draw()

        # self.image_skin.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
        # self.image_pants.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
        # self.image_shirts.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
        # self.image_boots.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
    def interact(self):
        self.be_civil()

    def be_civil(self):
        self.camp.wanderer_count -= 1

        if self.wanderer_index == 0:
            new_archer = Archer(self.pos_x, self.ground)
            play_mode.game_world.add_object(new_archer, 3)
            play_mode.game_world.remove_object(self)
        elif self.wanderer_index == 1:
            new_maid = Maid(self.pos_x, self.ground)
            play_mode.game_world.add_object(new_maid, 3)
            play_mode.game_world.remove_object(self)


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
        minx, _, maxx, _ = self.camp.get_bb()
        self.tx, self.ty = randint(int(minx), int(maxx)), self.pos_y
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



    def build_behavior_tree(self):
        a0 = Action('Wait', self.wait_time)
        ACT_set_wait_time = Action('Set Wait Time', self.set_wait_time)
        SEQ_wait_time = Sequence('Wait', ACT_set_wait_time, a0)
        a1 = Action('Move to', self.move_to)

        a2 = Action('Set random location', self.set_random_location)
        root = SEQ_wander = Sequence('Wander', a2, a1, SEQ_wait_time)



        self.bt = BehaviorTree(root)

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
                wanderer.image_wanderer[wanderer.wanderer_index][part_index][wanderer.part_image_indices[part_index]].clip_draw(int(wanderer.index_h) * wanderer.size_h, wanderer.index_v * wanderer.size_v, wanderer.size_h - wanderer.center_error_x, wanderer.size_v, wanderer.clip_pos_x, wanderer.clip_pos_y, wanderer.draw_x, wanderer.draw_y)

            # self.image_skin.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
            # self.image_pants.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
            # self.image_shirts.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
            # self.image_boots.clip_draw(0, 0, self.size_h, self.size_v, self.pos_x, self.pos_y, self.x, self.y)
        else:
            for part_index in range(4):
                wanderer.image_wanderer[wanderer.wanderer_index][part_index][wanderer.part_image_indices[part_index]].clip_draw(int(wanderer.index_h) * wanderer.size_h, wanderer.index_v * wanderer.size_v, wanderer.size_h - wanderer.center_error_x, wanderer.size_v, wanderer.clip_pos_x, wanderer.clip_pos_y, wanderer.draw_x, wanderer.draw_y)


class Walk:
    @staticmethod
    def enter(wanderer, e):
        wanderer.index_v = 6 - 1
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
        if wanderer.dir < 0:
            for part_index in range(4):
                wanderer.image_wanderer[wanderer.wanderer_index][part_index][wanderer.part_image_indices[part_index]].clip_draw(
                    int(wanderer.index_h) * wanderer.size_h, wanderer.index_v * wanderer.size_v,
                    wanderer.size_h - wanderer.center_error_x, wanderer.size_v, wanderer.clip_pos_x, wanderer.clip_pos_y,
                    wanderer.draw_x, wanderer.draw_y)

        else:
            for part_index in range(4):
                wanderer.image_wanderer[wanderer.wanderer_index][part_index][wanderer.part_image_indices[part_index]].clip_composite_draw(
                    int(wanderer.index_h) * wanderer.size_h, wanderer.index_v * wanderer.size_v,
                    wanderer.size_h - wanderer.center_error_x, wanderer.size_v,0, 'h', wanderer.clip_pos_x, wanderer.clip_pos_y,
                    wanderer.draw_x, wanderer.draw_y)

