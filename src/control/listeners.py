from src.model.events import subscribe
from src.control.gamestate import timestate

import sys

def event_time_listener(event):
    pass

def paddle_event_listener(event):
    pass

def setup_event_time_listener():
    subscribe("EVENT_START", event_time_listener)

def setup_paddle_event_listener():
    pass

def full_time_game_over(data):
    print("Time's up. Game over.")
    sys.exit(0)

def setup_full_time_listener():
    subscribe("TIME_OVER", full_time_game_over)

def setup_win_condition(fn):
    subscribe("USER_WINS", fn)

def setup_loss_condition(fn):
    subscribe("USER_LOST", fn)