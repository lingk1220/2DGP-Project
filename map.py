from os import remove
from random import randint
from urllib.request import build_opener

from pico2d import draw_rectangle

import game_world
import play_mode
from chicken_field import ChickenField
from enemy_building import EnemyBuilding
from ground import Ground
from obelisk import Obelisk
from camp import Camp
from obelisk2 import Obelisk2
from rock import Rock
from wall import Wall


class Map:
    def __init__(self,x, ground):
        self.map_size = 75
        self.tile_size = 96
        self.enemy_cutline = 0.8
        self.x = 0
        self.ground = ground

        self.elements = None

        self.grounds = [[], []]
        self.buildings = [[], []]
        self.walls = [[], []]

        self.enemy_buildings = [[], []]



        # self.build_walls(0, 3)

        # self.build_walls(1, 7)

        self.generate_map()
        self.build_walls(0, 5)

    def generate_map(self):
        self.elements = []
        self.buildings[0] = [None for _ in range(self.map_size)]
        self.buildings[1] = [None for _ in range(self.map_size)]
        self.elements.append(self.grounds)

        self.walls[0] = [None for _ in range(self.map_size)]
        self.walls[1] = [None for _ in range(self.map_size)]
        self.elements.append(self.walls)
        self.elements.append(self.buildings)
        self.elements.append(self.enemy_buildings)

        self.init_grounds(0, 0)
        self.init_grounds(1, 0)

        self.init_buildings(0, 5)
        self.init_buildings(1, 5)

        self.init_enemy_buildings(0, 0)
        self.init_enemy_buildings(1, 0)



    def get_bb(self):
        return 0, 0, 0, 0

    def update(self):
        for layer in self.elements:
            for layer_half in layer:
                for o in layer_half:
                    if o != None:
                        o.update()


    def draw(self):
        for layer in self.elements:
            for layer_half in layer:
                for o in layer_half:
                    if o != None:
                        o.draw()


    def draw_bb(self):
        for layer in self.elements:
            for layer_half in layer:
                for o in layer_half:

                    if o != None and o.__class__ != Ground:
                        l, b, r, t = o.get_bb()
                        l = 700 - play_mode.character.pos_x + l
                        r = 700 - play_mode.character.pos_x + r
                        draw_rectangle(l, b, r, t)


    def input_wall(self, dir, x_index):
        play_mode.character.lose_money(1)
        self.walls[dir][x_index] = (Wall(self, dir, x_index, self.ground))


    def input_building(self, dir, x_index):
        factor = randint(0, 150)

        if 0 <= factor < 20:
            self.buildings[dir][x_index] = (Camp(self, dir, x_index, self.ground))
        elif 20 <= factor < 130:
            self.buildings[dir][x_index] = (Rock(self, dir, x_index, self.ground))
        elif 130 <= factor < 150:
            self.buildings[dir][x_index] = (ChickenField(self, dir, x_index, self.ground))

    def build_walls(self, dir, x_index):
            t= 0
            for i in range(0, x_index):
                if self.walls[dir][i] != None:
                    t = i

            for i in range(t, x_index):
                self.input_wall(dir, i)
            pass

    def init_buildings(self, dir, x_index):
        if x_index < self.map_size:
            self.input_building(dir, x_index)
            self.init_buildings(dir, x_index + randint(5, 10))


    def input_ground(self, dir, x_index):
        self.grounds[dir].append(Ground(self, dir, x_index, 0, self.ground))
        self.grounds[dir].append(Ground(self, dir, x_index, 1, self.ground))
        self.grounds[dir].append(Ground(self, dir, x_index, 2, self.ground))

    def init_grounds(self, dir, x_index):
        if x_index < self.map_size:
            self.input_ground(dir, x_index)
            self.init_grounds(dir, x_index + 1)


    def input_enemy_building(self, dir, x_index):
        self.enemy_buildings[dir].append(EnemyBuilding(self, dir, x_index, self.ground))


    def init_enemy_buildings(self, dir, x_index):
        if x_index < self.map_size * self.enemy_cutline:
            self.input_enemy_building(dir, self.map_size - x_index)
            self.init_enemy_buildings(dir, x_index + randint(10, 20))

    def remove_walls(self, o):
        dir = o.dir
        i = o.x_index
        self.remove_map_object(self.walls[dir][i])
        i -= 1
        while (self.buildings[dir][i] == None or self.buildings[dir][i].__class__ != Rock) and i >0:
            self.remove_map_object(self.walls[dir][i])
            i -= 1


    def remove_map_object(self, o):
        print(f'o: {o}')

        for index, i in enumerate(self.walls[0]):
            if i == o:
                self.walls[0][index] = None

        for index, i in enumerate(self.walls[1]):
            if i == o:
                self.walls[1][index] = None

        for index, i in enumerate(self.buildings[0]):
            if i == o:
                self.buildings[0][index] = None

        for index, i in enumerate(self.buildings[1]):
            if i == o:
                self.buildings[1][index] = None

        game_world.remove_collision_object(o)