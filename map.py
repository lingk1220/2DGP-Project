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



        for i in range(10):
            self.input_walls(0, i)

        for i in range(10):
            self.input_building(1, i)

    def get_bb(self):
        return 0, 0, 0, 0

    def update(self):
        pass

    def draw(self):
        for i in range(len(self.walls[0])):
            self.walls[0][i].draw()

        for i in range(len(self.buildings[1])):
            self.buildings[1][i].draw()

    def input_walls(self, dir, x_index):
        if dir == 0:
            self.walls[dir].append(Wall(-1 * x_index * self.tile_size, self.ground))
        else:
            self.walls[dir].append(Wall(1 * x_index * self.tile_size, self.ground))

    def input_building(self, dir, x_index):
        if dir == 0:
            self.buildings[dir].append(Rock(-1 * x_index * self.tile_size, self.ground))
        else:
            self.buildings[dir].append(Rock(1 * x_index * self.tile_size, self.ground))
