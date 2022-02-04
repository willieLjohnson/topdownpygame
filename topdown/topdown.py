import pygame

from . import pygg
gg = pygg.gg

class TopDownGame(gg.Game):
    
    def __init__(self):
        super().__init__('topdownpygame')        
        self.enemies = pygame.sprite.Group()
        
        self._add_wall(gg.Vec2(0, 0), gg.Vec2(10, 600))
        self._add_wall(gg.Vec2(10, 0), gg.Vec2(790, 10))
        self._add_wall(gg.Vec2(10, 200), gg.Vec2(100, 10))
    
        self._add_enemy(gg.Vec2(50, 100))
        self._add_enemy(gg.Vec2(100, 100))

        for i in range(10): 
            self._add_block(gg.gen_vec2(100, 100, 10, 10), gg.Vec2(10, 10), gg.gen_color())

        self._add_block(gg.gen_vec2(100, 100, 10, 10), gg.Vec2(100, 100), self.style.NAVY)

        self.player = gg.Player(self, 50, 50)
        self.player.enemies = self.enemies
        
        self.screen.camera = gg.Camera(self.player, self.screen.width, self.screen.height)
        follow = gg.Follow(self.screen.camera, self.player)
        self.screen.camera.setmethod(follow)
        
        self.space.damping = gg.World.DAMPING
        
    def run(self):
        self.running = 1

        while self.running == 1:
            self.clock.tick(60)
            self._handle_quit()
            self._handle_input()
            self._update_space()
            
            self.player.update()  
            self.screen.clear()
            for entity in self.entities:
                player_pos = self.player.get_body().form.body.position
                entity_pos = entity.get_body().form.body.position
                distance = gg.Vec2(player_pos.x - entity_pos.x, player_pos.y - entity_pos.y).length()
                if entity.is_alive:
                    if distance < 500:
                        entity_color = entity.get_body().color
                        fog_alpha = (255 - (255 * distance / 500)) % 255
                        entity.change_color((entity_color[0], entity_color[1], entity_color[2], fog_alpha))
                    if distance < 1000:
                        entity.update()
                    if distance < 500:
                        self.screen.draw(entity)
                else:
                    self.entities.remove(entity)
            self.screen.draw(self.player)
            self.screen.update()
            pygame.display.update()
        
        pygame.quit()

    def _add_enemy(self, position): 
        enemy = gg.Enemy(self, position, gg.Vec2(15,15))
        self.enemies.add(enemy)
        self.entities.add(enemy)

    def _add_wall(self, position, size):
        wall = gg.Wall(self, position, size)
        self.entities.add(wall)
        
    def _add_block(self, position, size, color):
        shape = gg.Rectangle(self.space, position, size, color)
        block = gg.Entity(self, "block", shape, 0)
        self.entities.add(block)
        
    def _add_projectile(self, direction):
        position = self.player.get_body().position + (direction * 20)
        block = gg.Bullet(self, position, gg.Vec2(8, 8), direction, self.player.weapon.bullet_speed)
        self.entities.add(block) 
        
    def _handle_input(self):

        keys = pygame.key.get_pressed()  #checking dpressed keys

        if keys[pygame.K_a]:
            self.player.move(gg.Vec2(-1,0))
        if keys[pygame.K_d]:
            self.player.move(gg.Vec2(1,0))
        if keys[pygame.K_w]:
            self.player.move(gg.Vec2(0,-1))
        if keys[pygame.K_s]:
            self.player.move(gg.Vec2(0,1))
            
        shoot_dir = gg.Vec2(0,0)
            
        if keys[pygame.K_UP]:
            shoot_dir += gg.Vec2(0, -1)
        if keys[pygame.K_DOWN]:
            shoot_dir += gg.Vec2(0, 1) 
        if keys[pygame.K_LEFT]:
            shoot_dir += gg.Vec2(-1, 0)   
        if keys[pygame.K_RIGHT]:
            shoot_dir += gg.Vec2(1, 0)  
            
        self.player.focusing = keys[pygame.K_LSHIFT]
            
        
        if (abs(shoot_dir.x) > 0 or abs(shoot_dir.y) > 0) and self.player.can_shoot:
            self.player.shoot()
            self._add_projectile(shoot_dir)
         