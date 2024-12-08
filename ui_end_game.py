
from pico2d import load_image

from ui import UI
from ui_end_game_blur import EndingBlurUI
from ui_menubox import MenuboxUI
from ui_screenblur import ScreenBlurUI


class EndingUI:

    def __init__(self, dir):
        self.ui = UI()
        self.canvas_width = 1400
        self.canvas_height = 800
        self.ui_positions = [(0, 0)]

        self.endingblurui = EndingBlurUI(self.canvas_width // 2, self.canvas_height // 2, dir)
        self.ui.input_UI(self.endingblurui)


    def get_bb(self):
        return -10000, -10000, 10000, 10000

    def update(self):

        return self.endingblurui.update()


    def draw(self):
        self.ui.draw()
