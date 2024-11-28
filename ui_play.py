



from pico2d import load_image

from ui import UI
from ui_info import InformationUI


class PlayUI:

    def __init__(self):
        self.ui = UI()
        self.canvas_width = 1400
        self.canvas_height = 800
        self.ui_positions = [(50, self.canvas_height - 40)]

        self.informationui = InformationUI(50, self.canvas_height - 40)
        self.ui.input_UI(self.informationui)


    def get_bb(self):
        return -10000, -10000, 10000, 10000
    def update(self):
        self.informationui.update()
        pass

    def draw(self):
        self.ui.draw()

