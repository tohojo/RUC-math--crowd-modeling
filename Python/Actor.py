# vim:fileencoding=utf8

from Vector import Vector, Point
import numpy

EPSILON = 10e-5
CALC_RANGE = 20

class Actor:

    def __init__(self, **kwargs):

        if kwargs.has_key("position"):
            self.position = kwargs["position"]
        else:
            self.position = Point(0.0, 0.0)

        if kwargs.has_key("radius"):
            self.radius = kwargs["radius"]
        else:
            self.radius = 0.2

        if kwargs.has_key("velocity"):
            self.velocity = kwargs["velocity"]
        else:
            self.velocity = Vector(1.0, 1.0)

        self.initial_velocity = self.velocity

        if kwargs.has_key("target"):
            self.target = kwargs["target"]
        else:
            self.target = Point(1.0, 1.0)

        self.acceleration = Vector(0.0,0.0)

    def __repr__(self):
        return "Actor<C:%s,R:%r,V:%r>" % (self.position,self.radius,self.velocity)

    def __str__(self):
        return self.__repr__()

    def has_escaped(self):
        (x,y) = self.position.as_tuple()
        return x > CALC_RANGE or x < -CALC_RANGE or y > CALC_RANGE or y < -CALC_RANGE

    def calculate_acceleration(self, walls, actors):
        self.acceleration = Vector(0.01, 0.0)

    def update_position(self, timestep):

        # Calculate displacement from acceleration and velocity
        delta_p = Vector(
                self.velocity.x * timestep + 0.5 * self.acceleration.x * timestep**2,
                self.velocity.y * timestep + 0.5 * self.acceleration.y * timestep**2)

        # Update position and velocity, and reset the acceleration
        self.position += delta_p
        self.velocity += self.acceleration

        self.acceleration = Vector(0.0, 0.0) # Not strictly necessary
