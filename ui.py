



from pico2d import load_image

from ui_info import InformationUI


class UI:

    def __init__(self):

        self.canvas_width = 1400
        self.canvas_height = 800
        self.ui_positions = [(50, self.canvas_height - 40)]

        self.UICOUNT = 0
        self.uis = []



    def get_bb(self):
        return -10000, -10000, 10000, 10000
    def update(self):

        pass

    def draw(self):

        for i in range(self.UICOUNT):
            self.uis[i].draw()

    def input_UI(self, ui):
        self.UICOUNT += 1
        self.uis.append(ui)