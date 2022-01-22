from dataclasses import dataclass
from core import Color

@dataclass
class Style():
    BLACK: Color = (0, 0, 0)
    WHITE: Color = (225, 255, 255)
    BLUE: Color = (50, 50, 255)
    BROWN: Color = (139, 69, 19)
    STONE: Color = (55, 70, 70)
    RED: Color = (255, 50, 50)
    RED_FADED: Color = (125, 50, 50)


