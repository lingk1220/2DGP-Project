from pico2d import load_image


class Ground:
    global width, height
    image = None
    def __init__(self, x, y):
        self.width_image = 512
        self.height_image = 512

        self.count_h = 16
        self.count_v = 16

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = 2 - 1
        self.index_v = 14 + y - 1
        self.x, self.y = x, y + 1
        self.draw_x = 0
        self.draw_y = 0
        if Ground.image == None:
            Ground.image = load_image('Ground.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.index_h * self.size_h,
                             self.index_v * self.size_v,
                             self.size_h,
                             self.size_v,
                             self.size_h * self.x,
                             self.size_v * self.y - 18)
