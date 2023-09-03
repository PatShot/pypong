import math
from random import random
from src.objects import Puck, Paddle, TextDisplay
from src.clock import TickingClock
from src.model.events import post_event, subscribe
from src.model.types import GameObject, FontObject
from src.control.listeners import setup_full_time_listener
from src.ai.simple_ai import simple_ai
from src.model.phys import (
    kinetic_energy,
    vector_inner_product,
    kinetic_energy_vectors,
    move_object,
    signs_flipped, 
    border_collide, 
    handle_collisions,
    warp_to_top
)
from src.control.gamestate import fresh_gamestate, timestate
from src.settings import TOP_BOUND, BOTTOM_BOUND, SMASH_ACTIVE
from src.settings import CPU_PADDLE_START, USER_PADDLE_START
import pygame

CLOCK_POS = [60, 80]
BOUNCE_POS = [380, 80]
SHOW_VEL_POS = [270, 80]
KINETIC_ENERGY = [60, 20]

PUCK_POS = [220.0, 300.0]
PUCK_VEL = [round(random()*1.5, 2), 3.0]

def dummy_handler_event(data):
    print(f"Event being called, with data:{data}")


class Game():
    def __init__(
            self, 
            canvas_size: tuple[int, int],
            FPS: int = 60
            ) -> None:
        self.ball_objects: list[GameObject] = []
        self.font_objects: list[FontObject] = []
        self.control_objects: list[GameObject] = []
        self.user_object: Paddle = None
        self.cpu_object: Paddle = None
        self.canvas_x, self.canvas_y = canvas_size
        print(f"Screen size: {self.canvas_x} x {self.canvas_y}")
        self.bounce_num: int = 0
        self.FPS: int = FPS
        self.smash_active = SMASH_ACTIVE*self.FPS
        self.game_state: dict = fresh_gamestate
        self.max_time: int = 180000
        self.time: int = 0
        setup_full_time_listener()

    def register_object(self, object: GameObject) -> None:
        self.ball_objects.append(object)

    def untrack_object(self, object: GameObject) -> None:
        self.ball_objects.remove(object)

    def register_font(self, object: FontObject) -> None:
        self.font_objects.append(object)

    def untrack_font(self, object: FontObject) -> None:
        self.font_objects.remove(object)

    def register_user_object(self, object: Paddle) -> None:
        self.user_object = object
        self.control_objects.append(object)

    def untrack_user_object(self, object: Paddle) -> None:
        self.user_object = None
        self.control_objects.remove(object)

    def register_cpu_object(self, object: Paddle) -> None:
        self.cpu_object = object
        self.control_objects.append(object)

    def untrack_cpu_object(self, object: Paddle) -> None:
        self.cpu_object = None
        self.control_objects.remove(object)

    def check_time(self) -> None:
        self.time += 1
        if self.time > self.max_time:
            post_event("TIME_OVER", self.time)

    def check_if_score(self, ball: GameObject):
        _, y = ball.get_position()
        if y >= BOTTOM_BOUND:
            post_event("UP_SCORE", "CPU")
        if y < TOP_BOUND:
            post_event("UP_SCORE", "USER")

    def update_score(self, player):
        print(player)
        self.game_state[player]['score'] += 1

    def get_score(self, player):
        return self.game_state[player]['score']

    def declare_objects(self):
        # clk = TickingClock(CLOCK_POS)
        # self.register_font(clk)
        score_text = TextDisplay(text_fn=self.show_score, position=BOUNCE_POS, size=28)
        self.register_font(score_text)
        puck_speed = TextDisplay(text_fn=self.show_puck_speed, position=CLOCK_POS, size = 16)
        self.register_font(puck_speed)
        puck_ener  = TextDisplay(text_fn=self.show_kinetic_ener, position=KINETIC_ENERGY, size=16)
        self.register_font(puck_ener)

        # For testing Only
        # PUCK_POS = [
        #     (0.21*self.canvas_x + random()*0.56*self.canvas_x),
        #     (0.21*self.canvas_y + random()*0.57*self.canvas_y)]
        PUCK_VEL = [round(random()*1.5, 2), 3.0]
        puck = Puck(PUCK_POS, PUCK_VEL)
        self.register_object(puck)

        # For testing Only
        # PAD1_POS = [
        #     (self.canvas_x//2  - 25),
        #     0.95*self.canvas_y
        # ]
        paddle1 = Paddle(USER_PADDLE_START, max_history_len=self.FPS)
        self.register_user_object(paddle1)
        paddle2 = Paddle(CPU_PADDLE_START, max_history_len=self.FPS)
        self.register_cpu_object(paddle2)
        self.user_events()
        self.cpu_events()
        self.gamestate_events()

    def reset_game(self):
        for ball_obj in self.ball_objects:
            print(f"Puck currently at -> {ball_obj.get_position()}")
            ball_obj.update_position(PUCK_POS)
            ball_obj.update_velocity(PUCK_VEL)
        self.user_object.update_position(USER_PADDLE_START)
        self.cpu_object.update_position(CPU_PADDLE_START)
        self.time = 0
        post_event("RESET_DONE", 2000)

    def handle_reset(self, data):
        print(f"resetting for {data}")
        self.reset_game()
    
    def check_events(self):
        if self.game_state['USER']['smash_flag'] and (self.time >= self.game_state['USER']['smash_active']):
            self.game_state['USER']['smash_flag'] = False
            self.game_state['USER']['alpha'] = 1.00
            print("Deactivated Smash state.")
        if self.game_state['CPU']['smash_flag'] and (self.time >= self.game_state['CPU']['smash_active']):
            self.game_state['CPU']['smash_flag'] = False
            self.game_state['CPU']['alpha'] = 1.00
            print("Deactivated Smash state.")
    
    def update_positions(self):
        self.time += 1
        if self.time < self.FPS*2:
            return
        self.check_events()
        if not self.ball_objects:
            return
        
        if self.time %10 == 0:
            obs_gstate = self.push_ai_gamestate()
            simple_ai(gamestate=obs_gstate)
        # Maybe, I'll have multiple balls.
        # Who knows?
        for ball_object in self.ball_objects:
            updated_vel = border_collide(ball_object)
            # print(updated_vel)
            ball_object.update_velocity(updated_vel)

            updated_pos = move_object(ball_object)    
            ball_object.update_position(updated_pos)

            self.check_if_score(ball_object)
            # updated_pos = warp_to_top(ball_object)
            # ball_object.update_position(updated_pos)

            if self.user_object:
                self.ball_ctrl_object_collision(ball_object, self.user_object, 'USER')
            if self.cpu_object:
                self.ball_ctrl_object_collision(ball_object, self.cpu_object, 'CPU')
            # Detect bounces
            new_vel = ball_object.get_velocity()
            self.find_puck_speed(new_vel)
           
    def get_bounces(self):
        return str(self.bounce_num)
    
    def show_score(self):
        user_score = self.get_score('USER')
        cpu_score = self.get_score('CPU')
        return f"{user_score} - {cpu_score}"

    def find_puck_speed(self, vel: list[float]):
        vx = vel[0],
        vy = vel[1],
        self.game_state['ball_vx'] = abs(vx[0])
        self.game_state['ball_vy'] = abs(vy[0])
        self.game_state['ball_velocity'] = abs(math.sqrt(sum([x**2 for x in vel])))
 
    def show_puck_speed(self):
        vel = self.game_state['ball_velocity']
        vx = self.game_state['ball_vx']
        vy = self.game_state['ball_vy']
        return f"{vx:.2f}x + {vy:.2f}y = {vel:.2f}"
    
    def show_kinetic_ener(self):
        
        vx = self.game_state['ball_vx']
        vy = self.game_state['ball_vy']
        return f"{kinetic_energy_vectors(vel = [vx, vy]):.2f}"
    
    def ball_ctrl_object_collision(self, ball_object:GameObject, ctrl_object: Paddle, player: str, Thresh: int = 9):
        ctrl_object.record_pos()
        if 0.35*self.canvas_y < ball_object.position[1] < 0.8 * self.canvas_y:
            return
        if not ctrl_object.rect.colliderect(ball_object.rect):
            return
        val_diff = ctrl_object.rect.top - ball_object.rect.bottom
        if val_diff > Thresh:
            return
        ALPHA = self.game_state[player]['alpha']
        v_after_coll = handle_collisions(ball=ball_object, paddle=ctrl_object, ALPHA=ALPHA)
        ball_object.update_velocity(v_after_coll)
        new_pos = move_object(ball_object, 3)
        ball_object.update_position(new_pos)
        post_event("PADDLE_HIT", player)

    def push_ai_gamestate(self) -> dict:
        obs_gamestate = {
            "self": {
                "center": self.cpu_object.rect.center,
                "position": self.cpu_object.get_position(),
                "width": 80
            },
            "puck": {
                "position": self.ball_objects[0].get_position(),
                "velocity": self.ball_objects[0].get_velocity()
            },
            "smash": {
                "avail": False
            }
        }
       
        # if self.time % 200 > 90:
        #     obs_gamestate["smash"]['avail'] = True
        return obs_gamestate
    
    def win_condition(self, data):
        user_score = self.game_state['USER']['score']
        cpu_score = self.game_state['CPU']['score']
        if user_score == 11:
            post_event("USER_WINS", "")
        if cpu_score == 11:
            post_event("USER_LOST", "")
    
    def usr_smash_handler(self, player):
        if self.game_state[player]["smash_flag"]:
           return
        print(f"Activating {player} SMASH state")
        self.game_state[player]["smash_flag"] = True
        self.game_state[player]["smash_active"] = self.time + self.smash_active
        self.game_state[player]["alpha"]= 1.15
                
    
    def user_events(self):
        subscribe("PLYR_LEFT", self.user_object.handle_key_left)
        subscribe("PLYR_RIGHT", self.user_object.handle_key_right)
        subscribe("PLYR_SPACE", self.usr_smash_handler)

    def cpu_events(self):
        subscribe("CPUR_LEFT", self.cpu_object.handle_key_left)
        subscribe("CPUR_RIGHT", self.cpu_object.handle_key_right)
        subscribe("CPUR_SPACE", self.usr_smash_handler)

    def gamestate_events(self):
        subscribe("UP_SCORE", self.update_score)
        subscribe("UP_SCORE", self.handle_reset)
        subscribe("RESET_DONE", self.win_condition)
    
    def handle_key_event(self, keys: dict):
        if keys[pygame.K_LEFT]:
            post_event("PLYR_LEFT", "")
        if keys[pygame.K_RIGHT]:
            post_event("PLYR_RIGHT", "")
        if keys[pygame.K_SPACE]:
            post_event("PLYR_SPACE", "USER")

    