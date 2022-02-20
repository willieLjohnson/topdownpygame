import pygame

from . import pygg
gg = pygg.gg

# This layer bit is for balls colliding with other balls
# I'm only guessing that you want this though.
bullet_layer = 1
# This layer bit is for things that collide with red balls only.
entity_layer = 2
# This layer bit is for things that collide with blue balls only.
player_layer = 4
object_layer = 8

class Game(gg.Game):
    
    def __init__(self):
        super().__init__('topdownpygame')        
        self.enemies = pygame.sprite.Group()
        self.physics_system = gg.PhysicsSystem()
        self.decaying_system = gg.System([gg.Decaying])
        
        self._add_wall(gg.Vec2(0, 0), gg.Vec2(10, 600))
        self._add_wall(gg.Vec2(10, 0), gg.Vec2(790, 10))
        self._add_wall(gg.Vec2(10, 200), gg.Vec2(100, 10))
    
        # self._add_enemy(gg.Vec2(50, 100))
        # self._add_enemy(gg.Vec2(100, 100))

        # for i in range(10): 
        #     self._add_block(gg.gen_vec2(100, 100, 10, 10), gg.Vec2(10, 10), gg.gen_color())

        # self._add_block(gg.gen_vec2(100, 100, 10, 10), gg.Vec2(100, 100), self.style.NAVY)

        self.player = gg.Player(self, 50, 50)
        self.player.layers = entity_layer
        self.player.enemies = self.enemies
        self.physics_system.add(self.player)
        
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
            self._update_space()
            self.physics_system.update(delta)
            self.decaying_system.update(delta)
            self.player.update()
            self.screen.clear(self.style.BLACK)
            self.screen.drawGrid()
            
            self._finished_particle_fx = list()
            for id, particle_effect in self.particle_effects.items():

                if particle_effect.completed:
                    self._finished_particle_fx.append(id)
                    continue

                particle_effect.draw(self.screen)
                particle_effect.update()
                
            self._dead_entities = list()
            self._decayed_entities = list()
            for entity in self.entities.values():
                player_pos = self.player.get_body().model.body.position
                entity_pos = entity.get_component(gg.Body).position
                distance = gg.Vec2(player_pos.x - entity_pos.x, player_pos.y - entity_pos.y).length()
               
                if distance < self.screen.width:
                    entity_color = entity.get_body().color
                    fog_alpha = (255 - (255 * distance / self.screen.width)) % 255
                    entity.change_color((entity_color[0], entity_color[1], entity_color[2], fog_alpha))
                if distance < self.screen.width * 2:
                    entity.update()
                if distance < self.screen.width:
                    self.screen.draw(entity)
                stats = entity.get_component(gg.Stats)
                if stats is not None:
                    if not stats.is_alive:
                        self._dead_entities.append(entity)
                        
                decaying = entity.get_component(gg.Decaying)
                if decaying is not None:
                    if decaying.is_dead:
                        self._decayed_entities.append(entity)

            for entity in self._dead_entities:
                del self.entities[entity.id]
                self.physics_system.remove(entity)


            for entity in self._decayed_entities:
                del self.entities[entity.id]
                self.decaying_system.remove(entity)
                self.physics_system.remove(entity)


            for id in self._finished_particle_fx:
                del self.particle_effects[id]
            

            self.screen.draw(self.player)

            self.screen.update()
            pygame.display.update()
            # print(len(self.particle_effects))

        pygame.quit()
    
    
    def _handle_input(self, delta):

        keys = pygame.key.get_pressed()  #checking dpressed keys

        dust_dir = [0, 0]

        if keys[pygame.K_a]:
            self.player.move(gg.Vec2(-1,0))
            dust_dir[1] -= 1

        if keys[pygame.K_d]:
            self.player.move(gg.Vec2(1,0))
            dust_dir[1] += 1


        if keys[pygame.K_w]:
            self.player.move(gg.Vec2(0,-1))
            dust_dir[0] -= 1

        if keys[pygame.K_s]:
            self.player.move(gg.Vec2(0,1))
            dust_dir[0] += 1
            
        
        if dust_dir[0] != 0 or dust_dir [1] != 0:
            dust_fx = gg.Dust(self.player.rect.center, dust_dir) 
            self.particle_effects[dust_fx.id] = gg.Dust(self.player.rect.center, dust_dir)


            
        shoot_dir = gg.Vec2(0,0)
        if self.player.can_shoot:
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


    def _add_enemy(self, position): 
        enemy = gg.Enemy(self, position, gg.Vec2(15,15))
        self.enemies.add(enemy)
        self.entities.add(enemy)

    def _add_wall(self, position, size):
        wall = gg.Wall(self, position, size)
        self.entities[wall.id] = wall
        self.physics_system.add(wall)
        
    def _add_block(self, position, size, color):
        shape = gg.Rectangle(self.space, position, size, color)
        block = gg.Entity("block", gg.Body(shape), gg.Accelerator(0, 20000, gg.Vec2(0,0)))
        self.entities.add(block)
        self.physics_system.add(block)

        
    def _add_projectile(self, direction):
        pbody = self.player.get_body()
        pvelocity = pbody.velocity
        bullet_speed = self.player.get_weapon().bullet_speed
   
        same_x = (direction.x * pvelocity.x) > 0
        same_y = (direction.y * pvelocity.y) > 0
        
        velocity = gg.Vec2(direction.x * bullet_speed, direction.y * bullet_speed)
        velocity += pvelocity
        velocity += gg.Vec2(velocity.x, 0)
        velocity += gg.Vec2(0, velocity.y)

        position = self.player.get_body().position + (direction * 10)
        bullet = gg.Bullet(self, position, gg.Vec2(8, 8), velocity)
        self.entities[bullet.id] = bullet
        self.physics_system.add(bullet)
        self.decaying_system.add(bullet)
    