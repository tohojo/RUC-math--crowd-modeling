# vim:fileencoding=utf8

import pygame

SCREEN_WIDTH=600
SCREEN_HEIGHT=600
PIXEL_FACTOR = 30
BG_COLOR = (255,255,255)
DRAW_COLOR = pygame.Color(0,0,0)

class Canvas:
    """Class to manage a canvas and draw objects on it."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                0, 32)


        self.clock = pygame.time.Clock()


    def clear_screen(self):
        self.screen.fill(BG_COLOR)

    def tick(self):
        self.clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        pygame.display.flip()

    def draw_wall(self, w):
        w = w.clone()
        w.screen_coords(SCREEN_WIDTH, SCREEN_HEIGHT, PIXEL_FACTOR)
        pygame.draw.line(self.screen, DRAW_COLOR, w.start.as_tuple(), w.end.as_tuple())

    def draw_actor(self, a):
        a = a.clone()
        a.screen_coords(SCREEN_WIDTH, SCREEN_HEIGHT, PIXEL_FACTOR)
        pygame.draw.circle(self.screen, DRAW_COLOR, a.as_tuple(), a.radius)
