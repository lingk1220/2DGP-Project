from random import randint

from pico2d import load_image

import game_framework
import pause_mode
import play_mode


class House:
    image = None
    def __init__(self,map, dir = 1, x = 0, y = 0):
        self.width_image = 1184
        self.height_image = 768

        self.map = map
        self.count_h = 1
        self.count_v = 1

        self.x_index = x

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = 7 - 1
        self.index_v = 29 - 1

        self.dir = dir
        self.draw_dir = 1
        self.pos_x = 0
        self.pos_y = y + 116

        self.tiles_h = 3
        self.tiles_v = 2

        self.hp = 50

        self.is_dying = 0

        self.draw_x = self.size_h * self.tiles_h * 1.5
        self.draw_y = self.size_v * self.tiles_v * 1.5

        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        play_mode.game_world.add_collision_pair('enemy:ally', None, self)

        if House.image == None:
            House.image = load_image('house.png')

    def get_bb(self):
        return self.pos_x - 288 * 1.6  / 3, self.pos_y - 190 * 1.6  / 2, self.pos_x + 288 * 1.6  / 2.2, self.pos_y + 190 * 1.6  / 2.7

    def attacked(self, other):
        self.hp -= 1
        if self.hp <= 0:
            self.is_dying = 1
            game_framework.push_mode(pause_mode)


    def handle_collision(self, group, other):
        if group == '':
            pass

    def update(self):
        pass

    def draw(self):
        if abs(play_mode.character.pos_x - self.pos_x) > 1000:
            return
        self.clip_pos_x = 700 - play_mode.character.pos_x + self.pos_x
        self.clip_pos_y = self.pos_y

        if self.draw_dir > 0:
            self.image.clip_composite_draw(900,
                                            348,
                                            288,
                                            190,
                                            0,
                                            'h',
                                            self.clip_pos_x,
                                            self.clip_pos_y,
                                            288 * 1.6, 190 * 1.6
                                            )

        else:
            self.image.clip_composite_draw(self.index_h * self.size_h,
                                            self.index_v * self.size_v,
                                            self.size_h * self.tiles_h,
                                            self.size_v * self.tiles_v,
                                            0,
                                            'h',
                                            self.clip_pos_x,
                                            self.clip_pos_y,
                                            self.draw_x, self.draw_y
                                            )


    def interact(self):
        print('Interact With Rock')
        self.map.build_walls(self.dir, self.x_index + 1)
