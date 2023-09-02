import pygame
from dataclasses import dataclass
import math
from src.objects import Paddle, Puck
from src.settings import HEIGHT, WIDTH, TOP_BOUND
from .events import post_event
from .types import GameObject

def kinetic_energy(vel: float, mass: float = 1.0):
    return 0.5*mass*vel*vel

def vector_inner_product(vector: list[float]):
    return math.sqrt(sum([x*x for x in vector]))

def kinetic_energy_vectors(vel: list[float], mass: float = 1.0):
    return kinetic_energy(vector_inner_product(vel))

def border_collide(object: GameObject) -> list[float]:
    '''Returns: [new_position, new_velocity]'''
    vx, vy = object.get_velocity()
    new_vx, new_vy = vx, vy
    cen_x, cen_y = object.rect.center
    if cen_y < TOP_BOUND:
        post_event("UP_SCORE", "USER")
        new_vy = -vy
    if cen_x > WIDTH-2 or cen_x < 2:
        new_vx = -vx
    return [new_vx, new_vy]

# Test helper function
def warp_to_top(obj: GameObject):
    # old_x, old_y = obj.get_position()
    # if old_y > HEIGHT:
    #     post_event("UP_SCORE", "CPU")
    #     # return [old_x, int(0.21*HEIGHT)]
    # return [old_x, old_y]
    pass

def move_object(obj: GameObject, t: int = 1) -> list[float]:
    '''Move Rect position by t intervals'''
    x, y = obj.get_position()
    vx, vy = obj.get_velocity()
    new_x = x + vx*t
    new_y = y + vy*t
    new_pos = [new_x, new_y]
    # print(a.get_position(), vx, vy, t, new_x, new_y)
    return new_pos

def accelerate_object(
        obj: GameObject, 
        a: list[float] = [0.0, 0.0],
        t: int = 1
    ) -> list[float]:
    '''Returns velocity after acceleration'''
    vx, vy = obj.get_velocity()
    ax, ay = a
    new_vx = vx + ax*t
    new_vy = vy + ay*t
    return [new_vx, new_vy]


def signs_flipped(A, B):
    if len(A) != len(B):
        raise ValueError("Input lists must have the same length")

    for a, b in zip(A, B):
        if (a < 0 and b >= 0) or (a >= 0 and b < 0):
            return True

    return False

# def detect_collisions(a: GameObject, b: GameObject) -> bool:
#     if abs(x_a - x_b) < 25 and abs(y_a - y_b) < 25:
#         return True
#     else:
#         return False
    
def handle_collisions(ball: GameObject, paddle: Paddle, ALPHA: float = 1.000) -> list[float]:
    vx, vy = ball.get_velocity()
    old_vx, old_vy = vx, vy
    vy = -1*ALPHA*vy
    assert ALPHA != 0

    try:
        pseudo_vel, _ = paddle.calc_pseudo_vel()
    except AttributeError as e:
        raise AttributeError(f"{e} not found. CHECK if `handle_collisions` is calling (Ball, Paddle) in right order.")
    try:
        sign_pad_v = pseudo_vel / abs(pseudo_vel)
    except ZeroDivisionError:
        sign_pad_v = 1
    
    ball_pos_x, _ = ball.get_position()
    pad_mid_x, _ = paddle.rect.midtop
    pad_half_w = paddle.rect.w / 2
    hit_pos_x = ball_pos_x - pad_mid_x

    # if sign_pad_v*hit_pos_x < :
    #     MAX_K = (hit_pos_x/pad_half_w)
    MAX_K = (hit_pos_x/pad_half_w)*sign_pad_v*0.5

    vx = (vx + MAX_K*pseudo_vel)*(1/ALPHA)
    
    print(f"pos hit: {hit_pos_x}, K: {MAX_K}, pseudo_vel: {pseudo_vel}")
    print(f"Original_X_vel: {old_vx} Ending X_vel: {vx}")
    return [vx, vy]