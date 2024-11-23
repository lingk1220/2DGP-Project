



from pico2d import load_image

from ui_info import InformationUI

UICOUNT = 1
UIPOSITION = [()]

class UI:

    images = [None] * 7
    def __init__(self):

        self.canvas_width = 1400
        self.canvas_height = 800
        self.ui_positions = [(50, self.canvas_height - 40)]

        informationui = InformationUI()


        self.uis = []

        self.uis.append(informationui)


    def get_bb(self):
        return -10000, -10000, 10000, 10000
    def update(self):

        pass

    def draw(self):

        for i in range(UICOUNT):
            self.uis[i].draw(*self.ui_positions[i])