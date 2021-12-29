import pygame
from config import Style
from player import Player
from game_objects import Wall

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

Vector = pygame.Vector2

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Platformer')

gameobjects = pygame.sprite.Group()
walls = pygame.sprite.Group()

wall = Wall(0, 0, 10, 600)
walls.add(wall)
gameobjects.add(wall)

wall = Wall(10, 0, 790, 10)
walls.add(wall)
gameobjects.add(wall)

wall = Wall(10, 200, 100, 10)
walls.add(wall)
gameobjects.add(wall)

player = Player(50, 50)
player.walls = walls
gameobjects.add(player)

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.change_speed(-player.speed, 0)
            elif event.key == pygame.K_d:
                player.change_speed(player.speed, 0)
            elif event.key == pygame.K_w:
                player.change_speed(0, -player.speed)
            elif event.key == pygame.K_s:
                player.change_speed(0, player.speed)
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.change_speed(player.speed, 0)
            elif event.key == pygame.K_d:
                player.change_speed(-player.speed, 0)
            elif event.key == pygame.K_w:
                player.change_speed(0, player.speed)
            elif event.key == pygame.K_s:
                player.change_speed(0, -player.speed)
                
    gameobjects.update()
    
    screen.fill(Style.BLACK)        
    gameobjects.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
            
            
            
            
            