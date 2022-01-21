import pygame
from config import Style

Vector = pygame.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        
        self.game = game
        
        self.image = pygame.Surface([15, 15])
        self.image.fill(Style.WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.speed = 3
        self.velocity = Vector(0, 0)
        
    def move(self, x, y):
        self.velocity.x += x
        self.velocity.y += y

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self._handle_enemy_collision()
        self._handle_gameobject_collision()

    def _handle_enemy_collision(self):
        enemies_hit = pygame.sprite.spritecollide(self, self.game.enemies, False)

        for enemy in enemies_hit:
            print(enemy)
            enemy.receiveDamage(10)
                
    def _handle_gameobject_collision(self):
        gameobjects_collided = pygame.sprite.spritecollide(self, self.game.get_gameobjects(), False)
        
        for gameobject in gameobjects_collided:
            if self.velocity.x > 0:
                self.rect.right = gameobject.rect.left
            else:
                self.rect.left = gameobject.rect.right
    
        gameobjects_collided = pygame.sprite.spritecollide(self, self.game.get_gameobjects(), False)
        for gameobject in gameobjects_collided:
            if self.velocity.y > 0:
                self.rect.bottom = gameobject.rect.top
            else:
                self.rect.top = gameobject.rect.bottom
