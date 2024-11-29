from pico2d import draw_rectangle

import game_framework
import play_mode
import time_shift_mode
from map import Map

collision_pairs = {}

map = None

objects = [[], [], [], [], []]


UI = [[], [], []]

time = 30.0
is_day = True

def add_object(o, depth = 0):
    objects[depth].append(o)

def add_UI(o,depth = 0):
    UI[depth].append(o)

def add_map(o):
    global map
    map = o

def update():

    for layer in objects:
        for o in layer:
            o.update()

    map.update()

    for layer in UI:
        for o in layer:
            o.update()

    update_time()


def render():
    for index, layer in enumerate(objects):
        if(index == 2):
            map.draw()
        for o in layer:

            o.draw()

    for layer in UI:
        for o in layer:
            o.draw()

    i = 0
    for layer in objects:
        if 0 < i and i  <= 4:
            for o in layer:
                l, b, r, t = o.get_bb()
                l = 700 - play_mode.character.pos_x + l
                r = 700 - play_mode.character.pos_x + r
                draw_rectangle(l, b, r, t)
                pass
        i += 1

    map.draw_bb()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True



def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return

    raise ValueError('Cannot delete non existing object')

def update_time():
    global time, is_day
    time += game_framework.frame_time
    if time > 10:
        is_day = False
        game_framework.push_mode(time_shift_mode)
        if time > 20:
            time = 0
            is_day = True
            game_framework.push_mode(time_shift_mode)
