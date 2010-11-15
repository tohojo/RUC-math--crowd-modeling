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
            (self.x, self.y) = args[0]
        elif len(args) == 2:
#            assert (type(args[0]) in (int, float) and type(args[1]) in (int,float))
            self.x = args[0]
            self.y = args[1]

    def __add__(self, v):
        """Vector(x1+x2, y1+y2)"""
        return self.__class__(self.x+v.x, self.y+v.y)

    def __iadd__(self, v):
        """Vector(x1+x2, y1+y2)"""
        self.x += v.x
        self.y += v.y
        return self
    
    def __sub__(self, v):
        """Vector(x1-x2, y1-y2)"""
        return self.__class__(self.x-v.x, self.y-v.y)

    def __isub__(self, v):
        self.x -= v.x
        self.y -= v.y
        return self
    
    def __mul__( self, scalar ):
        """Vector(x1*x2, y1*y2)"""
        return self.__class__(self.x*scalar, self.y*scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self
    
    def __div__(self, scalar):
        """Vector(x1/x2, y1/y2)"""
        return self.__class__(self.x/scalar, self.y/scalar)

    def __idiv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        return self
    
    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)
    
    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def dot(self, p):
        "Dot product between this and another point"
        return numpy.vdot((self.x, self.y), (p.x, p.y))
    
    def length(self):
        return numpy.sqrt(self.x**2 + self.y**2)
    
    def distance_to(self, p):
        """Calculate the distance between two points."""
        return (self - p).length()
    
    def as_tuple(self):
        """(x, y)"""
        return (self.x, self.y)
    
    def clone(self):
        """Return a full copy of this point."""
        return self.__class__(self.x, self.y)
    
    def move_to(self, x, y):
        """Reset x & y coordinates."""
        self.x = x
        self.y = y

    def normal(self):
        """Return a normalized version of this vector"""
        return self / self.length()

    def normalize(self, l = None):
        """Normalize this vector in-place, using an optional pre-calculated
        length. Optimization of the normal() method. Returns self to allow
        for drop-in replacement of normal()"""
        if l is None:
            l = self.length()
        self.x /= l
        self.y /= l

        return self
    
    def slide(self, p):
        '''Move to new (x+dx,y+dy).
        
        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x += p.x
        self.y += p.y
    
    def slide_xy(self, dx, dy):
        '''Move to new (x+dx,y+dy).
        
        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x += dx
        self.y += dy

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
        x, y = (c*self.x - s*self.y, s*self.x + c*self.y)
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
