import random
from random import randint

from pico2d import load_image, get_events, clear_canvas, update_canvas
from pico2d import delay
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
import game_world
from camp import Camp
from crop import Crop
from archer import Archer
from background import Background
from character import Character
from ground import Ground
from chicken import Chicken
from maid import Maid

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


    running = True



    background = Background()
    game_world.add_object(background, 0)

    for i in range (0, 3):
        for j in range(-80, 45 + 80 + 1):
            ground = Ground(j, i)
            game_world.add_object(ground, 1)







    global character
    character = Character(width // 2, GROUNDHEIGHT)



    game_world.add_object(character, 1)

    archer = Archer(width // 2 + 100, GROUNDHEIGHT)
    game_world.add_object(archer, 2)

    global chickens
    chickens = [Chicken(400 + (randint(0, 1) * 2 - 1) * randint(0, 5) * 50, GROUNDHEIGHT) for _  in range (5)]
    for chicken in chickens:
        game_world.add_object(chicken, 2)


    maid = Maid(700, GROUNDHEIGHT)
    game_world.add_object(maid, 2)

    crop = Crop(1100, GROUNDHEIGHT)
    game_world.add_object(crop, 2)

    camp = Camp(100, GROUNDHEIGHT)
    game_world.add_object(camp, 2)


def update():
    game_world.update()
    game_world.handle_collisions()
    delay(0.01)
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    pass

def pause():
    pass

def resume():
    pass
