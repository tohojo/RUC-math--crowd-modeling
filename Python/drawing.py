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
        pygame.draw.line(self.screen, DRAW_COLOR, 
                Helper.screen_coords(w.start), 
                Helper.screen_coords(w.end))

    def draw_actor(self, a):
        pygame.draw.circle(self.screen, DRAW_COLOR, 
                Helper.screen_coords(a), Helper.screen_radius(a.radius))


class Helper:

    @staticmethod
    def screen_coords(x, y = None):
        if hasattr(x, "as_tuple"):
            (x, y) = x.as_tuple()
        x *= PIXEL_FACTOR
        y *= -PIXEL_FACTOR

        shift_w = SCREEN_WIDTH/2
        shift_h = SCREEN_HEIGHT/2

        x += shift_w
        y += shift_h

        return (x,y)

    @staticmethod
    def screen_radius(r):
        return r*PIXEL_FACTOR

