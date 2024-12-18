from pico2d import get_events, pico2d, delay, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN

import game_framework
import game_world
import pause_mode
import play_mode
from archer import Archer
from ui import UI
from ui_pause import PauseUI
from ui_time_shift import TimeShiftUI


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
                game_framework.push_mode(pause_mode)

        else:
            play_mode.character.handle_event(event)


def init():
    global ui
    ui = UI()
    ui_timeshift = TimeShiftUI()
    ui.input_UI(ui_timeshift)
    pass


def update():
    play_mode.update()
    r= ui.update()

    if r == 1:
        game_framework.pop_mode()

    if r == 2:
        game_world.is_day = not game_world.is_day
        if game_world.is_day == True:
            for o in game_world.objects[3]:
                if o.__class__ == Archer:
                    o.set_day()
        pass

def draw():
    play_mode.draw()
    ui.draw()


    pass


def finish():
    game_world.is_shifted = False

    pass

def pause():
    pass

def resume():
    pass