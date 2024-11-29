
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_LSHIFT, SDLK_e

SHIFT_PRESSED = 2

def start_event(e):
    return e[0] == 'START'

def space_down(e): # e가 space down인지 판단 >> True or False
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def lshift_down(e): # e가 space down인지 판단 >> True or False
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

def lshift_up(e): # e가 space down인지 판단 >> True or False
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LSHIFT

def time_out_interact(e):
    return e[0] == 'TIME_OUT' and e[1] == 0

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_down_with_shift(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT and e[SHIFT_PRESSED] == 1


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def right_up_with_shift(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT and e[SHIFT_PRESSED] == 1


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_down_with_shift(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT and e[SHIFT_PRESSED] == 1

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def left_up_with_shift(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT and e[SHIFT_PRESSED] == 1

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def interact_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e

def interact_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_e

def run_shift(e):
    return e[0] == 'SHIFT' and e[1] == 'RUN'

def idle_shift(e):
    return e[0] == 'SHIFT' and e[1] == 'IDLE'

def change_mode_play(e):
    return e[0] == 'CHANGE MODE' and e[1] == 'PLAY'


class StateMachine:
    def __init__(self, obj):
        self.obj = obj # 어떤 객체의 상태 머신인지를 설정
        self.event_q = [] #상태 이벤트 보관할 리스트
        pass

    def start(self, state):
        self.cur_state = state # 시작 상태를 받아서, 그걸로 현재 상태를 정의
        self.cur_state.enter(self.obj, ('START', 0))
        print(f'Enter into {state}')
        pass

    def update(self):
        self.cur_state.do(self.obj)
        # 혹시 이벤트가 있나
        if self.event_q: # list는 멤버가 있으면 True
            e = self.event_q.pop(0)
            #이 시점에서 주어진 정보
            #e
            #cur_state
            #현재 상태와 현재 발생한 이벤트에 따라서
            #다음 상태를 결정
            #상태 변환 테이블 이용.

            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    print(f'Exit from {self.cur_state}')
                    self.cur_state.exit(self.obj, e)
                    self.cur_state = next_state
                    print(f'Enter into {next_state}')
                    self.cur_state.enter(self.obj, e) #상태 변환 이유를 명확히 알려줌
                    return
            # 이 시점으로 왔다는 것은 event에 따른 전환 실패
            print(f'        WARNING: {e} not handled at state {self.cur_state}')
        pass

    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def add_event(self, e):
        print(f'    DEBUG: add event{e}')
        self.event_q.append(e)
        pass

    def clear_event(self):
        t = self.event_q[0]
        self.event_q.clear()
        self.event_q.append(t)

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass