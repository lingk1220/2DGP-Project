from pico2d import draw_rectangle

import play_mode

collision_pairs = {}


objects = [[], [], [], [], []]


UI = [[], [], []]

def add_object(o, depth = 0):
    objects[depth].append(o)

def add_UI(o, depth = 0):
    objects[depth].append(o)


def update():
    for layer in objects:
        for o in layer:
            o.update()

    for layer in UI:
        for o in layer:
            o.update()

def render():
    for layer in objects:
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