import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.speed = 3
        self.change_x = 0
        self.change_y = 0
        self.walls = None


    def change_speed(self, x, y):
        self.change_x += x
        self.change_y += y

    # TODO: Try to loop through block hit list only once
    def update(self):
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y
    
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
                
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
        
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

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
    
    screen.fill(BLACK)        
    gameobjects.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
            
            
            
            
            