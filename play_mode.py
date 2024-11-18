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
from skeleton import Skeleton

GROUNDHEIGHT = 120
width = 1400
height = 800





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

    global character
    character = Character(0, GROUNDHEIGHT)



    game_world.add_object(character, 4)

    background = Background()
    game_world.add_object(background, 0)

    for i in range (0, 3):
        for j in range(-80, 45 + 80 + 1):
            ground = Ground(j, i)
            game_world.add_object(ground, 1)









    archer = Archer(-500, GROUNDHEIGHT)
    game_world.add_object(archer, 3)

    global chickens
    chickens = [Chicken(400 + (randint(0, 1) * 2 - 1) * randint(0, 5) * 50, GROUNDHEIGHT) for _  in range (1)]
    for chicken in chickens:
        game_world.add_object(chicken, 3)


    maid = Maid(700, GROUNDHEIGHT)
    game_world.add_object(maid, 3)

    crop = Crop(1100, GROUNDHEIGHT)
    game_world.add_object(crop, 3)

    camp = Camp(500, GROUNDHEIGHT)
    game_world.add_object(camp, 2)

    skeleton = Skeleton(-700, GROUNDHEIGHT)
    game_world.add_object(skeleton, 3)

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
