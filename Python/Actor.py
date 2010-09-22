# vim:fileencoding=utf8

from Vector import Vector
import numpy

EPSILON = 10e-5

class Actor(Vector):

    def __init__(self, x, y, radius = 1.0):
        Vector.__init__(self, x, y)
        self.radius = radius
        self.move_vector = Vector(0.06, 0.06)

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

    def update_move_vector(self, walls):
#        print [w.distance_to(self) for w in walls]
        for w in walls:
            if w.distance_to(self) <= self.radius and \
                w.distance_to(self+self.move_vector) < w.distance_to(self):

                P = w.projection(self)

                proj_dir = P-self

                print proj_dir, self.move_vector

                rads = proj_dir.angle(self.move_vector)

#                if rads > numpy.pi/2:
#                    rads = numpy.pi- rads



                print rads, numpy.rad2deg(rads)

                rot = 2*rads


                # rotate the way that will make us move away from the wall
                if w.distance_to(self+self.move_vector.rotate(rot)) > w.distance_to(self):
                    self.move_vector = self.move_vector.rotate(rot)
                else:
                    self.move_vector = self.move_vector.rotate(-rot)



