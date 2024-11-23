
from pico2d import load_image

from ui import UI
from ui_menubox import MenuboxUI


class PauseUI:

    def __init__(self):
        self.ui = UI()
        self.canvas_width = 1400
        self.canvas_height = 800
        self.ui_positions = [(50, self.canvas_height - 40)]

        menuboxui = MenuboxUI(400, 700)
        self.ui.input_UI(menuboxui)


    def get_bb(self):
        return -10000, -10000, 10000, 10000
    def update(self):

        pass

    def draw(self):
        self.ui.draw()
