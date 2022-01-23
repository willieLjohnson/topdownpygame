from enum import Enum
from typing import Any
import pygame
from config import Style, Color
from dataclasses import dataclass
from core import *
import uuid

Vector = pygame.Vector2
Group = pygame.sprite.Group

PLAYER = "Player"
ENEMY = "Enemy"
WALL = "Wall"

class Direction:
    UP: float = -1.0
    DOWN: float = 1.0
    LEFT: float = -1.0
    RIGHT: float = 1.0

class ComponentType(Enum):
    ID = "ID"
    DEFAULT = "DEFAULT"
    STATS = "STATS"
    BODY = "BODY"
    
@dataclass
class Component:
    type = ComponentType.DEFAULT
    
@dataclass
class ID(Component):
    type = ComponentType.ID
    uuid: uuid.UUID
    
@dataclass
class Stats(Component):
    type = ComponentType.STATS
    
    health: int
    strength: int
    defense: int
    agility: int
    
    def change_health(self, amount):
        self.health += amount
    
    def change_strength(self, amount):
        self.strength += amount
    
    def change_defense(self, amount):
        self.defense += amount
    
    def change_agility(self, amount):
        self.agility += amount
    
@dataclass
class Body(Component):
    type = ComponentType.BODY
    
    position: Vector
    size: Vector
    color: Color
    velocity: Vector
    speed: float
    h_collision: bool = False
    v_collision: bool = False
    
    is_alive: bool = True
    
    def __init__(self, position = None, size = None, color = None, velocity = None, speed = None):
        super().__init__()
        self.position = position if position else Vector(0, 0)
        self.size = size if size else Vector(0, 0)
        self.color = color if color else Style.STONE
        self.velocity = velocity if velocity else Vector(0, 0)
        self.speed = speed if speed else 3
       
    def reset_collisions(self):
        self.h_collision = False
        self.v_collision = False

# Entities
class Entity(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.components = {ComponentType.ID: uuid.uuid1()}
        
    def set_component(self, component_type, component):
        self.components[component_type] = component
        
    def get_component(self, component_type):
        if component_type in self.components:
            return self.components[component_type]
    
    def is_alive(self):
        return self.get_component(ComponentType.BODY).is_alive
    
    def update(self):
        self._move()
        self._handle_gameobject_collision()
        self._reset_collisions()
        self._reset_velocity()
     
    def accelerate(self, x, y):
        body = self.get_component(ComponentType.BODY)
        body.velocity.x += x * body.speed
        body.velocity.y += y * body.speed
 
    def change_color(self, new_color):
        body = self.get_component(ComponentType.BODY)
        body.color = new_color
        self.image.fill(new_color)
    
    def _reset_velocity(self):
        body = self.get_component(ComponentType.BODY)
        body.velocity = Vector(0, 0)
    
    def _move(self):
        body = self.get_component(ComponentType.BODY)
        self.rect.y += body.velocity.y
        self.rect.x += body.velocity.x

    def _updatesprite(self):
        body = self.get_component(ComponentType.BODY)
        self.image = pygame.Surface([body.size.x, body.size.y])
        self.image.fill(body.color)
        self.rect = pygame.Rect = self.image.get_rect()
        self.rect.x = body.position.x
        self.rect.y = body.position.y
       
    def _handle_gameobject_collision(self):
        gameobjects = self.game.get_gameobjects()
        for gameobject in gameobjects:
            if gameobject == self:
                continue
            
            collide(self, gameobject)

    def _reset_collisions(self):
        self.get_component(ComponentType.BODY).reset_collisions()
        

## Game Objects

class GameObject(Entity):
    def __init__(self, game, name, position, size, color, speed):
        super().__init__(name)
        self.game = game
        self.name = name
        self.set_component(ComponentType.BODY, Body(position, size, color, speed=speed))
        self._updatesprite()
    
class Wall(GameObject):
    def __init__(self, game, position, size):
        super().__init__(game, WALL, position, size, Style.BROWN, 0)
    
## Actors

class Actor(GameObject):
    def __init__(self, game, name, position, size, color, speed, health, strength, defense, agility):
        super().__init__(game, name, position, size, color, speed)
        self.set_component(ComponentType.STATS, Stats(health, strength, defense, agility))
        
    def update(self):
        super().update()
        
    def _hurt(self, amount):
        self.stats.health -= amount
        if (self.stats.health < 0):
            self._die()
            
    def _die(self):
        self.change_color(Style.BLACK)
        self.is_alive = False
        
    def receiveDamage(self, amount):
        self._hurt(amount)
        # TODO: Timer that has shows damage animation effect
       

class Enemy(Actor):
    def __init__(self, game, position, size):
        super().__init__(game, ENEMY, position, size, Style.RED, 3, 100, 1, 1, 1)
        
    def update(self):
        super().update()
        targets = pygame.sprite.Group()
        targets.add(self.game.player)
        targets_hit = pygame.sprite.spritecollide(self, targets, False)
        
        for target in targets_hit:
            if target.name == PLAYER:
                # TODO: Player damage
                pass
        
def collide(gameobject, other):
    if gameobject.rect.colliderect(other.rect):
        collision_tolerance_h = gameobject.rect.h * 0.8
        collision_tolerance_w = gameobject.rect.w * 0.8
        
        gameobject_body = gameobject.get_component(ComponentType.BODY)
        other_body = other.get_component(ComponentType.BODY)
        
        # moving up
        up_difference = other.rect.bottom - gameobject.rect.top
        if abs(up_difference) < collision_tolerance_h and gameobject_body.velocity.y < 0:
            other_body.velocity.y = gameobject_body.velocity.y * 0.5
            gameobject_body.velocity.y *= -1
            gameobject.rect.y += up_difference
            gameobject_body.v_collision = True

            
        # moving down
        down_difference = other.rect.top - gameobject.rect.bottom
        if abs(down_difference) < collision_tolerance_h and gameobject_body.velocity.y > 0:
            other_body.velocity.y = gameobject_body.velocity.y * 0.5
            gameobject_body.velocity.y *= -1
            gameobject.rect.y += down_difference
            gameobject_body.v_collision = True

        # moving left
        left_difference = other.rect.right - gameobject.rect.left
        if abs(left_difference) < collision_tolerance_w and gameobject_body.velocity.x < 0:
            other_body.velocity.x = gameobject_body.velocity.x * 0.5

            gameobject_body.velocity.x *= -1
            gameobject.rect.x += left_difference
            gameobject_body.h_collision = True

        # moving right
        right_difference = other.rect.left - gameobject.rect.right
        if abs(right_difference) < collision_tolerance_w and gameobject_body.velocity.x > 0:
            other_body.velocity.x = gameobject_body.velocity.x * 0.5
            gameobject_body.velocity.x *= -1
            gameobject.rect.x += right_difference
            gameobject_body.h_collision = True