import math
import random
import time
from random import randint


import game_framework


from pico2d import load_image, get_time, draw_rectangle

import game_world
import play_mode
from chicken import Chicken
from obelisk import Obelisk
from obelisk2 import Obelisk2
from skeleton import Skeleton
from wanderer import Wanderer
from state_machine import StateMachine
from zombie import Zombie


class EnemyBuilding:
    image = None
    def __init__(self,map, dir, x, y):
        self.building = None
        self.map = map
        self.dir = dir

        self.x = x
        self.ground = y

        self.init_building()

        self.pos_x = self.building.pos_x
        self.enemy_count = 0
        self.enemy_count_max = 3


        self.spawn_timer = 0
        self.spawn_delay = 1.0



        self.tag = 'enemy'
    def get_bb(self):
        return self.building.get_bb()

    def handle_collision(self, group, other):
        pass


    def init_building(self):

        difficulty_cutline = self.map.map_size -  (self.map.map_size * self.map.enemy_cutline / 10)
        self.difficulty = self.x / self.map.map_size


        if self.x > difficulty_cutline:
            self.building = Obelisk2(self.map, self.dir, self.x, self.ground, self.difficulty)
        else:
            self.building = Obelisk(self.map, self.dir, self.x, self.ground, self.difficulty)

    def spawn_enemy(self):
        pass




    def update(self):
        self.building.update()



        pass

    def handle_event(self, event):
        pass


    def draw(self):
        self.building.draw()
