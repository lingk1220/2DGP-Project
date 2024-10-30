import random

from pico2d import load_image

from play_mode import width, height


class Skeleton:
    global width, height
    image = None
    def __init__(self, x, y):
        self.width_image = 600
        self.height_image = 150

        self.count_h = 4
        self.count_v = 1

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = x
        self.index_v = y
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Skeleton.image == None:
            Skeleton.image = load_image('Skeleton_Idle.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.index_h * self.size_h + 60,
                             self.index_v * self.size_v + 30,
                             self.size_h - 100,
                             self.size_v - 60,
                             self.size_h * self.index_h + width // 2 + 128,
                             self.size_v * self.index_v + height // 2, 100, 180)
