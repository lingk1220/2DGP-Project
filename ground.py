from pico2d import load_image

import play_mode


class Ground:
    global width, height
    image = None
    def __init__(self, map, dir, x_index, y_index, y):
        self.width_image = 512
        self.height_image = 512

        self.count_h = 16
        self.count_v = 16

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = 2 - 1
        self.index_v = 14 + y_index - 1

        self.map = map
        self.x, self.y = x_index, y_index
        self.pos_x = x_index * ((dir *2)-1) * map.tile_size
        self.pos_y = 11 + self.map.tile_size // 3 * self.y

        self.draw_x = self.size_h
        self.draw_y = self.size_v

        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        if Ground.image == None:
            Ground.image = load_image('Ground.png')

    def get_bb(self):
        return self.pos_x - self.draw_x / 2, self.pos_y - self.draw_y / 2, self.pos_x + self.draw_x / 2, self.pos_y + self.draw_y / 2

    def update(self):
        pass

    def draw(self):
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        Ground.image.clip_draw(self.index_h * self.size_h, self.index_v * self.size_v, self.size_h * 1, self.size_v, self.clip_pos_x - self.map.tile_size // 3, self.clip_pos_y)
        Ground.image.clip_draw(self.index_h * self.size_h, self.index_v * self.size_v, self.size_h * 1, self.size_v, self.clip_pos_x, self.clip_pos_y)
        Ground.image.clip_draw(self.index_h * self.size_h, self.index_v * self.size_v, self.size_h * 1, self.size_v, self.clip_pos_x + self.map.tile_size // 3, self.clip_pos_y)