from pico2d import load_font, load_image


class MenuboxUI:

    images = [None] * 7
    image_background = None
    def __init__(self, offset_x, offset_y):
        self.width_image = [96, 41, 128, 120, 120, 32, 32]
        self.height_image = [96, 41, 16, 8, 8, 32, 32]
        self.draw_rate = [6, 1.7, 1.7, 1.7, 1.7, 3, 2, 2]


        self.image_names = ['Menu_Box_Frame', '', 'Value_Bar', 'Value_HP', 'Value_Gold', 'sun', 'moon']
        self.image_index = [0, 3, 4, 2, 2, 1, 5, 6]
        self.canvas_width = 1400
        self.canvas_height = 800

        self.draw_offset_x = offset_x
        self.draw_offset_y = offset_y
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

        self.font = load_font('./Font/ByteBounce.TTF', 64)


        if MenuboxUI.image_background == None:
            MenuboxUI.image_background = load_image('./UI/MenuBox/Menu_Background3.png')

        for i in range(0, 1):
            if MenuboxUI.images[i] == None:
                name = './UI/' + 'MenuBox' + '/' + self.image_names[i] +  '.png'
                print(name)
                MenuboxUI.images[i] = load_image(name)
                pass

    def get_bb(self):
        return -10000, -10000, 10000, 10000
    def update(self):

        pass

    def draw(self):

        self.image_background.clip_draw(0, 0, 128, 128, self.canvas_width // 2, self.canvas_height // 2, self.canvas_width, self.canvas_height)
        for i in range(1):
            if i is not 6:
                d = self.image_index[i]
                self.images[d].clip_draw(0, 0, self.width_image[d], self.height_image[d], self.pos_x[i] + self.draw_offset_x, self.pos_y[i] + self.draw_offset_y, self.width_image[d]  * self.draw_rate[i], self.height_image[d] * self.draw_rate[i])

        self.font.draw(700, 400, f'Exit Game', (210, 201, 165))
