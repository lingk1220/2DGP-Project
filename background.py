from pico2d import load_image

import play_mode


class Background:

    images_day = [None] * 4
    images_night = [None] * 4

    def __init__(self):
        self.width_image = 576
        self.height_image = 324
        self.draw_x = 0
        self.draw_y = -400
        for i in range(0, 4):
            if Background.images_day[i] == None:
                name = './background/' + 'sky_day' + (str)(i+1) + '.png'
                Background.images_day[i] = load_image(name)

            if Background.images_night[i] == None:
                name = './background/' + 'sky_night' + (str)(i + 1) + '.png'
                Background.images_night[i] = load_image(name)


    def get_bb(self):
        return -10000, -10000, 10000, 10000
    def update(self):

        pass

    def draw(self):
        if play_mode.game_world.is_day:
            for i in range(0,4):
                self.images_day[i].clip_draw_to_origin(int(self.draw_x) , int(self.draw_y) - 400,  2304, 1296, -int(play_mode.character.pos_x / 50 * i) - 300, -200)

        else:
            for i in range(0, 4):
                self.images_night[i].clip_draw_to_origin(int(self.draw_x), int(self.draw_y) - 400, 2304, 1296, -int(play_mode.character.pos_x / 50 * i) - 300, -200)
