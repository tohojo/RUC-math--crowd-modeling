# vim:fileencoding=utf8

from Vector import Vector, Point
import numpy

EPSILON = 10e-5
CALC_RANGE = 300

class Actor(Vector):

    def __init__(self, x, y, **kwargs):
        Vector.__init__(self, x, y)

        if kwargs.has_key("radius"):
            self.radius = kwargs["radius"]
        else:
            self.radius = 0.5

        if kwargs.has_key("velocity"):
            self.velocity = kwargs["velocity"]
        else:
            self.velocity = Vector(1.0, 1.0)

        if kwargs.has_key("target"):
            self.target = kwargs["target"]
        else:
            self.target = Point(1.0, 1.0)

        self.acceleration = Vector(0.0,0.0)

    @property
    def center(self):
        "Return center as a tuple"
        return self.as_tuple()

    def __mul__( self, scalar ):
        """Vector(x1*x2, y1*y2)"""
        return Actor(self.x*scalar, self.y*scalar, self.radius*scalar)

    def clone(self):
        return Actor(self.x, self.y, self.radius)

    def update_pos(self):
        self.slide(self.move_vector)

    def __repr__(self):
        return "Actor<C:%s,R:%r>" % (self.center,self.radius)

    def __str__(self):
        return self.__repr__()

    def has_escaped(self):
        (x,y) = self.a
        return x > CALC_RANGE or x < -CALC_RANGE or y > CALC_RANGE or y < -CALC_RANGE

    def calculate_acceleration(self, walls, actors):
        pass
