import pygame
from src.color import BLACK
from src.control.game import Game
from src.control.listeners import setup_win_condition
from src.control.listeners import setup_loss_condition
from src.settings import HEIGHT, WIDTH, FPS
# from src.control.listeners import 

CENTER = (WIDTH/2, HEIGHT/2)

CLOCK_POS = (60, 80)
CLOCK_VEL = (0.0, 0.0)

PUCK_POS = (300, 500)
PUCK_VEL = (5.0, 10.0)


class App():
    def __init__(self) -> None:
        self._running: bool = True
        self.screen = None
        self.clock: pygame.time.Clock = None
        self.size = (WIDTH, HEIGHT)
        self.game = Game(self.size, FPS=FPS)

    def init_objects(self) -> None:
        # clk = TickingClock(CLOCK_POS, CLOCK_VEL)
        # puck = Puck(PUCK_POS, PUCK_VEL)
        # self.objects.append(clk)
        # self.objects.append(puck)
        self.game.declare_objects()
        pass

    def time_event(self, t: int = 2000) -> None:
        pygame.time.wait(t)

    def on_init(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.clock = pygame.time.Clock()
        self._running = True
        # subscribe("RESET_DONE", self.time_event)
        setup_win_condition(self.on_win)
        setup_loss_condition(self.on_loss)

    def on_win(self, data) -> None:
        pygame.time.wait(500)
        self.screen.fill(BLACK)
        font_win = pygame.font.SysFont('freemono', 32)
        rendered = font_win.render('YOU WON!', 1, 'white')
        self.screen.blit(rendered, [0.45*HEIGHT, 0.45*WIDTH])
        pygame.display.flip()
        pygame.event.wait()
        self._running = False

    def on_loss(self, data) -> None:
        pygame.time.wait(1000)
        self.screen.fill(BLACK)
        font_win = pygame.font.SysFont('freemono', 32)
        rendered = font_win.render('YOU LOST!', 1, 'white')
        self.screen.blit(rendered, [0.45*HEIGHT, 0.45*WIDTH])
        pygame.display.flip()
        pygame.event.wait()
        self._running = False

    def on_event(self, events: list[pygame.event.EventType]):
        for event in events:
            # if event.type == pygame.QUIT:
            #     self._running = False
            match event.type:
                case pygame.QUIT:
                    self._running = False
        
        keys = pygame.key.get_pressed()
        self.game.handle_key_event(keys)

    def on_update(self):
        # for object in self.game.objects:
        #     updated_pos, updated_vel = move_around(object)
        #     object.update_position(updated_pos)
        #     object.update_velocity(updated_vel)
        self.game.update_positions()
        pass


    def render(self):
        for object in self.game.font_objects:
            render = object.render()
            pos = object.get_position()
            self.screen.blit(render, pos)
        # render = self.clk.render()
        # pos = self.clk.get_position()
        # self.screen.blit(render, pos)
        for object in self.game.ball_objects:
            obj_rect, obj_color = object.render()
            pygame.draw.rect(self.screen, obj_color, obj_rect)
        for object in self.game.control_objects:
            obj_rect, obj_color = object.render()
            pygame.draw.rect(self.screen, obj_color, obj_rect)
        pass

    def on_execute(self) -> None:
        self.on_init()
        self.init_objects()

        while self._running:
            # self._frame_count += 1
            self.screen.fill(BLACK)
            self.on_event(events=pygame.event.get())
            self.on_update()
            # if self._frame_count % 5 == 0:
            #     print(f"Rendering ... {self._frame_count}")
            self.render()
            self.clock.tick(FPS)
            pygame.display.flip()
        
        pygame.quit()

