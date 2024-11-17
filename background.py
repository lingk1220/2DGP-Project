from pico2d import load_image

import play_mode


class Background:

    images = [None] * 4
    def __init__(self):
        self.width_image = 576
        self.height_image = 324
        self.draw_x = 0
        self.draw_y = -400
        for i in range(0, 4):
            if Background.images[i] == None:
                name = 'Sky' + (str)(i+1) + '.png'
                Background.images[i] = load_image(name)
                pass

    def get_bb(self):
        return -10000, -10000, 10000, 10000
    def update(self):

        pass

    def draw(self):
        for i in range(0,4):
            self.images[i].clip_draw_to_origin(int(self.draw_x) , int(self.draw_y) - 400,  2304, 1296, -int(play_mode.character.pos_x / 20 * i) - 300, -200)
            # self.images[i].clip_draw(0,
            #                          0,
            #                          self.width_image,
            #                          self.height_image,
            #                          1400 // 2,
            #                          800 // 2, self.width_image * 4, self.height_image * 4 - 300)
            #
            #
