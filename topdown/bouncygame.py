import pygame
import uuid
from . import pygg
gg = pygg.gg

@gg.generate_component_classmethods(gg.Body, gg.Accelerator)
class Bouncy(gg.Entity):
    def __init__(self, *components):
        super().__init__("bouncy", components)
        self.id = uuid.uuid4()
            
class Game(gg.Game):
    debug = False
    def __init__(self):
        super().__init__('bouncy')
        self.speed_multiplier = 1
        self.style.background = gg.GGSTYLE.BLACK
        self.debug = True
        self.system = gg.PhysicsSystem()

        for _ in range(0):
            self._create_bouncy()
        self.space.damping = 1
        self.box = gg.Box(self.space, (10, 10), (self.screen.width - 10, self.screen.height - 10), 1, 0)
        self.rectangle = gg.Rectangle(self.space, (self.screen.width / 2, self.screen.height / 2), (300,300), self.style.WHITE, 1, 0)
        
        
    def run(self):
        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self._handle_quit()
            self._handle_input()
            delta = self.clock.tick(120)
            self._update_space()
            self.entities.update()
            self.system.update(delta)
            self.screen.clear(self.style.background) 

            for entity in self.entities:
                self.screen.draw(entity)
            
            if self.debug:
                self.space.debug_draw(self._draw_options)
            self.screen.update()
            pygame.display.flip()


        pygame.quit()

        
    def _create_bouncy(self):
        random_color = gg.gen_color(255)
        random_position = gg.gen_vec2(self.screen.width, self.screen.height)
        random_size = gg.gen_range(1, 40) 
        random_speed = gg.gen_range(-30000, 30000)
        random_vel = gg.gen_vec2(random_speed, random_speed)
        bouncy = Bouncy()
        bouncy._set_body(self.space, random_position, gg.Vec2(random_size, random_size), random_color, random_vel, 1, 0)
        bouncy._set_accelerator(0, random_speed)
        bouncy._update_sprite_with_body()

        self.entities.add(bouncy)
        self.system.add(bouncy)
        
             
    def _handle_input(self):
        keys = pygame.key.get_pressed()  #checking pressed keys

        if keys[pygame.K_d]:
            self.debug = not self.debug
        if keys[pygame.K_a]:
            self._create_bouncy()

