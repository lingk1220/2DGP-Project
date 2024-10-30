from pico2d import *
import play_mode
import game_framework
width = 1400
height = 800

time_game = 0
image_update_tick_per = 2
open_canvas(width, height, False, False)
game_framework.run(play_mode)

# game loop
# finalization code
close_canvas()