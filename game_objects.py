import pygame
from config import Style, Color
from dataclasses import dataclass

Vector = pygame.Vector2
VectorZero = Vector(0, 0)
Group = pygame.sprite.Group

# Components

@dataclass
class Names():
    PLAYER = "Player"
    ENEMY = "Enemy"
    WALL = "Wall"
    
@dataclass
class Stats():
    health: int =  100
    strength: int = 1
    defense: int = 1
    speed: int = 3
    
@dataclass      
class Body():
    position: Vector = VectorZero
    size: Vector = Vector(15,15)
    color: Color = Style.STONE
    velocity: Vector = VectorZero
    
    def move(self, direction):
       self.velocity += direction * self.speed

# Game Objects

class GameObject(pygame.sprite.Sprite):
    def __init__(self, game, name, body):
        super().__init__()
        self.game = game
        self.name = name
        self.body = body
        
        self.image = pygame.Surface([body.size.x, body.size.y])
        self.image.fill(body.color)
        
        self.rect = self.image.get_rect()
        self.rect.x = body.position.x
        self.rect.y = body.position.y
        
    def change_color(self, new_color):
        self.body.color = new_color
        self.image.fill(new_color)
  
class Wall(GameObject):
    def __init__(self, game, position, size):
        super().__init__(game, Names.WALL, Body(position, size, Style.BROWN))
    
## Entities
        
class Entity(GameObject):
    def __init__(self, game, name, body = Body(), stats = Stats()):
        super().__init__(game, name, body)
        self.stats = stats

    
    def _hurt(self, amount):
        self.stats.health -= amount
        if (self.stats.health < 0):
            self._die()
            
    def _die(self):
        self.change_color(Style.BLACK)
        
    def receiveDamage(self, amount):
        self._hurt(amount)
        # TODO: Timer that has shows damage animation effect


class Enemy(Entity):
    def __init__(self, game, position):
        super().__init__(game, name = Names.ENEMY, body = Body(position = position, color = Style.RED))
        self.walls = Group()
        
    def move(self, x, y):
        body = self.body
        body.velocity.x += x
        body.velocity.y += y

    def update(self):
        self.rect.y += self.body.velocity.y
        self.rect.x += self.body.velocity.x

        targets = pygame.sprite.Group()
        targets.add(self.game.player)
        targets_hit = pygame.sprite.spritecollide(self, targets, False)
        
        for target in targets_hit:
            if target.name == Names.Player:
                # TODO: Player damage
                pass
    
        
