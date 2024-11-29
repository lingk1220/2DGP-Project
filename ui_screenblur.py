from pico2d import load_font, load_image

import game_framework


class ScreenBlurUI:

    image_background = None
    def __init__(self, offset_x, offset_y):

        self.ui_count = 1
        self.image_count = 1

        self.t = 0
        self.mt = 255

        self.dir = 1

        self.text_count = 3
        self.texts = ['Resume', 'Setting', 'Exit Game']
        self.text_offset = [(77, 0), (82, 0), (48, 0)]
        self.text_parent = [1, 2, 3]
        self.image_index = [0, 1, 1, 1, 2, 1, 5, 6]
        self.canvas_width = 1400
        self.canvas_height = 800

        self.draw_offset_x = offset_x
        self.draw_offset_y = offset_y

        if ScreenBlurUI.image_background == None:
            ScreenBlurUI.image_background = load_image('./UI/blur/background_blur.png')



    def get_bb(self):
        return -10000, -10000, 10000, 10000

    def update(self):
        r = 0
        self.t = self.t + self.dir * 100 * game_framework.frame_time
        if 0 > self.t:
            r = 1
            self.dir = 1
            self.t = 0
        elif self.mt < self.t:
            self.dir = -1
            self.t = self.mt
        self.image_background.opacify(self.t / self.mt)
        return r
        pass

    def draw(self):

        self.image_background.clip_draw(0, 0, 128, 128, self.canvas_width // 2, self.canvas_height // 2, self.canvas_width, self.canvas_height)
