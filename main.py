from pico2d import *
import random

class Props:
    global width, height
    image = None
    def __init__(self):
        self.x, self.y = random.randint(0, 0), 90
        self.draw_x = 0
        self.draw_y = 0
        if Props.image == None:
            Props.image = load_image('Props.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 1024, 1024, width // 2, height // 2)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global running

    global world

    running = True
    world = []

    prop = Props()
    world.append(prop)

def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

width = 1000
height = 800

open_canvas(width, height, False, False)
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)
# finalization code
close_canvas()