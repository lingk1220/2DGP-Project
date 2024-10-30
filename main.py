from pico2d import *
import play_mode
import game_framework
width = 1400
height = 800

time_game = 0
open_canvas(width, height, True, False)
game_framework.run(play_mode)

# game loop
# finalization code
close_canvas()
delay(0.1)