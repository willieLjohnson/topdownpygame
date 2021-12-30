import pygame
from config import Style

Vector = pygame.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface([15, 15])
        self.image.fill(Style.WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.speed = 3
        self.velocity = Vector(0, 0)
        self.walls = None


    def move(self, x, y):
        self.velocity.x += x
        self.velocity.y += y

    def update(self):
        self.rect.x += self.velocity.x

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.velocity.x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.velocity.y
    
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.velocity.y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
 