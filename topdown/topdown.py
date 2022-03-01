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
        
                
        self._dead_entities = list()
        self._decayed_entities = list()
        self._finished_particle_fx = list()

        
        self._add_wall(gg.Vec2(0, 0), gg.Vec2(10, 600))
        self._add_wall(gg.Vec2(10, 0), gg.Vec2(790, 10))
        self._add_wall(gg.Vec2(10, 200), gg.Vec2(100, 10))

        self.player = gg.Player(self, 50, 50)
        self.player.layers = entity_layer
        self.player.enemies = self.enemies
        self.physics_system.add(self.player)
        self.entities[self.player.id] = self.player
        self.shield_size = 0
       
        for i in range(3): 
            self._add_enemy(gg.Vec2(1 + (i * 25), 1 + (i * 25)))
     
        self.screen.camera = gg.Camera(self.player, self.screen.width, self.screen.height)
        follow = gg.Follow(self.screen.camera, self.player)
        self.screen.camera.setmethod(follow)
        
        self.space.damping = gg.World.DAMPING
    
        # Setup the collision callback function
        bullet_enemy_colhandler = self.space.add_default_collision_handler()
        bullet_enemy_colhandler.begin = self._bullet_collides_enemy

        
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
            
            for id, particle_effect in self.particle_effects.items():

                if particle_effect.completed:
                    self._finished_particle_fx.add(id)
                    continue

                particle_effect.draw(self.screen)
                particle_effect.update()
                
     
            for entity in self.entities.values():
                if entity.name == gg.PLAYER_NAME: continue
                
                player_pos = self.player.get_body().model.body.position
                entity_pos = entity.get_component(gg.Body).position
                distance = gg.Vec2(player_pos.x - entity_pos.x, player_pos.y - entity_pos.y).length()
               
                if distance < self.screen.width:
                    entity_color = entity.get_body().color
                    fog_alpha = (255 - (255 * distance / self.screen.width)) % 255
                    entity.change_color((entity_color[0], entity_color[1], entity_color[2], fog_alpha))
                if distance < 100_000:
                    entity.update()
                
                if distance < self.screen.width:
                    self.screen.draw(entity)
                stats = entity.get_component(gg.Stats)
                if stats is not None:
                    if not stats.is_alive:
                        self._dead_entities.add(entity)
                        
                decaying = entity.get_component(gg.Decaying)
                if decaying is not None:
                    if decaying.is_dead:
                        self._decayed_entities.add(entity)

            for entity in self._dead_entities:
                ebody = entity.get_body()
                del self.entities[entity.id]
                self.physics_system.remove(entity)
                self.space.remove(ebody.model.body, ebody.model.shape)
            self._dead_entities = set()



            for entity in self._decayed_entities:
                ebody = entity.get_body()
                del self.entities[entity.id]
                self.decaying_system.remove(entity)
                self.physics_system.remove(entity)
                self.space.remove(ebody.model.body, ebody.model.shape)
            self._decayed_entities = set()
            
            for id in self._finished_particle_fx:
                del self.particle_effects[id]
            self._finished_particle_fx = set()
            
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
        pbody = self.player.get_body()
        if self.player.focusing:
            self.shield_size += 1 * delta
        else:
            if self.shield_size > 0:
                self._add_projectile(shoot_dir, gg.Vec2(self.shield_size, 1 * self.shield_size * 0.01))
                self.shield_size = 0

        if (abs(shoot_dir.x) > 0 or abs(shoot_dir.y) > 0) and self.player.can_shoot:
            self.player.shoot()
            self._add_projectile(shoot_dir)


    def _add_enemy(self, position): 

        for i in range(gg.gen_intrange(2, 4)):
            size = gg.Vec2(30, 30)
            if gg.gen_intrange(1, 100) < 10:
                size = gg.Vec2(40, 40)
                
            enemy = gg.Enemy(self, position * i, size)
            self.enemies.add(enemy)
            self.entities[enemy.id] = enemy
            self.physics_system.add(enemy)

    def _add_wall(self, position, size):
        wall = gg.Wall(self, position, size)
        self.entities[wall.id] = wall
        self.physics_system.add(wall)
        return wall
        
    def _add_block(self, position, size, color):
        shape = gg.Rectangle(self.space, position, size, color)
        block = gg.Entity("block", gg.Body(shape), gg.Accelerator(0, 20000, gg.Vec2(0,0)))
        self.entities.add(block)
        self.physics_system.add(block)

        
    def _add_projectile(self, direction, size = gg.Vec2(10, 8)):
        pbody = self.player.get_body()
        pvelocity = pbody.velocity
        bullet_speed = self.player.get_weapon().bullet_speed

        velocity = gg.Vec2(direction.x * bullet_speed, direction.y * bullet_speed)
        velocity += gg.Vec2(velocity.x, 0)
        velocity += gg.Vec2(0, velocity.y)

        position = self.player.get_body().position + (direction * 10)
        bullet = gg.Bullet(self, position, size, pvelocity, velocity)
        self.entities[bullet.id] = bullet
        self.physics_system.add(bullet)
        self.decaying_system.add(bullet)
    
                
    def _bullet_collides_enemy(self, arbiter, space, data):
        entity_a = self.entities.get(arbiter.shapes[0].entity_id)
        entity_b = self.entities.get(arbiter.shapes[1].entity_id)
        
        if entity_a is None or entity_b is None: return True
        
        acolor = entity_a.get_body().model.color
        bcolor = entity_b.get_body().model.color 
        
        if entity_a.type == gg.BULLET_TYPE and entity_b.type == gg.ENEMY_TYPE:
            entity_b.damage(10)
            entity_b.change_color(gg.GGSTYLE.GREEN)

            entity_a.get_decaying().current *= 0.9

        elif entity_b.type == gg.BULLET_TYPE and entity_a.type == gg.ENEMY_TYPE:
            entity_a.damage(10)
            entity_a.change_color(gg.GGSTYLE.GREEN)

            entity_b.get_decaying().current *= 0.9

        elif entity_b.type == gg.ENEMY_TYPE and entity_a.type == gg.ENEMY_TYPE:
            if not gg.Color.is_same_rgb(acolor, gg.GGSTYLE.YELLOW) and not gg.Color.is_same_rgb(acolor, gg.GGSTYLE.RED):
                entity_a.change_color(gg.GGSTYLE.RED)
            if not gg.Color.is_same_rgb(bcolor, gg.GGSTYLE.YELLOW) and not gg.Color.is_same_rgb(bcolor, gg.GGSTYLE.RED):
                entity_b.change_color(gg.GGSTYLE.RED)

        elif entity_b.type == gg.PLAYER_TYPE and entity_a.type == gg.ENEMY_TYPE:
            entity_a.change_color(gg.GGSTYLE.YELLOW)
        elif entity_a.type == gg.PLAYER_TYPE and entity_b.type == gg.ENEMY_TYPE:
            entity_b.change_color(gg.GGSTYLE.YELLOW)
        return True

        
