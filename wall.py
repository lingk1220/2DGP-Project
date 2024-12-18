from pico2d import load_image

import play_mode


class Wall:
    image = None
    def __init__(self,map, dir, x, y):
        self.width_image = 864
        self.height_image = 1280

        self.map = map
        self.count_h = 27
        self.count_v = 40

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = 14 - 1
        self.index_v = 29 - 1

        self.dir = dir

        self.x_index = x

        self.pos_x = x * map.tile_size * (dir * 2 - 1)
        self.pos_y = y + self.size_v * 2 / 2 - 3

        self.tiles_h = 2
        self.tiles_v = 2

        self.is_dying = 0
        self.hp = 30
        self.draw_x = self.size_h * self.tiles_h * 1.9
        self.draw_y = self.size_v * self.tiles_v * 1.9

        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        play_mode.game_world.add_collision_pair('character:building', None, self)
        play_mode.game_world.add_collision_pair('enemy:ally', None, self)

        if Wall.image == None:
            Wall.image = load_image('Props2.png')

    def get_bb(self):
        return self.pos_x - self.draw_x / 2.5, self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x / 2.5, self.pos_y + self.draw_y / 2.8

    def handle_collision(self, group, other):
        if group == 'character:building':

            pass


    def update(self):
        pass

    def draw(self):
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        self.image.clip_composite_draw(self.index_h * self.size_h,
                                        self.index_v * self.size_v,
                                        self.size_h * self.tiles_h,
                                       self.size_v * self.tiles_v,
                                       0,
                                       '',
                                       self.clip_pos_x,
                                       self.clip_pos_y,
                                       self.draw_x, self.draw_y
                                       )



    def interact(self):
        pass

    def attacked(self, other):
        self.hp -= 1
        if self.hp <= 0:

            self.map.remove_walls(self)
            self.is_dying = 1