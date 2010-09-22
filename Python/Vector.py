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
    
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    
    def __add__(self, p):
        """Vector(x1+x2, y1+y2)"""
        return Vector(self.x+p.x, self.y+p.y)
    
    def __sub__(self, p):
        """Vector(x1-x2, y1-y2)"""
        return Vector(self.x-p.x, self.y-p.y)
    
    def __mul__( self, scalar ):
        """Vector(x1*x2, y1*y2)"""
        return Vector(self.x*scalar, self.y*scalar)
    
    def __div__(self, scalar):
        """Vector(x1/x2, y1/y2)"""
        return Vector(self.x/scalar, self.y/scalar)
    
    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)
    
    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def dot(self, p):
        "Dot product between this and another point"
        return numpy.dot((self.x, self.y), (p.x, p.y))
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def distance_to(self, p):
        """Calculate the distance between two points."""
        return (self - p).length()
    
    def as_tuple(self):
        """(x, y)"""
        return (self.x, self.y)
    
    def clone(self):
        """Return a full copy of this point."""
        return Vector(self.x, self.y)
    
    def integerize(self):
        """Convert co-ordinate values to integers."""
        self.x = int(self.x)
        self.y = int(self.y)
    
    def floatize(self):
        """Convert co-ordinate values to floats."""
        self.x = float(self.x)
        self.y = float(self.y)
    
    def move_to(self, x, y):
        """Reset x & y coordinates."""
        self.x = x
        self.y = y
    
    def slide(self, p):
        '''Move to new (x+dx,y+dy).
        
        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x = self.x + p.x
        self.y = self.y + p.y
    
    def slide_xy(self, dx, dy):
        '''Move to new (x+dx,y+dy).
        
        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x = self.x + dx
        self.y = self.y + dy


    def screen_coords(self, width, height, factor):

        self.x *= factor
        self.y *= -factor

        shift_w = width/2
        shift_h = height/2

        self.x += shift_w
        self.y += shift_h
    
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
        return Vector(x,y)
    
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
