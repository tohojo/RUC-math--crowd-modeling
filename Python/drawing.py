# vim:fileencoding=utf8

import pygame
import parameters as pm

if pm.use_c_ext:
    import optimised

SCREEN_WIDTH=600
SCREEN_HEIGHT=600
PIXEL_FACTOR = 20
BG_COLOR = (255,255,255)
DRAW_COLOR = pygame.Color(0,0,0)
TARGET_COLOR = pygame.Color(255,0,0)

class Canvas:
    """Class to manage a canvas and draw objects on it."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                0, 32)
        self.font = pygame.font.Font(None, 16)

        self.clock = pygame.time.Clock()


    def clear_screen(self):
        self.screen.fill(BG_COLOR)

    def tick(self):
        self.clock.tick(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(self.screen, "simulation.png")
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
                Helper.screen_coords(a.position),
                Helper.screen_radius(a.radius))

    def draw_actors(self):
        if pm.use_c_ext:
            for i in xrange(pm.actor.initial_number):
                (x,y,r) = optimised.get_actor(i)
                pygame.draw.circle(self.screen, DRAW_COLOR,
                        Helper.screen_coords(x,y),
                        Helper.screen_radius(r))


    def draw_target(self, t):
        pygame.draw.circle(self.screen, TARGET_COLOR, 
                Helper.screen_coords(t[0], t[1]),
                Helper.screen_radius(0.2))

    def draw_proj(self, p):
        pygame.draw.circle(self.screen, DRAW_COLOR, 
                Helper.screen_coords(p), 2)

    def draw_text(self, t):
        text = self.font.render("%s - %d fps" % (t, self.clock.get_fps()), True, DRAW_COLOR, BG_COLOR)
        self.screen.blit(text, text.get_rect())


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

        return (int(x),int(y))

    @staticmethod
    def screen_radius(r):
        return int(r*PIXEL_FACTOR)

