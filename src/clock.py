import pygame
from src.model.types import FontObject
from src.color import BLURPLE
import time


CLOCK_FONT = 'freemono'


def get_time() -> str:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


def declare_clock_font() -> pygame.font.FontType:
    font_for_time = pygame.font.SysFont(CLOCK_FONT, 64)
    return font_for_time


def render_simple_clock(font: pygame.font.FontType, color: str) -> pygame.SurfaceType:
    current_time = get_time()
    time_font_rect = font.render(current_time, 1, color)
    return time_font_rect

class TickingClock(FontObject):
    def __init__(self, position: list[int, int]) -> None:
        pygame.font.init()
        self.size = 32
        self.clock_font = pygame.font.SysFont(CLOCK_FONT, self.size)
        self.position = self._x, self._y = position
        self.color = BLURPLE
        self.surface = render_simple_clock(self.clock_font, self.color)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    def get_position(self) -> list[int, int]:
        return self.position
    
    def update_position(self, pos: list[int, int]) -> None:
        self.position = self._x, self._y = pos

    def get_width(self) -> int:
        return self.width
    
    def get_height(self) -> int:
        return self.height
    
    def render(self):
        self.surface = render_simple_clock(self.clock_font, self.color)
        return self.surface