import pygame
import random
from . import pygg as GG
           
def collide(gameobject, other):
    if gameobject.rect.colliderect(other.rect):
        collision_tolerance_h = (gameobject.rect.h + other.rect.h) * 0.5
        collision_tolerance_w = (gameobject.rect.w + other.rect.w) * 0.5
        
        # moving up
        up_difference = other.rect.bottom - gameobject.rect.top
        if abs(up_difference) < collision_tolerance_h and gameobject.body.velocity.y < 0:
            gameobject.body.velocity.y *= -1
            other.body.velocity.y *= -1
            gameobject.rect.y += up_difference
            # other.rect.y -= up_difference
            
        # moving down
        down_difference = other.rect.top - gameobject.rect.bottom
        if abs(down_difference) < collision_tolerance_h and gameobject.body.velocity.y > 0:
            gameobject.body.velocity.y *= -1
            other.body.velocity.y *= -1
            gameobject.rect.y += down_difference
            # other.rect.y -= down_difference

        # moving left
        left_difference = other.rect.right - gameobject.rect.left
        if abs(left_difference) < collision_tolerance_w and gameobject.body.velocity.x < 0:
            gameobject.body.velocity.x *= -1
            other.body.velocity.x *= -1
            gameobject.rect.x += left_difference
            # other.rect.x -= left_difference

        # moving right
        right_difference = other.rect.left - gameobject.rect.right
        if abs(right_difference) < collision_tolerance_w and gameobject.body.velocity.x > 0:
            gameobject.body.velocity.x *= -1
            other.body.velocity.x *= -1
            gameobject.rect.x += right_difference
            # other.rect.x -= right_difference
            
class BouncyGame(GG.Game):
    def __init__(self):
        super().__init__('bouncy')
        for i in range(50):
            self._create_bouncy(GG.Vec2((GG.SCREEN_WIDTH - 15) * random(), (GG.SCREEN_HEIGHT - 15) * random()))
        


        
    def run(self):
        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.clock.tick(60)
            self.gameobjects.update()
            self._handle_collisions()
            self._handle_input()
            GG.screen.fill(GG.Style.BLACK)
            self.gameobjects.draw(GG.screen)
            pygame.display.update()

        pygame.quit()
    
    def _create_bouncy(self, position=GG.Vec2((GG.SCREEN_WIDTH - 15) * random(), (GG.SCREEN_HEIGHT - 15) * random())):
        bouncy = GG.Entity(self, 'bouncy', GG.Body(position=position, color= (255 * random(), 255* random(), 255* random())))
        bouncy.body.velocity = GG.Vec2(1,1)
        self.gameobjects.add(bouncy)
      
    def _handle_collisions(self):        
        for bouncy in self.gameobjects:
            # with screen
            if bouncy.rect.right > GG.SCREEN_WIDTH or bouncy.rect.left < 0:
                bouncy.body.velocity.x *= -1
            if bouncy.rect.bottom > GG.SCREEN_HEIGHT or bouncy.rect.top < 0:
                bouncy.body.velocity.y *= -1
                
            for other in self.gameobjects:
                if other == bouncy:
                    continue
                collide(bouncy, other)

                
            
             
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()  #checking pressed keys

        # if keys[pygame.K_a]:
        #     self.player.move(-self.player.speed, 0)
        # if keys[pygame.K_d]:
        #     self.player.move(self.player.speed, 0)
        # if keys[pygame.K_w]:
        #     self.player.move(0, -self.player.speed)
        # if keys[pygame.K_s]:
        #     self.player.move(0, self.player.speed)
                
    def get_gameobjects(self):
        return [*self.walls, *self.enemies]
    