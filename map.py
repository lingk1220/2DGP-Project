from os import remove
from random import randint
from urllib.request import build_opener

from pico2d import draw_rectangle

import game_world
import play_mode
from chicken_field import ChickenField
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

        self.x = 0
        self.ground = ground

        self.elements = None

        self.grounds = [[], []]
        self.buildings = [[], []]
        self.walls = [[], []]

        self.enemy_buildings = [[], []]

        # self.build_walls(0, 3)
        # self.build_walls(0, 5)
        # self.build_walls(1, 7)

        self.generate_map()


    def generate_map(self):
        self.elements = []
        self.elements.append(self.grounds)
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
                    o.update()
        # for i in range(len(self.walls[0])):
        #     self.walls[0][i].update()
        # for i in range(len(self.walls[1])):
        #     self.walls[1][i].update()
        #
        # for i in range(len(self.buildings[0])):
        #     self.buildings[0][i].update()
        # for i in range(len(self.buildings[1])):
        #     self.buildings[1][i].update()
        #
        # for i in range(len(self.enemy_buildings[0])):
        #     self.enemy_buildings[0][i].update()
        #
        # for i in range(len(self.enemy_buildings[1])):
        #     self.enemy_buildings[1][i].update()
        #
        # pass

    def draw(self):
        for layer in self.elements:
            for layer_half in layer:
                for o in layer_half:
                    o.draw()
        # for i in range(len(self.walls[0])):
        #     self.walls[0][i].draw()
        # for i in range(len(self.walls[1])):
        #     self.walls[1][i].draw()
        #
        # for i in range(len(self.buildings[0])):
        #     self.buildings[0][i].draw()
        # for i in range(len(self.buildings[1])):
        #     self.buildings[1][i].draw()
        #
        # for i in range(len(self.enemy_buildings[0])):
        #     self.enemy_buildings[0][i].draw()
        #
        # for i in range(len(self.enemy_buildings[1])):
        #     self.enemy_buildings[1][i].draw()


    def draw_bb(self):
        for i in range(len(self.walls[0])):
            l, b, r, t = self.walls[0][i].get_bb()
            l = 700 - play_mode.character.pos_x + l
            r = 700 - play_mode.character.pos_x + r
            draw_rectangle(l, b, r, t)
        for i in range(len(self.walls[1])):
            l, b, r, t = self.walls[1][i].get_bb()
            l = 700 - play_mode.character.pos_x + l
            r = 700 - play_mode.character.pos_x + r
            draw_rectangle(l, b, r, t)

        for i in range(len(self.buildings[0])):
            l, b, r, t = self.buildings[0][i].get_bb()
            l = 700 - play_mode.character.pos_x + l
            r = 700 - play_mode.character.pos_x + r
            draw_rectangle(l, b, r, t)
        for i in range(len(self.buildings[1])):
            l, b, r, t = self.buildings[1][i].get_bb()
            l = 700 - play_mode.character.pos_x + l
            r = 700 - play_mode.character.pos_x + r
            draw_rectangle(l, b, r, t)


    def input_wall(self, dir, x_index):
        self.walls[dir].append(Wall(self, dir, x_index, self.ground))


    def input_building(self, dir, x_index):
        factor = randint(0, 150)
        if 0 <= factor < 50:
            self.buildings[dir].append(Camp(self, dir, x_index, self.ground))
        elif 50 <= factor < 100:
            self.buildings[dir].append(Rock(self, dir, x_index, self.ground))
        elif 100 <= factor < 150:
            self.buildings[dir].append(ChickenField(self, dir, x_index, self.ground))

    def build_walls(self, dir, x_index):

            for i in range(len(self.walls[dir]), x_index):
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
        self.enemy_buildings[dir].append(Obelisk2(self, dir, x_index, self.ground))


    def init_enemy_buildings(self, dir, x_index):
        if x_index < self.map_size / 3:
            self.input_enemy_building(dir, self.map_size - x_index)
            self.init_enemy_buildings(dir, x_index + randint(10, 20))

    def remove_walls(self, o):
        dir = o.dir
        i = o.x_index
        while self.buildings[dir][i].__class__ != 'Rock' and i >0:
            self.remove_map_object(self.walls[dir][i])
            i -= 1


    def remove_map_object(self, o):
        if o in self.walls[0]:
            self.walls[0].remove(o)
        if o in self.walls[1]:
            self.walls[1].remove(o)

        if o in self.buildings[0]:
            self.buildings[0].remove(o)
        if o in self.buildings[1]:
            self.buildings[1].remove(o)

        game_world.remove_collision_object(o)