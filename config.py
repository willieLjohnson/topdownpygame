from dataclasses import dataclass

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

@dataclass
class Color():
    r: int
    g: int
    b: int
    
    def rgb(self):
        return (self.r, self.g, self.b)
    
@dataclass      
class Style():
    BLACK: Color = (0, 0, 0)
    WHITE: Color = (225, 255, 255)
    BLUE: Color = (50, 50, 255)
    BROWN: Color = (139, 69, 19)
    STONE: Color = (55, 70, 70)
    RED: Color = (255, 50, 50)
    RED_FADED: Color = (125, 50, 50)


