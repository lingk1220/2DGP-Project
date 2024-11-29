
from pico2d import load_image

from ui import UI
from ui_menubox import MenuboxUI
from ui_screenblur import ScreenBlurUI


class TimeShiftUI:

    def __init__(self):
        self.ui = UI()
        self.canvas_width = 1400
        self.canvas_height = 800
        self.ui_positions = [(0, 0)]

        self.screenblurui = ScreenBlurUI(self.canvas_width // 2, self.canvas_height // 2)
        self.ui.input_UI(self.screenblurui)


    def get_bb(self):
        return -10000, -10000, 10000, 10000

    def update(self):
        return self.screenblurui.update()


    def draw(self):
        self.ui.draw()
