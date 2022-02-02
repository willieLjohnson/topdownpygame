import pygame

from src.pygg.src import game

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

        for i in range(10): 
            self._add_block(GG.gen_vec2(100, 100, 10, 10), GG.Vec2(10, 10), GG.gen_color())

        self._add_block(GG.gen_vec2(100, 100, 10, 10), GG.Vec2(100, 100), self.style.NAVY)

        self.player = GG.Player(self, 50, 50)
        self.player.enemies = self.enemies
        
        self.camera = GG.Camera(self.player)
        follow = GG.Follow(self.camera, self.player)
        self.camera.setmethod(follow)
        
        self.space.damping = GG.World.DAMPING
        
    def run(self):
        self.running = 1

        while self.running == 1:
            self.clock.tick(60)
            self._handle_quit()
            self._handle_input()
            self._update_space()
            self.player.update()
            self.camera.scroll()
            GG.canvas.fill(GG.STYLE.BLACK)
            
            for gameobject in self.gameobjects:
                player_pos = self.player.get_component(GG.ComponentType.BODY).form.body.position
                gameobject_pos = gameobject.get_component(GG.ComponentType.BODY).form.body.position
                distance = GG.Vec2(player_pos.x - gameobject_pos.x, player_pos.y - gameobject_pos.y).length()
                if gameobject.is_alive:
                    if distance < 500:
                        gameobject_color = gameobject.get_component(GG.ComponentType.BODY).color
                        fog_alpha = (255 - (255 * distance / 500)) % 255
                        gameobject.change_color((gameobject_color[0], gameobject_color[1], gameobject_color[2], fog_alpha))
                    if distance < 1000:
                        gameobject.update()
                    if distance < 500:
                        GG.canvas.blit(gameobject.image, (gameobject.rect.x - self.camera.offset.x, gameobject.rect.y - self.camera.offset.y))
                else:
                    self.gameobjects.remove(gameobject)
            GG.canvas.blit(self.player.image, (self.player.rect.x - self.camera.offset.x, self.player.rect.y - self.camera.offset.y))
            GG.main.blit(GG.canvas, (0, 0))
            
            pygame.display.update()
        
        pygame.quit()

    def _add_enemy(self, position): 
        enemy = GG.Enemy(self, position, GG.Vec2(15,15))
        self.enemies.add(enemy)
        self.gameobjects.add(enemy)

    def _add_wall(self, position, size):
        wall = GG.Wall(self, position, size)
        self.gameobjects.add(wall)
        
    def _add_block(self, position, size, color):
        shape = GG.Rectangle(self.space, position, size, color)
        block = GG.GameObject(self, "block", shape, 0)
        self.gameobjects.add(block)
        
    def _add_projectile(self, direction):
        position = self.player.get_component(GG.ComponentType.BODY).position + (direction * 20)
        block = GG.Bullet(self, position, GG.Vec2(8, 8), direction, self.player.weapon.bullet_speed)
        self.gameobjects.add(block) 
        
    def _handle_input(self):

        keys = pygame.key.get_pressed()  #checking pressed keys

        if keys[pygame.K_a]:
            self.player.accelerate(GG.Vec2(-1,0))
        if keys[pygame.K_d]:
            self.player.accelerate(GG.Vec2(1,0))
        if keys[pygame.K_w]:
            self.player.accelerate(GG.Vec2(0,-1))
        if keys[pygame.K_s]:
            self.player.accelerate(GG.Vec2(0,1))
            
        shoot_dir = GG.Vec2(0,0)

            
            
        if keys[pygame.K_UP]:
            shoot_dir += GG.Vec2(0, -1)
        if keys[pygame.K_DOWN]:
            shoot_dir += GG.Vec2(0, 1) 
        if keys[pygame.K_LEFT]:
            shoot_dir += GG.Vec2(-1, 0)   
        if keys[pygame.K_RIGHT]:
            shoot_dir += GG.Vec2(1, 0)  
            
        self.player.focusing = keys[pygame.K_LSHIFT]
            
        
        if (abs(shoot_dir.x) > 0 or abs(shoot_dir.y) > 0) and self.player.can_shoot:
            self.player.shoot()
            self._add_projectile(shoot_dir)
         