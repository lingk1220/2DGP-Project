import time

from pico2d import clear_canvas, update_canvas

global frame_time
frame_time = 0.0

def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time
    frame_time = 0.0

    current_time = time.time()

    while running:
        stack[-1].handle_events()
        stack[-1].update()

        clear_canvas()
        stack[-1].draw()
        update_canvas()

        frame_time = time.time() - current_time
        frame_rate = 1.0 / frame_time
        current_time += frame_time

    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()


def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()

def pop_mode():
    global stack
    if (len(stack) > 0):
    # execute the current mode's finish function
        stack[-1].finish()
    # remove the current mode
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()

def quit():
    global running

    running = False