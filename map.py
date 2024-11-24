from random import randint

from pico2d import draw_rectangle

import play_mode
from rock import Rock
from wall import Wall


class Map:
    def __init__(self,x, ground):
        self.tile_size = 96
        self.x = 0
        self.ground = ground
        self.buildings = [[], []]
        self.walls = [[], []]



        self.build_walls(0, 3)
        self.build_walls(0, 5)
        self.build_walls(1, 7)

        self.init_buildings(0, 1)
        self.init_buildings(1, 1)

    def get_bb(self):
        return 0, 0, 0, 0

    def update(self):
        pass

    def draw(self):
        for i in range(len(self.walls[0])):
            self.walls[0][i].draw()
        for i in range(len(self.walls[1])):
            self.walls[1][i].draw()

        for i in range(len(self.buildings[0])):
            self.buildings[0][i].draw()
        for i in range(len(self.buildings[1])):
            self.buildings[1][i].draw()

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
        if dir == 0:
            self.walls[dir].append(Wall(self, -1 * x_index * self.tile_size, self.ground))
        else:
            self.walls[dir].append(Wall(self, 1 * x_index * self.tile_size, self.ground))

    def input_building(self, dir, x_index):
        if dir == 0:
            self.buildings[dir].append(Rock(self, -1 * x_index * self.tile_size, self.ground))
        else:
            self.buildings[dir].append(Rock(self, 1 * x_index * self.tile_size, self.ground))


    def build_walls(self, dir, x_index):
        for i in range(len(self.walls[dir]), x_index):
            self.input_wall(dir, i)
        pass

    def init_buildings(self, dir, x_index):
        print('dpd')
        self.input_building(dir, x_index)
        if x_index < 100:
            self.init_buildings(dir, x_index + randint(5, 10))
