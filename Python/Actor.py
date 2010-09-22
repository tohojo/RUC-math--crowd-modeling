# vim:fileencoding=utf8

from Vector import Vector

class Actor(Vector):

    def __init__(self, x, y, radius = 1.0):
        Vector.__init__(self, x, y)
        self.radius = radius

    @property
    def center(self):
        "Return center as a tuple"
        return self.as_tuple()

    def __mul__( self, scalar ):
        """Vector(x1*x2, y1*y2)"""
        return Actor(self.x*scalar, self.y*scalar, self.radius*scalar)

    def translated(self, dx, dy):
        return Actor(self.x+dx, self.y+dy, self.radius)

    def multiplied(self, scalar):
        return self * scalar

    def screen_coords(self, width, height, factor):
        self.radius *= factor
        Vector.screen_coords(self, width, height, factor)

    def clone(self):
        return Actor(self.x, self.y, self.radius)
