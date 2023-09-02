import pygame
from src.clock import render_simple_clock, declare_clock_font, TickingClock
from src.color import BLACK, WHITE, BLURPLE
# CLOCK_FONT = 'nimbussansnarrow'

# window settings
FPS = 2
SCREEN_X = 480
SCREEN_Y = 800

def view() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    clock = pygame.time.Clock()
    running = True

    time_font_pos = (64, 140)
    # font_for_time = declare_clock_font()
    time_display= TickingClock(time_font_pos)

    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
        
        screen.fill(BLACK)

        # time_font_rect =  render_simple_clock(font_for_time, BLURPLE)
        time_font_rect = time_display.render()
        screen.blit(time_font_rect, time_font_pos)
        
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
