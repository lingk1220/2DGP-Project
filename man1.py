import random

from pico2d import load_image

from play_mode import width, height


class Man1:
    global width, height
    image_skin = None
    image_pants = None
    image_boots = None
    image_shirts = None

    def __init__(self):
        self.width_image = 800
        self.height_image = 448
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Man1.image_skin == None:
            Man1.image_skin = load_image('Male Skin1.png')
        if Man1.image_pants == None:
            Man1.image_pants = load_image('Blue Pants.png')
        if Man1.image_shirts == None:
            Man1.image_shirts = load_image('Shirt.png')
        if Man1.image_boots == None:
            Man1.image_boots = load_image('Boots.png')

    def update(self):
        pass

    def draw(self):
        self.image_skin.clip_draw(0, 0, self.width_image, self.height_image, width // 2, height // 2)
        self.image_pants.clip_draw(0, 0, self.width_image, self.height_image, width // 2, height // 2)
        self.image_shirts.clip_draw(0, 0, self.width_image, self.height_image, width // 2, height // 2)
        self.image_boots.clip_draw(0, 0, self.width_image, self.height_image, width // 2, height // 2)
