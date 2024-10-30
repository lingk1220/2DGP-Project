import random

from pico2d import load_image

from play_mode import width, height


class Archer:
    global width, height
    image = None
    def __init__(self, x, y):
        self.width_image = 704
        self.height_image = 320

        self.count_h = 11
        self.count_v = 5

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = x
        self.index_v = y
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Archer.image == None:
            Archer.image = load_image('Archer.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.index_h * self.size_h,
                             self.index_v * self.size_v,
                             self.size_h,
                             self.size_v,
                             self.size_h * self.index_h + width // 2,
                             self.size_v * self.index_v + height // 2, 96, 96)
