from src.model.events import post_event

empty_gamestate = {
    "self": {
        "center": [],
        "position": [],
        "width": 80
    },
    "puck": {
        "position": [],
        "velocity": []
    },
    "smash": {
        "avail": False
    }
}

def simple_ai(gamestate:dict):
    '''
    Simple AI that follows position
    and smashes every few seconds.
    '''
    current_puck_pos_x, _ = gamestate["puck"]['position']
    self_cen_x, _ = gamestate['self']['center']

    if current_puck_pos_x > self_cen_x:
        post_event("CPUR_RIGHT", "")
    elif current_puck_pos_x < self_cen_x:
        post_event("CPUR_LEFT", "")
    
    if gamestate['smash']['avail']:
        post_event("CPUR_SPACE", "CPU")
