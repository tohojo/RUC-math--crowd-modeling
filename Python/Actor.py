# vim:fileencoding=utf8

from Vector import Vector

class Actor(Vector):

    def __init__(self, center = (0.0, 0.0), radius = 1.0):
        Vector.__init__(self, center[0], center[1])
        self.radius = radius

    @property
    def center(self):
        "Return center as a tuple"
        return self.as_tuple()
