import pygame
from config import *
from player import Player
from game_objects import Wall

Vector = pygame.Vector2

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('topdownpygame')
        
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        self.gameobjects = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
    
        wall = Wall(0, 0, 10, 600)
        self.walls.add(wall)
        self.gameobjects.add(wall)

        wall = Wall(10, 0, 790, 10)
        self.walls.add(wall)
        self.gameobjects.add(wall)

        wall = Wall(10, 200, 100, 10)
        self.walls.add(wall)
        self.gameobjects.add(wall)

        self.player = Player(50, 50)
        self.player.walls = self.walls
        self.gameobjects.add(self.player)
        

    def run(self):
        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self._handle_input()           
            self.gameobjects.update()
            
            self.screen.fill(Style.BLACK)        
            self.gameobjects.draw(self.screen)
            
            pygame.display.flip()
            
            self.clock.tick(60)

        pygame.quit()
    
    def _handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.player.move(-self.player.speed, 0)
                    elif event.key == pygame.K_d:
                        self.player.move(self.player.speed, 0)
                    elif event.key == pygame.K_w:
                        self.player.move(0, -self.player.speed)
                    elif event.key == pygame.K_s:
                        self.player.move(0, self.player.speed)
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.move(self.player.speed, 0)
                    elif event.key == pygame.K_d:
                        self.player.move(-self.player.speed, 0)
                    elif event.key == pygame.K_w:
                        self.player.move(0, self.player.speed)
                    elif event.key == pygame.K_s:
                        self.player.move(0, -self.player.speed)
                        
Game().run()               
            
            