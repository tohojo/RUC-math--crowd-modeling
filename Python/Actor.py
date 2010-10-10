# vim:fileencoding=utf8

from Vector import Vector
import numpy

EPSILON = 10e-5
CALC_RANGE = 300

class Actor(Vector):

    def __init__(self, x, y, radius = 1.0, move_vector = Vector(0.6, 0.6)):
        Vector.__init__(self, x, y)
        self.radius = radius
        self.move_vector = move_vector

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

    def update_move_vector(self, walls, actors):
#        print [w.distance_to(self) for w in walls]
        bounced = False
        for w in walls:
            if w.distance_to(self) <= self.radius and \
                w.distance_to(self+self.move_vector) < w.distance_to(self):

                P = w.projection(self)

                proj_dir = P-self

                if not bounced:
                    self.update_direction(proj_dir, w)
                    bounced = True

        for a in actors:
            if a == self: continue
            if a.distance_to(self) <= (self.radius + a.radius) and \
                a.distance_to(self+self.move_vector) < a.distance_to(self):

                if not bounced:
                    self.update_direction(a, a)
                    bounced = True

    def update_direction(self, P, w):

        rads = P.angle(self.move_vector)

        if rads > numpy.pi/2:
            rads = numpy.pi- rads



#                print numpy.rad2deg(rads), proj_dir, self.move_vector

        rot = 2*rads


        # rotate the way that will make us move away from the wall
        if w.distance_to(self+self.move_vector.rotate(rot)) > w.distance_to(self):
            self.move_vector = self.move_vector.rotate(rot)
        else:
            self.move_vector = self.move_vector.rotate(-rot)



