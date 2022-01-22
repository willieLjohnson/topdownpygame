import pygame
from config import *
from player import Player
from camera import *
from game_objects import *
from core import *

class TopDown(Game):
    def __init__(self):
        super().__init__('topdownpygame')
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        self._add_wall(Vector(0, 0), Vector(10, 600))
        self._add_wall(Vector(10, 0), Vector(790, 10))
        self._add_wall(Vector(10, 200), Vector(100, 10))
    
        self._add_enemy(Vector(50, 100))
        self._add_enemy(Vector(100, 100))

        self.player = Player(self, 50, 50)
        self.player.enemies = self.enemies
        
        self.camera = Camera(self.player)
        follow = Follow(self.camera, self.player)
        self.camera.setmethod(follow)
        
    def run(self):
        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.clock.tick(60)
            self._handle_input()
            self.gameobjects.update()
            self.player.update()
            self.camera.scroll()
            canvas.fill(Style.BLACK)
            
            for gameobject in self.get_gameobjects():
                if gameobject.is_alive():
                    canvas.blit(gameobject.image, (gameobject.rect.x - self.camera.offset.x, gameobject.rect.y - self.camera.offset.y))
                else:
                    self.gameobjects.remove(gameobject)
            canvas.blit(self.player.image, (self.player.rect.x - self.camera.offset.x, self.player.rect.y - self.camera.offset.y))
            screen.blit(canvas, (0, 0))
            
            pygame.display.update()
        
        pygame.quit()

    def _add_enemy(self, position): 
        enemy = Enemy(self, position, Vector(15,15))
        enemy.walls = self.walls
        self.gameobjects.add(enemy)
        self.enemies.add(enemy)

    def _add_wall(self, position, size):
        wall = Wall(self, position, size)
        self.walls.add(wall)
        self.gameobjects.add(wall) 
        
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()  #checking pressed keys

        if keys[pygame.K_a]:
            self.player.accelerate(Direction.LEFT, 0)
        if keys[pygame.K_d]:
            self.player.accelerate(Direction.RIGHT, 0)
        if keys[pygame.K_w]:
            self.player.accelerate(0, Direction.UP)
        if keys[pygame.K_s]:
            self.player.accelerate(0, Direction.DOWN)
                
    def get_gameobjects(self):
        return [*self.walls, *self.enemies]
    
TopDown().run()               
            
            