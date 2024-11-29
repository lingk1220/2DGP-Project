



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
        r = None
        for ui in self.uis:
            print(f'uin: {ui}')
            t = ui.update()
            if t is not None:
                r = t

        return r
    def draw(self):

        for ui in self.uis:
            ui.draw()

    def input_UI(self, ui):
        self.UICOUNT += 1
        self.uis.append(ui)