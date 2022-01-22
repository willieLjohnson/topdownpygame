from turtle import down
import pygame
from config import Style
from game_objects import *

Vector = pygame.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.name = "Player"
        self.game = game
        self.components = {
            ComponentType.BODY: Body(Vector(x,y), Vector(10,10), Style.WHITE, 3)
        }
        self._updatesprite()
    
    def get_component(self, component_type):
        if component_type in self.components:
            return self.components[component_type]
        
    def accelerate(self, x, y):
        body = self.get_component(ComponentType.BODY)
        body.velocity.x += x * body.speed
        body.velocity.y += y * body.speed

    def move(self):
        body = self.get_component(ComponentType.BODY)
        self.rect.y += body.velocity.y
        self.rect.x += body.velocity.x

    def update(self):
        self.move()
        self._handle_gameobject_collision()
        self._handle_enemy_collision()
        self._reset_collisions()
        self._reset_velocity()
        
    def _updatesprite(self):
        body = self.get_component(ComponentType.BODY)
        self.image = pygame.Surface([body.size.x, body.size.y])
        self.image.fill(body.color)
        self.rect = pygame.Rect = self.image.get_rect()
        self.rect.x = body.position.x
        self.rect.y = body.position.y
       
        
    def _reset_velocity(self):
        self.get_component(ComponentType.BODY).velocity = Vector(0, 0)
    
    def _reset_collisions(self):
        self.get_component(ComponentType.BODY).reset_collisions()

    def _handle_enemy_collision(self):
        enemies_hit = pygame.sprite.spritecollide(self, self.game.enemies, False)

        for enemy in enemies_hit:
            print(enemy)
            enemy.receiveDamage(10)
                
    def _handle_gameobject_collision(self):
        gameobjects = self.game.get_gameobjects()
        for gameobject in gameobjects:
            collide(self, gameobject)
    