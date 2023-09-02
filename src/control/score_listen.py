from ..model.events import subscribe
from ..model.types import Events

# Scores
def handle_score_events(cur_score: dict, player_scored: str):
    cur_score[player_scored] += 1
    return cur_score

def setup_score_handler():
    subscribe(Events.SCORED, handle_score_events)

