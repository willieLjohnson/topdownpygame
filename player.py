from turtle import down
import pygame
from config import Style
from game_objects import *

Vector = pygame.Vector2

class Player(Entity):
    def __init__(self, game, x, y):
        super().__init__(PLAYER)
        self.game = game
        self.set_component(ComponentType.BODY, Body(Vector(x, y), Vector(10,10), Style.WHITE, Vector(0,0), 3))
        self._updatesprite()
    
    def update(self):
        super().update()
        self._handle_enemy_collision()
        
    def _handle_enemy_collision(self):
        enemies_hit = pygame.sprite.spritecollide(self, self.game.enemies, False)

        for enemy in enemies_hit:
            print(enemy)
            enemy.receiveDamage(10)
    