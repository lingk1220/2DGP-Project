from pico2d import load_font, load_image
from sdl2.ext import MessageBox


class MenuboxUI:

    images = [None] * 7
    image_background = None
    menu_font64 = None
    def __init__(self, offset_x, offset_y):
        self.width_image = [96, 64, 128, 120, 120, 32, 32]
        self.height_image = [96, 16 , 16, 8, 8, 32, 32]
        self.draw_rate = [6, 5, 5, 5, 1.7, 3, 2, 2]

        self.ui_count = 4
        self.image_count = 2
        self.image_names = ['Menu_Box_Frame', 'Title_Box', 'Value_Bar', 'Value_HP', 'Value_Gold', 'sun', 'moon']

        self.text_count = 3
        self.texts = ['Resume', 'Setting', 'Exit Game']
        self.text_offset = [(77, 0), (82, 0), (48, 0)]
        self.text_parent = [1, 2, 3]
        self.image_index = [0, 1, 1, 1, 2, 1, 5, 6]
        self.canvas_width = 1400
        self.canvas_height = 800

        self.draw_offset_x = offset_x
        self.draw_offset_y = offset_y
        self.pos_x = [(0 + self.width_image[self.image_index[0]]  / 2)* self.draw_rate[0],
                      (25 + self.width_image[self.image_index[1]] / 2) * self.draw_rate[2],
                      (25 + self.width_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      (25 + self.width_image[self.image_index[3]] /2)* self.draw_rate[2],
                      (50 + self.width_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      (-10 + self.width_image[self.image_index[5]] / 2) * self.draw_rate[5],
                      (-1 + self.width_image[self.image_index[6]] / 2) * self.draw_rate[6],
                      (-1 + self.width_image[self.image_index[7]] / 2) * self.draw_rate[7]
                      ]

        self.pos_y = [( - 0- self.height_image[self.image_index[0]]  / 2)* self.draw_rate[0] ,
                      ( - 18 - self.height_image[self.image_index[1]] / 2) * self.draw_rate[2],
                      ( - 48 - self.height_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      ( - 78 - self.height_image[self.image_index[3]] / 2) * self.draw_rate[2],
                      ( - 29 - self.height_image[self.image_index[2]] / 2) * self.draw_rate[2],
                      (  7 - self.height_image[self.image_index[5]] / 2) * self.draw_rate[5],
                      (-4 - self.height_image[self.image_index[6]] / 2) * self.draw_rate[6],
                      (-4 - self.height_image[self.image_index[7]] / 2) * self.draw_rate[7]
                      ]

        if MenuboxUI.menu_font64 == None:
            MenuboxUI.menu_font64 = load_font('./Font/ByteBounce.TTF', 64)


        if MenuboxUI.image_background == None:
            MenuboxUI.image_background = load_image('./UI/MenuBox/Menu_Background3.png')

        for i in range(0, self.image_count):
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

        MenuboxUI.image_background.clip_draw(0, 0, 128, 128, self.canvas_width // 2, self.canvas_height // 2, self.canvas_width, self.canvas_height)
        for i in range(self.ui_count):
            if i is not 6:
                d = self.image_index[i]
                MenuboxUI.images[d].clip_draw(0, 0, self.width_image[d], self.height_image[d], self.pos_x[i] + self.draw_offset_x, self.pos_y[i] + self.draw_offset_y, self.width_image[d]  * self.draw_rate[i], self.height_image[d] * self.draw_rate[i])

        for i in range(self.text_count):
            ui_index = self.text_parent[i]
            d = self.image_index[ui_index]
            MenuboxUI.menu_font64.draw(self.text_offset[i][0] + self.pos_x[ui_index] + self.draw_offset_x - ((self.width_image[d]  * self.draw_rate[ui_index]) // 2), self.text_offset[i][1] + self.pos_y[ui_index] + self.draw_offset_y, self.texts[i], (210, 201, 165))

