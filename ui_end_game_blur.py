from pico2d import load_font, load_image

import game_framework
import game_world


class EndingBlurUI:

    image_background = None
    def __init__(self, offset_x, offset_y, dir):

        self.ui_count = 1
        self.image_count = 1

        self.t = 0
        self.mt = 100
        self.dir = dir

        self.text_count = 3
        self.texts = ['Resume', 'Setting', 'Exit Game']
        self.text_offset = [(77, 0), (82, 0), (48, 0)]
        self.text_parent = [1, 2, 3]
        self.image_index = [0, 1, 1, 1, 2, 1, 5, 6]
        self.canvas_width = 1400
        self.canvas_height = 800

        self.draw_offset_x = offset_x
        self.draw_offset_y = offset_y

        if EndingBlurUI.image_background == None:
            EndingBlurUI.image_background = load_image('./UI/blur/background_blur.png')
            EndingBlurUI.image_background.opacify(0)


    def get_bb(self):
        return -10000, -10000, 10000, 10000

    def update(self):
        r = 0

        if self.t < self.mt:
            self.t += 0.5
        else:
            self.t = self.mt
            r = 1
            pass

        if self.dir == 1:
            self.image_background.opacify(self.t / self.mt)

        elif self.dir == -1:
            self.image_background.opacify(1 - self.t / self.mt)

        return r

    def draw(self):

        self.image_background.clip_draw(0, 0, 128, 128, self.canvas_width // 2, self.canvas_height // 2, self.canvas_width, self.canvas_height)
