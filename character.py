import random

from pico2d import load_image

#from main import width, height

width = 1400
height = 800

class Character:
    global width, height
    image = None
    def __init__(self, x, y):
        self.width_image = 3626
        self.height_image = 594

        self.count_h = 37
        self.count_v = 9

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = x
        self.index_v = y
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Character.image == None:
            Character.image = load_image('JoannaD\'ArcIII-Sheet#1.png')

    def update(self):
        self.index_h = 1 - 1
        self.index_v = 9 - 1
        pass

    def draw(self):
        self.image.clip_draw(self.index_h * self.size_h,
                             self.index_v * self.size_v,
                             self.size_h,
                             self.size_v,
                             width // 2 + 64,
                             height // 2 + 64, self.size_h, self.size_v)
