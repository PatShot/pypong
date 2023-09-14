from pygame import SurfaceType
from pygame.rect import RectType
from typing import Protocol
from enum import Enum, auto
from abc import ABC, abstractmethod

class GameObject(Protocol):
    position : list[float]
    velocity : list[float]
    width: int
    height: int
    rect: RectType

    def render(self) -> None:
        """Draw the Object's Rectangle to Surface"""
        ...

    def get_position(self) -> list[int]:
        ...

    def get_velocity(self) -> list[float]:
        ...

    def get_height(self) -> int:
        ...

    def get_width(self) -> int:
        ...

    def update_position(self, pos: list[float]) -> None:
        ...

    def update_velocity(self, vel: list[float]) -> None:
        ...

class FontObject(Protocol):
    position: list[int]
    size: int

    def render(self):
        """return the surface with font rendered"""

    def get_position(self) -> list[int]:
        ... 

    def update_position(self, pos: list[int]) -> None:
        ...

class Player(ABC):
    player: str
    events: list
    @abstractmethod
    def read_gamestate(self, gamestate: dict):
        '''read gamestate'''

    def player_events(self, add_event):
        '''add event to listen'''

    def rectangle(self) -> None:
        '''return rectangle to pygame'''