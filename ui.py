from pico2d import load_image

import play_mode



class UI:

    images = [None] * 7
    def __init__(self):
        self.width_image = [160, 41, 128, 120, 120, 32, 32]
        self.height_image = [41, 41, 16, 8, 8, 32, 32]
        self.draw_rate = [2, 1.7, 1.7, 1.7, 1.7, 3, 2, 2]

        self.image_names = ['Heart_Bar_Panel', 'Circle_Box', 'Value_Bar', 'Value_HP', 'Value_Gold', 'sun', 'moon']
        self.image_index = [0, 3, 4, 2, 2, 1, 5, 6]
        self.canvas_width = 1400
        self.canvas_height = 800

        self.draw_offset_x = [45]
        self.draw_offset_y = [self.canvas_height - 40]
        self.pos_x = [(0 + self.width_image[self.image_index[0]]  / 2)* self.draw_rate[0],
                      (50 + self.width_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      (50 + self.width_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      (50 + self.width_image[self.image_index[2]] /2)* self.draw_rate[2],
                      (50 + self.width_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      (-10 + self.width_image[self.image_index[5]] / 2) * self.draw_rate[5],
                      (-1 + self.width_image[self.image_index[6]] / 2) * self.draw_rate[6],
                      (-1 + self.width_image[self.image_index[7]] / 2) * self.draw_rate[7]
                      ]

        self.pos_y = [( - 0- self.height_image[self.image_index[0]]  / 2)* self.draw_rate[0] ,
                      ( - 12 - self.height_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      ( - 29 - self.height_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      ( - 12 - self.height_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      ( - 29 - self.height_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      (  7 - self.height_image[self.image_index[5]] / 2) * self.draw_rate[5],
                      (-4 - self.height_image[self.image_index[6]] / 2) * self.draw_rate[6],
                      (-4 - self.height_image[self.image_index[7]] / 2) * self.draw_rate[7]
                      ]

        for i in range(0, 7):
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
        for i in range(8):
            if i is not 6:
                d = self.image_index[i]
                self.images[d].clip_draw(0, 0, self.width_image[d], self.height_image[d], self.pos_x[i] + self.draw_offset_x[0], self.pos_y[i] + self.draw_offset_y[0], self.width_image[d]  * self.draw_rate[i], self.height_image[d] * self.draw_rate[i])
            # self.images[i].clip_draw(0,
            #                          0,
            #                          self.width_image,
            #                          self.height_image,
            #                          1400 // 2,
            #                          800 // 2, self.width_image * 4, self.height_image * 4 - 300)
            #
            #
