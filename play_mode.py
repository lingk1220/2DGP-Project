import random

from pico2d import load_image, get_events, clear_canvas, update_canvas
from pico2d import delay
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
from archer import Archer
from background import Background
from character import Character
from ground import Ground
from rabbit import Rabbit

GROUNDHEIGHT = 120
width = 1400
height = 800


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


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            character.handle_event(event)


def init():
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
    character = Character(width // 2, GROUNDHEIGHT)



    world.append(character)

    archer = Archer(width // 2 + 100, GROUNDHEIGHT)
    world.append(archer)
    global rabbits
    rabbits = [Rabbit(100, GROUNDHEIGHT) for _  in range (1)]
    for rabbit in rabbits:
        world.append(rabbit)


def update():
    global world
    for o in world:
        o.update()

    delay(0.01)
    pass


def draw():
    global world
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


def finish():
    pass

def pause():
    pass

def resume():
    pass
