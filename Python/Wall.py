# vim:fileencoding=utf8

import numpy, math
from Vector import Vector

class Wall:

    def __init__(self, start, end):
        "Start and end are Vectors"
        self.start = start
        self.end = end

    def distance_to(self, p):
        """The shortest distance from the wall to point p."""
        #    From http://www.codeguru.com/forum/showthread.php?t=194400:
        #
        #    Let the point be C (Cx,Cy) and the line be AB (Ax,Ay) to (Bx,By).
        #    Let P be the point of perpendicular projection of C on AB.  The parameter
        #    r, which indicates P's position along AB, is computed by the dot product 
        #    of AC and AB divided by the square of the length of AB:

        #        (1)     AC dot AB
        #            r = ---------  
        #                ||AB||^2

        #    r has the following meaning:

        #    r=0      P = A
        #    r=1      P = B
        #    r<0      P is on the backward extension of AB
        #    r>1      P is on the forward extension of AB
        #    0<r<1    P is interior to AB


        #    The point P can then be found:

        #    Px = Ax + r(Bx-Ax)
        #    Py = Ay + r(By-Ay)

        #    And the distance from A to P = r*L."""

        AC = p-self.start
        AB = self.end-self.start
        r = AC.dot(AB)/self.length()**2


        if r > 1:
            # The point p is past the end of the wall
            return p.distance_to(self.end)
        if r < 0:
            # The point p is past the beginning of the wall
            return p.distance_to(self.start)

        P = Vector(self.start.x + r*(self.end.x-self.start.x),
                self.start.y + r*(self.end.y-self.start.y))

        return P.distance_to(p)

        
    def length(self):
        return self.start.distance_to(self.end)

if __name__ == "__main__":
    p = Vector(12,-2)
    w = Wall(Vector(-1,-2), Vector(1,-2))
    print w.distance_to(p)
