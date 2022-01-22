from dataclasses import dataclass
import pygame
from config import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

Vector = pygame.Vector2

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

@dataclass
class Color:
    r: int = 255
    g: int = 255
    b: int = 255
    
    def rgb(self):
        return (self.r, self.g, self.b)
    
@dataclass
class Game:
    name = ""
    gameobjects = pygame.sprite.Group()
    
    def __init__(self, name):
        self.name = name
        pygame.init()
        pygame.display.set_caption(name)