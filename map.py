from os import remove
from random import randint
from urllib.request import build_opener

from pico2d import draw_rectangle

import enemy_building
import game_world
import play_mode
from chicken_field import ChickenField
from enemy_building import EnemyBuilding
from farm import Farm
from ground import Ground
from house import House
from obelisk import Obelisk
from camp import Camp
from obelisk2 import Obelisk2
from rock import Rock
from state_machine import right_down
from wall import Wall



class Map:
    def __init__(self,x, ground):
        self.map_size = 50
        self.tile_size = 96
        self.enemy_cutline = 0.4
        self.x = 0
        self.ground = ground

        self.elements = None

        self.grounds = [[], []]
        self.buildings = [[], []]
        self.walls = [[], []]

        self.enemy_buildings = [[], []]
        self.house = [None]

        self.left_enemy_building  = None
        self.right_enemy_building = None
        # self.build_walls(0, 3)

        # self.build_walls(1, 7)

        self.generate_map()

    def generate_map(self):
        self.elements = []
        self.buildings[0] = [None for _ in range(self.map_size + 1)]
        self.buildings[1] = [None for _ in range(self.map_size + 1)]
        self.elements.append(self.grounds)

        self.walls[0] = [None for _ in range(self.map_size)]
        self.walls[1] = [None for _ in range(self.map_size)]
        self.elements.append(self.walls)
        self.elements.append(self.buildings)

        self.enemy_buildings[0] = [None for _ in range(self.map_size + 1)]
        self.enemy_buildings[1] = [None for _ in range(self.map_size + 1)]
        self.elements.append(self.enemy_buildings)

        self.init_grounds(0, 0)
        self.init_grounds(1, 0)

        self.buildings[0][7] = (Camp(self, 0, 7, self.ground))
        self.buildings[1][7] = (Farm(self, 1, 7, self.ground))
        self.buildings[0][15] = (ChickenField(self, 0, 15, self.ground))
        self.buildings[0][22] = (Rock(self, 0, 22, self.ground))
        self.buildings[1][15] = (Rock(self, 1, 15, self.ground))



        self.init_buildings(0, 30)
        self.init_buildings(1, 22)


        self.init_enemy_buildings(0, 0)
        self.init_enemy_buildings(1, 0)

        self.house[0] = [House(self, 1, 0, self.ground)]
        self.elements.append(self.house)
        self.init_enemy_building()

        self.left_none = False
        self.right_none = False


    def get_bb(self):
        return 0, 0, 0, 0

    def update(self):
        for layer in self.elements:
            for layer_half in layer:
                for o in layer_half:
                    if o != None:

                        if o.__class__ == EnemyBuilding:
                            if o.building.__class__ == Obelisk or o.building.__class__ == Obelisk2:
                                if o == self.left_enemy_building or o == self.right_enemy_building:

                                    o.update()
                        else:
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

        self.walls[dir][x_index] = (Wall(self, dir, x_index, self.ground))


    def input_building(self, dir, x_index):
        factor = randint(0, 200)

        if 0 <= factor < 30:
            self.buildings[dir][x_index] = (Camp(self, dir, x_index, self.ground))
        elif 30 <= factor < 150:
            self.buildings[dir][x_index] = (Rock(self, dir, x_index, self.ground))
        elif 150 <= factor < 180:
            self.buildings[dir][x_index] = (ChickenField(self, dir, x_index, self.ground))
        elif 180 <= factor < 200:
            self.buildings[dir][x_index] = (Farm(self, dir, x_index, self.ground))


    def build_walls(self, dir, x_index):
        if play_mode.character.money < 5:
            return

        play_mode.character.lose_money(5)
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
            self.init_buildings(dir, x_index + randint(5, 6))


    def input_ground(self, dir, x_index):
        self.grounds[dir].append(Ground(self, dir, x_index, 0, self.ground))
        self.grounds[dir].append(Ground(self, dir, x_index, 1, self.ground))
        self.grounds[dir].append(Ground(self, dir, x_index, 2, self.ground))

    def init_grounds(self, dir, x_index):
        if x_index < self.map_size + 20:
            self.input_ground(dir, x_index)
            self.init_grounds(dir, x_index + 1)


    def input_enemy_building(self, dir, x_index):

        self.enemy_buildings[dir][x_index] = (EnemyBuilding(self, dir, x_index, self.ground))


    def init_enemy_buildings(self, dir, x_index):
        if x_index < self.map_size * self.enemy_cutline:
            if self.buildings[dir][x_index] is not None:
                self.input_enemy_building(dir, self.map_size - (x_index + 5))
                self.init_enemy_buildings(dir, x_index + 5 + randint(10, 20))
            else:
                self.input_enemy_building(dir, self.map_size - x_index)
                self.init_enemy_buildings(dir, x_index+ randint(10, 20))

    def remove_walls(self, o):
        dir = o.dir
        i = o.x_index
        self.remove_map_object(self.walls[dir][i])
        i -= 1
        while (self.buildings[dir][i] == None or self.buildings[dir][i].__class__ != Rock) and i >0:
            self.remove_map_object(self.walls[dir][i])
            i -= 1


    def remove_map_object(self, o):

        s =  0

        for index, i in enumerate(self.walls[0]):
            if i == o:
                self.walls[0][index] = None
                s = 1
        for index, i in enumerate(self.walls[1]):
            if i == o:
                self.walls[1][index] = None
                s = 1
        for index, i in enumerate(self.buildings[0]):
            if i == o:
                self.buildings[0][index] = None
                s = 1
        for index, i in enumerate(self.buildings[1]):
            if i == o:
                self.buildings[1][index] = None
                s = 1
        for index, i in enumerate(self.enemy_buildings[0]):
            if i == o:
                self.enemy_buildings[0][index] = None
                s = 1
        for index, i in enumerate(self.enemy_buildings[1]):
            if i == o:
                self.enemy_buildings[1][index] = None
                s = 1

        if s == 1:
            game_world.remove_collision_object(o)

        return s

    def init_enemy_building(self):
        for o in self.enemy_buildings[0]:
            if o is not None:
                self.left_enemy_building = o
                break

        for o in self.enemy_buildings[1]:
            if o is not None:
                self.right_enemy_building = o
                break

    def reset_enemy_building(self, dir):
        tl = self.left_enemy_building
        tr = self.right_enemy_building
        if dir < 0:
            self.remove_map_object(self.left_enemy_building)
            for o in self.enemy_buildings[0]:
                if o is not None:
                    self.left_enemy_building = o
                    break

            if tl == self.left_enemy_building:
                self.left_none = True
        else:
            self.remove_map_object(self.right_enemy_building)
            for o in self.enemy_buildings[1]:
                if o is not None:
                    self.right_enemy_building = o
                    break

            if tr == self.right_enemy_building:
                self.right_none = True



        if self.left_none and self.right_none:
            play_mode.end_game('Win')