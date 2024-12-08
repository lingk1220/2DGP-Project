from pico2d import get_events, pico2d, delay, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN

import game_framework
import game_world
import pause_mode
import play_mode
from archer import Archer
from ui import UI
from ui_end_game import EndingUI

from ui_pause import PauseUI
from ui_time_shift import TimeShiftUI


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
                pass

        else:
            play_mode.character.handle_event(event)


def init():
    global ui
    ui = UI()
    ui_end = None
    if play_mode.f == False:
        ui_end = EndingUI(-1)
    else:
        ui_end = EndingUI(1)

    ui.input_UI(ui_end)
    pass


def update():
    #play_mode.update()
    r= ui.update()

    if r == 1:
        if play_mode.f == True:
            game_framework.quit()
        else:
            play_mode.f = True
            game_framework.pop_mode()

        pass

def draw():
    play_mode.draw()
    ui.draw()


    pass


def finish():


    pass

def pause():
    pass

def resume():
    pass