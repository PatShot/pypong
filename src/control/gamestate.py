fresh_gamestate = {
    "USER" : {
        "score" : 0,
        "smash_flag" : False,
        "smash_active" : 0,
        "alpha": 1.00,
        "position": []
    },
    "CPU" : { 
        "score" : 0,
        "smash_flag" : False,
        "smash_active": 0,
        "alpha": 1.00,
        "position": []
    },
    "ball_vx": 0.0,
    "ball_vy": 0.0,
    "ball_velocity": 0.0,
    "last_paddle_hit": None
}

timestate = {
    "time_flag": False,
    "time": 0,
    "time_count": 0
}

# Change the way the gamestate is constructed.
# There has to be a way of building the gamestate
# with discrete components, as I want to switch
# between two game modes : One with Single Paddle,
# And then the standard PONG.

gamestate = {
    "BALL" : {
        "x": 0,
        "y": 0,
        "vx": 0,
        "vy": 0
    }
} 