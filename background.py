from pico2d import load_image


class Background:

    images = [None] * 4
    def __init__(self):
        self.width_image = 576
        self.height_image = 324

        for i in range(0, 4):
            if Background.images[i] == None:
                name = 'Sky' + (str)(i+1) + '.png'
                Background.images[i] = load_image(name)
                pass
    def update(self):
        pass

    def draw(self):
        for i in range(0,4):
            self.images[i].clip_draw(0,
                                     0,
                                     self.width_image,
                                     self.height_image,
                                     1400 // 2,
                                     800 // 2, self.width_image * 3, self.height_image * 3)
