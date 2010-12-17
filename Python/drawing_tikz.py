# vim:fileencoding=utf8

DRAW_COLOUR = "black"
TARGET_COLOUR = "red"

COLOURS = [
        "blue",
        "green",
        "red",
        ]

class Canvas:
    """Class to manage a canvas and draw objects on it."""

    def __init__(self, width, height, factor, image_prefix):
        self.width = width/float(factor)
        self.height = height/float(factor)
        self.output = []
        self.image_prefix = image_prefix
        self.pixel_factor = factor

        self.target_colours = dict()


    def quit(self):
        print

    def clear_screen(self):
        pass

    def tick(self, framerate):
        return True

    def update(self):
        pass

    def create_image(self, frames):
        output = "\r%d frames" % (frames+1)
        print output,

        filename = "%s-%05d.tex" % (self.image_prefix, frames)
        fp = open(filename, "w")
        fp.write("\\begin{tikzpicture}\n")
        fp.write("\n".join(self.output))
        fp.write("\n\\end{tikzpicture}\n")
        fp.close()
        self.output = []

    def _draw_circle(self, x, y, r, c):
        if x > self.width or x < -self.width or y > self.height or y < -self.height:
            return
        self.output.append("\\draw[color=%s] (%.2f,%.2f) circle (%.2f);" % (c,x,y,r))

    def _draw_line(self, x1, y1, x2, y2, c):
        self.output.append(
                "\\draw[color=%s] (%.2f,%.2f) -- (%.2f,%.2f);" % (c,x1,y1,x2,y2))

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
        self._draw_circle(x, y, self.screen_radius(0.2), TARGET_COLOUR)

    def draw_text(self, t, draw_fps):
        x = self.width/2.0
        y = self.height/2.0
        if draw_fps:
            text = "%s - %d fps" % (t, self.clock.get_fps())
        else:
            text = t
        self.output.append("\\node at (%.2f, %.2f) {%s};" % (-x, y, text))

        self.output.append("\\useasboundingbox (%.2f, %.2f) rectangle (%.2f, %.2f);" %(
            -x, -y, x, y))


    def screen_coords(self, x, y):
        return (x,y)

    def screen_radius(self, r):
        return r

