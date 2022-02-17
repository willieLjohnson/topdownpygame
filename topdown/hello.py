import pygame
from . import pygg
gg = pygg.gg

from typing import TypedDict, Type

class Systems(TypedDict):
    system_type: Type[gg.System]
    system: gg.System
    


class Game(gg.Game):
    def __init__(self):
        super().__init__('hello')
        
        self.player = gg.Player(self, 50, 50)
        
        object = gg.Wall(self, gg.Vec2(10, 10), gg.Vec2(self.screen.height, 10))
        self.entities.add(object)
        self.physics_system = gg.PhysicsSystem([self.player, object])

        self.screen.camera = gg.Camera(self.player, self.screen.width, self.screen.height)
        follow = gg.Follow(self.screen.camera, self.player)
        self.screen.camera.setmethod(follow)
        self.space.damping = gg.World.DAMPING
        
 
    def run(self):
        self.running = 1

        while self.running == 1:
            delta = self.clock.tick(60)
            self._handle_quit()
            self._handle_input(delta)
            self.player.update()  
            self._update_space()
            self.entities.update()
            self.screen.clear()
            self.physics_system.update(delta)
            self.screen.drawGrid()
            for entity in self.entities:
                player_pos = self.player.get_body().position
                entity_pos = entity.get_body().position
                distance = gg.Vec2(player_pos.x - entity_pos.x, player_pos.y - entity_pos.y).length()
        
                self.screen.draw(entity)
                    
                # stats = entity.get_component(Stats)
                # if stats is not None:
                #     if not stats.is_alive:
                #         self.entities.remove(entity)
                        
            self.screen.draw(self.player)
            self.screen.update()                    

            # self.space.debug_draw(self._draw_options)


            pygame.display.flip()
            print(self.clock.get_fps())
        
        pygame.quit()
    
        
    def _handle_input(self, delta):

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