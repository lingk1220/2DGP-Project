from pico2d import get_events, pico2d, delay, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN

import game_framework
import play_mode
from ui import UI
from ui_pause import PauseUI


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()



def init():
    global ui
    ui = UI()
    ui_pause = PauseUI()
    ui.input_UI(ui_pause)
    pass


def update():

    delay(0.01)
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