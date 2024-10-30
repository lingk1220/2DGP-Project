from pico2d import *

import play_mode
width = 1400
height = 800

time_game = 0
image_update_tick_per = 2
open_canvas(width, height, False, False)
play_mode.reset_world()
# game loop
while play_mode.running:
    play_mode.handle_events()
    play_mode.update_world()
    play_mode.render_world()
    time_game += 1
    delay(0.02)
# finalization code
close_canvas()