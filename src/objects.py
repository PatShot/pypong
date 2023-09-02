import pygame
from pygame import SurfaceType
from collections import deque
from src.color import *
from src.model.types import GameObject, FontObject
from src.model.events import subscribe

COLL_THRESH = 4

class Puck(GameObject):
    def __init__(self, position: list[float], vel: list[float] = [0.0, 0.0], color: str = RED) -> None:
        self.position = self._x, self._y = position
        self.velocity = self._vx, self_vy = vel
        self.height = 5
        self.width = 5
        self.rect = pygame.Rect(self._x, self._y, self.width, self.height)
        self.color = color
    
    def get_position(self) -> list[float]:
        return self.position
    
    def get_velocity(self) -> list[float]:
        return self.velocity
    
    def get_height(self) -> int:
        return self.height
    
    def get_width(self) -> int:
        return self.width
    
    def update_position(self, pos: list[int]) -> None:
        self.position = pos

    def update_velocity(self, vel: list[float]) -> None:
        self.velocity = vel
    
    # def render(self) -> SurfaceType:
    #     self.surface.fill(self.color)
    #     return self.surface

    def render(self) -> list:
        x, y = self.position
        self.rect = pygame.Rect(x, y, self.width, self.height)
        return [self.rect, self.color]
        

class Paddle(GameObject):
    def __init__(
            self, 
            position: list[float], 
            vel: list[float] = [0.0, 0.0], 
            color: str = WHITE,
            max_history_len: int = 60
        ) -> None:
        self.position= self._x, self._y = position
        self.velocity = self._vx, self_vy = vel
        self.history_pos : deque = deque(maxlen=max_history_len//2)
        self.step = 10
        self.height = 15
        self.width = 80
        self.surface = pygame.Surface((self.width+1, self.height+1))
        self.rect = pygame.Rect(self._x, self._y, self.width, self.height)
        self.color = color
        self.event_binder = [
            subscribe("KEY_LEFT", self.handle_key_left),
            subscribe("KEY_RIGHT", self.handle_key_right),
            ]
    
    def get_position(self) -> list[float]:
        return self.position
    
    def get_velocity(self) -> list[float]:
        return self.velocity
    
    def get_height(self) -> int:
        return self.height
    
    def get_width(self) -> int:
        return self.width
    
    def update_position(self, pos: list[float]) -> None:
        self.position = pos

    def update_velocity(self, vel: list[float]) -> None:
        self.velocity = vel

    def update_width(self, new_width: int) -> None:
        self.width = new_width

    # DANGER -> These have hardcoded widths.
    # Change before resize addition.
    def handle_key_left(self, data):
        # print(f"LISTEN: KEY LEFT")
        if self.rect.left - 0 > COLL_THRESH:
            self.move_left(step = self.step)

    def handle_key_right(self, data):
        # print(f"LISTEN: KEY RIGHT")
        if 480 - self.rect.right  > COLL_THRESH:
            self.move_right(step= self.step)

    def move_right(self, step:int =10) -> None:
        x, y = self.position
        self.position = [x+step, y]

    def move_left(self, step: int =10) -> None:
        x, y = self.position
        self.position = [x - step, y]

    def record_pos(self) -> None:
        self.history_pos.append(self.position)

    def calc_pseudo_vel(self) -> list[float]:
        pseudo_vx = self.history_pos[-1][0] - self.history_pos[0][0]
        pseudo_vy = self.history_pos[-1][1] - self.history_pos[-1][0]
        return [pseudo_vx/self.history_pos.maxlen, pseudo_vy/self.history_pos.maxlen]
    
    def render(self) -> list:
        x, y = self.position
        self.rect = pygame.Rect(x, y, self.width, self.height)
        return [self.rect, self.color]
    

class TextDisplay(FontObject):
    def __init__(
            self,
            text_fn, 
            position: list[int],
            size: int = 32
            ) -> None:
        pygame.font.init()
        self.text_fn = text_fn
        self.size = size
        self.TEXT_FONT = 'freemono'
        self.font_object = pygame.font.SysFont(self.TEXT_FONT, self.size)
        self.position = self._x, self._y = position
        self.color = BLURPLE
        self.init_text = self.text_fn()
        self.surface = self.font_object.render(self.init_text, 1, self.color)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    def get_position(self) -> list[int]:
        return self.position
    
    def update_position(self, pos: list[int]) -> None:
        self.position = self._x, self._y = pos

    def get_width(self) -> int:
        return self.width
    
    def get_height(self) -> int:
        return self.height
    
    def render(self):
        text = self.text_fn()
        return self.font_object.render(text, 1, self.color)