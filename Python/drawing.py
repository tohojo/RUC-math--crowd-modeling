# vim:fileencoding=utf8

import pygame
try:
    from pygame import gfxdraw
    drawing = "gfxdraw"
except ImportError:
    drawing = "draw"

BG_COLOUR = (255,255,255)
DRAW_COLOUR = (0,0,0)
TARGET_COLOUR = (255,0,0)


COLOURS = [
        (0,0,255),
        (0,255,0),
        (255,0,0),
        ]

class Canvas:
    """Class to manage a canvas and draw objects on it."""

    def __init__(self, width, height, factor, image_prefix):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), 0, 32)
        self.pixel_factor = factor
        self.image_prefix = image_prefix

        self.target_colours = dict()

        self.font = pygame.font.Font(None, 18)

        self.clock = pygame.time.Clock()

    def quit(self):
        pygame.display.quit()

    def clear_screen(self):
        self.screen.fill(BG_COLOUR)

    def tick(self, framerate):
        self.clock.tick(framerate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.image.save(self.screen, "simulation.png")
                return False
        return True

    def update(self):
        pygame.display.flip()

    def create_image(self, frames):
        if pygame.version.vernum < (1,8,0):
            ext = "tga"
        else:
            ext = "png"
        pygame.image.save(self.screen, "%s-%05d.%s" % (self.image_prefix, frames, ext))

    def _draw_circle(self, x, y, r, c):
        if drawing == "gfxdraw":
            gfxdraw.aacircle(self.screen, x, y, r, c)
        elif drawing == "draw":
            pygame.draw.circle(self.screen, c, (x,y), r, 1)

    def _draw_line(self, x1, y1, x2, y2, c):
        if drawing == "gfxdraw":
            gfxdraw.line(self.screen, x1, y1, x2, y2, c)
        elif drawing == "draw":
            pygame.draw.line(self.screen, c, (x1, y1), (x2, y2))

    def draw_wall(self, w):
        (x1,y1) = self.screen_coords(w[0], w[1])
        (x2,y2) = self.screen_coords(w[2], w[3])
        self._draw_line(x1, y1, x2, y2, DRAW_COLOUR)

    def _get_colour(self, t):
        if not t in self.target_colours:
            self.target_colours[t] = COLOURS[len(self.target_colours)]
        return self.target_colours[t]

    def draw_pedestrian(self, x, y, r, t):
        colour = self._get_colour(t)
        (x,y) = self.screen_coords(x,y)
        self._draw_circle(x, y, self.screen_radius(r), colour)

    def draw_target(self, x, y):
        (x,y) = self.screen_coords(x,y)
        if x > self.width or x < -self.width or y > self.height or y < -self.height:
            return
        self._draw_circle(x, y, self.screen_radius(0.2), TARGET_COLOUR)

    def draw_text(self, t, draw_fps):
        if draw_fps:
            text = "%s - %d fps" % (t, self.clock.get_fps())
        else:
            text = t
        texture = self.font.render(text, 
                True, DRAW_COLOUR, BG_COLOUR)
        self.screen.blit(texture, texture.get_rect())


    def screen_coords(self, x, y):
        x *= self.pixel_factor
        y *= -self.pixel_factor

        shift_w = self.width/2
        shift_h = self.height/2

        x += shift_w
        y += shift_h

        return (int(x),int(y))

    def screen_radius(self, r):
        return int(r*self.pixel_factor)

