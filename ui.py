from pico2d import load_image

import play_mode




class UI:

    images = [None] * 5
    def __init__(self):
        self.width_image = [160, 41, 128, 120, 120]
        self.height_image = [41, 41, 16, 8, 8]
        self.image_names = ['Heart_Bar_Panel', 'Circle_Box', 'Value_Bar', 'Value_HP', 'Value_Gold']
        self.draw_x = 0
        self.draw_y = -400
        for i in range(0, 5):
            if UI.images[i] == None:
                name = './UI/' + 'HeartBar' + '/' + self.image_names[i] +  '.png'
                print(name)
                UI.images[i] = load_image(name)
                pass

    def get_bb(self):
        return -10000, -10000, 10000, 10000
    def update(self):

        pass

    def draw(self):
        for i in range(0,4):
            print('what')
            self.images[i].clip_draw(0, 0, self.width_image[i], self.height_image[i], 50, 700, self.width_image[i], self.height_image[i])
            # self.images[i].clip_draw(0,
            #                          0,
            #                          self.width_image,
            #                          self.height_image,
            #                          1400 // 2,
            #                          800 // 2, self.width_image * 4, self.height_image * 4 - 300)
            #
            #
