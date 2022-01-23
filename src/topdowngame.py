import pygame
from . import pygg as GG

class TopDownGame(GG.Game):
    def __init__(self):
        super().__init__('topdownpygame')        
        self.enemies = pygame.sprite.Group()
        
        self._add_wall(GG.Vec2(0, 0), GG.Vec2(10, 600))
        self._add_wall(GG.Vec2(10, 0), GG.Vec2(790, 10))
        self._add_wall(GG.Vec2(10, 200), GG.Vec2(100, 10))
    
        self._add_enemy(GG.Vec2(50, 100))
        self._add_enemy(GG.Vec2(100, 100))
        
        for i in range(2): 
            self.gameobjects.add(GG.GameObject(self, 'block', GG.Vec2(i * 30, i * 30), GG.Vec2(15,15), GG.STYLE.BLUE, 0))

        self.player = GG.Player(self, 50, 50)
        self.player.enemies = self.enemies
        
        self.camera = GG.Camera(self.player)
        follow = GG.Follow(self.camera, self.player)
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
            GG.canvas.fill(GG.STYLE.BLACK)
            
            for gameobject in self.gameobjects:
                if gameobject.is_alive():
                    GG.canvas.blit(gameobject.image, (gameobject.rect.x - self.camera.offset.x, gameobject.rect.y - self.camera.offset.y))
                else:
                    self.gameobjects.remove(gameobject)
            GG.canvas.blit(self.player.image, (self.player.rect.x - self.camera.offset.x, self.player.rect.y - self.camera.offset.y))
            GG.screen.blit(GG.canvas, (0, 0))
            
            pygame.display.update()
        
        pygame.quit()

    def _add_enemy(self, position): 
        enemy = GG.Enemy(self, position, GG.Vec2(15,15))
        self.enemies.add(enemy)
        self.gameobjects.add(enemy)

    def _add_wall(self, position, size):
        wall = GG.Wall(self, position, size)
        self.gameobjects.add(wall)
        
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()  #checking pressed keys

        if keys[pygame.K_a]:
            self.player.accelerate(GG.Direction.LEFT, 0)
        if keys[pygame.K_d]:
            self.player.accelerate(GG.Direction.RIGHT, 0)
        if keys[pygame.K_w]:
            self.player.accelerate(0, GG.Direction.UP)
        if keys[pygame.K_s]:
            self.player.accelerate(0, GG.Direction.DOWN)
            
            