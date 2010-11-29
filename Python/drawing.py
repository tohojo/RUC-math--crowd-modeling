# vim:fileencoding=utf8

import pygame
from pygame import gfxdraw
import parameters as pm

if pm.use_c_ext:
    import optimised

SCREEN_WIDTH=600
SCREEN_HEIGHT=600
PIXEL_FACTOR = 30
BG_COLOUR = (255,255,255)
DRAW_COLOUR = pygame.Color(0,0,0)
TARGET_COLOUR = pygame.Color(255,0,0)

class Canvas:
    """Class to manage a canvas and draw objects on it."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                0, 32)
        self.font = pygame.font.Font(None, 16)

        self.clock = pygame.time.Clock()


    def clear_screen(self):
        self.screen.fill(BG_COLOUR)

    def tick(self):
        self.clock.tick(pm.framerate_limit)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(self.screen, "simulation.png")
                return False
        return True

    def update(self, frames):
        pygame.display.flip()
        if pm.create_images:
            pygame.image.save(self.screen, "%s%05d.png" % (pm.image_prefix, frames))

    def draw_wall(self, w):
        (x1,y1) = Helper.screen_coords(w.start)
        (x2,y2) = Helper.screen_coords(w.end)
        gfxdraw.line(self.screen, x1, y1, x2, y2, DRAW_COLOUR)

    def draw_actor(self, a):
        pygame.draw.circle(self.screen, DRAW_COLOUR, 
                Helper.screen_coords(a.position),
                Helper.screen_radius(a.radius))

    def draw_actors(self):
        if pm.use_c_ext:
            for (x,y,r) in optimised.get_actors():
                (x,y) = Helper.screen_coords(x,y)
                gfxdraw.aacircle(self.screen,
                        x,y,
                        Helper.screen_radius(r),
                        DRAW_COLOUR)


    def draw_target(self, t):
        (x,y) = Helper.screen_coords(t[0], t[1])
        gfxdraw.aacircle(self.screen, x, y,
                Helper.screen_radius(0.2),
                TARGET_COLOUR)

    def draw_proj(self, p):
        pygame.draw.circle(self.screen, DRAW_COLOUR, 
                Helper.screen_coords(p), 2)

    def draw_text(self, t):
        if pm.create_images:
            text = t
        else:
            text = "%s - %d fps" % (t, self.clock.get_fps())
        texture = self.font.render(text, 
                True, DRAW_COLOUR, BG_COLOUR)
        self.screen.blit(texture, texture.get_rect())


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

