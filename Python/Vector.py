# vim:fileencoding=utf8

import math, numpy


class Vector:
    
    """A vector identified by coordinates (x,y).

    From http://wiki.python.org/moin/PointsAndRectangles
    
    supports: +, -, *, /, str, repr
    
    length  -- calculate length of vector to point from origin
    distance_to  -- calculate distance between two points
    as_tuple  -- construct tuple (x,y)
    clone  -- construct a duplicate
    integerize  -- convert x & y to integers
    floatize  -- convert x & y to floats
    move_to  -- reset x & y
    slide  -- move (in place) +dx, +dy, as spec'd by point
    slide_xy  -- move (in place) +dx, +dy
    rotate  -- rotate around the origin
    rotate_about  -- rotate around another point
    """
    
    def __init__(self, *args):
        if len(args) == 1:
            self.a = numpy.copy(args[0])
        elif len(args) == 2:
#            assert (type(args[0]) in (int, float) and type(args[1]) in (int,float))
            self.a = numpy.array((args[0],args[1]))

    @property
    def x(self):
        return self.a[0]

    @property
    def y(self):
        return self.a[1]

    def __add__(self, v):
        """Vector(x1+x2, y1+y2)"""
        return self.__class__(self.a+v.a)
    
    def __sub__(self, v):
        """Vector(x1-x2, y1-y2)"""
        return self.__class__(self.a-v.a)
    
    def __mul__( self, scalar ):
        """Vector(x1*x2, y1*y2)"""
        if type(scalar) != float and type(scalar) != int \
                and type(scalar) != numpy.float64:
            raise NotImplemented
        return self.__class__(self.a*scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __div__(self, scalar):
        """Vector(x1/x2, y1/y2)"""
        return self.__class__(self.a/scalar)
    
    def __str__(self):
        return "(%s, %s)" % (self.a[0], self.a[1])
    
    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.a[0], self.a[1])

    def dot(self, p):
        "Dot product between this and another point"
        return numpy.vdot(self.a, p.a)
    
    def length(self):
        return numpy.sqrt(numpy.sum(numpy.square(self.a)))
    
    def distance_to(self, p):
        """Calculate the distance between two points."""
        return (self - p).length()
    
    def as_tuple(self):
        """(x, y)"""
        return (self.a[0], self.a[1])
    
    def clone(self):
        """Return a full copy of this point."""
        return self.__class__(self.a)
    
    def move_to(self, x, y):
        """Reset x & y coordinates."""
        self.a[0] = x
        self.a[1] = y

    def normal(self):
        return self / self.length()
    
    def slide(self, p):
        '''Move to new (x+dx,y+dy).
        
        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.a += p.a
    
    def slide_xy(self, dx, dy):
        '''Move to new (x+dx,y+dy).
        
        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.a[0] += dx
        self.a[1] += dy

    def angle(self, v):
        return numpy.arccos(self.dot(v)/(self.length()*v.length()))


    def rotate(self, rad):
        """Rotate counter-clockwise by rad radians.
        
        Positive y goes *up,* as in traditional mathematics.
        
        Interestingly, you can use this in y-down computer graphics, if
        you just remember that it turns clockwise, rather than
        counter-clockwise.
        
        The new position is returned as a new Vector.
        """
        s, c = [f(rad) for f in (math.sin, math.cos)]
        x, y = (c*self.a[0] - s*self.a[1], s*self.a[0] + c*self.a[1])
        return self.__class__(x,y)
    
    def rotate_about(self, p, theta):
        """Rotate counter-clockwise around a point, by theta degrees.
        
        Positive y goes *up,* as in traditional mathematics.
        
        The new position is returned as a new Vector.
        """
        result = self.clone()
        result.slide(-p.x, -p.y)
        result.rotate(theta)
        result.slide(p.x, p.y)
        return result

    @staticmethod
    def projection_length(A, B, C):
        """Return the projection of a point on this vector.

        If the point is outside the vector, return the nearest end point."""

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

        AC = C-A
        AB = B-A
        return AC.dot(AB)/AB.length()

Point = Vector
