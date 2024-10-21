from pico2d import *
import random

from background import Background
from character import Character
from ground import Ground


class Props:
    global width, height
    image = None
    def __init__(self):
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Props.image == None:
            Props.image = load_image('Props.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 1024, 1024, width // 2, height // 2 - 100)

class Props2:
    global width, height
    image = None
    def __init__(self):
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Props2.image == None:
            Props2.image = load_image('Props2.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 1024, 1024, width // 2, height // 2 - 100)

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


class Archer:
    global width, height
    image = None
    def __init__(self, x, y):
        self.width_image = 704
        self.height_image = 320

        self.count_h = 11
        self.count_v = 5

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = x
        self.index_v = y
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Archer.image == None:
            Archer.image = load_image('Archer.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.index_h * self.size_h,
                             self.index_v * self.size_v,
                             self.size_h,
                             self.size_v,
                             self.size_h * self.index_h + width // 2,
                             self.size_v * self.index_v + height // 2, 96, 96)


class Skeleton:
    global width, height
    image = None
    def __init__(self, x, y):
        self.width_image = 600
        self.height_image = 150

        self.count_h = 4
        self.count_v = 1

        self.size_h = (self.width_image // self.count_h)
        self.size_v = (self.height_image // self.count_v)

        self.index_h = x
        self.index_v = y
        self.x, self.y = random.randint(0, 0), 0
        self.draw_x = 0
        self.draw_y = 0
        if Skeleton.image == None:
            Skeleton.image = load_image('Skeleton_Idle.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.index_h * self.size_h + 60,
                             self.index_v * self.size_v + 30,
                             self.size_h - 100,
                             self.size_v - 60,
                             self.size_h * self.index_h + width // 2 + 128,
                             self.size_v * self.index_v + height // 2, 100, 180)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            character.handle_event(event)


def reset_world():
    global running

    global world

    running = True
    world = []

    prop = Props()

    #world.append(prop)

    background = Background()
    world.append(background)

    for i in range (0, 3 + 1):
        for j in range(-80, 45 + 80 + 1):
            ground = Ground(j, i)
            world.append(ground)



    prop2 = Props2()

    #world.append(prop2)




    global character
    character = Character(width // 2, 123)



    world.append(character)




def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


width = 1400
height = 800

time_game = 0
image_update_tick_per = 2
open_canvas(width, height, False, False)
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    time_game += 1
    delay(0.02)
# finalization code
close_canvas()