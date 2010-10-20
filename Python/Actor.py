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

        self.initial_position = self.position

        if kwargs.has_key("radius"):
            self.radius = kwargs["radius"]
        else:
            self.radius = 0.2

        if kwargs.has_key("velocity"):
            self.velocity = kwargs["velocity"]
        else:
            self.velocity = Vector(1.0, 1.0)

        if kwargs.has_key("desired_velocity"):
            self.initial_desired_velocity = kwargs["desired_velocity"]
        else:
            self.initial_desired_velocity = 0.5

        if kwargs.has_key("max_velocity"):
            self.max_velocity = kwargs["max_velocity"]
        else:
            self.max_velocity = 3.0

        if kwargs.has_key("relax_time"):
            self.relax_time = kwargs["relax_time"]
        else:
            self.relax_time = 1.0

        self.initial_velocity = self.velocity

        if kwargs.has_key("target"):
            self.target = kwargs["target"]
        else:
            self.target = Point(0.0, 10.0)

        self.acceleration = Vector(0.0,0.0)
        self.time = 0.0

    def __repr__(self):
        return "Actor<C:%s,R:%r,V:%r>" % (self.position,self.radius,self.velocity)

    def __str__(self):
        return self.__repr__()

    def has_escaped(self):
        (x,y) = self.position.as_tuple()
        return x > CALC_RANGE or x < -CALC_RANGE or y > CALC_RANGE or y < -CALC_RANGE

    def calculate_acceleration(self, walls, actors):

        # To compute the impatience factor, we need the average velocity,
        # in the direction of desired movement.
        #
        # This is found by projecting the direction we have moved onto the
        # vector from the initial position to the target and computing the
        # distance from this projection. The distance travelled is then
        # converted to an average velocity my dividing with the time
        if self.time == 0.0:
            average_velocity = 0.0
        else:
            proj = Vector.projection_length(
                       self.initial_position, self.target, self.position)


            average_velocity = proj / self.time

        # The impatience factor is given by the average velocity divided
        # by the *initial* desired velocity. (6) in the article
        impatience = 1.0 - average_velocity / self.initial_desired_velocity

        # (5) in the article
        desired_velocity = (1.0-impatience) * self.initial_desired_velocity + \
                impatience * self.max_velocity

        towards_target = (self.target - self.position).normal()

        desired_acceleration = (1.0/self.relax_time) * \
                (desired_velocity * towards_target - self.velocity)

        self.acceleration = desired_acceleration


    def update_position(self, timestep):

        # Calculate displacement from acceleration and velocity
        delta_p = Vector(
                self.velocity.x * timestep + 0.5 * self.acceleration.x * timestep**2,
                self.velocity.y * timestep + 0.5 * self.acceleration.y * timestep**2)

        # Update position and velocity, and reset the acceleration
        self.position += delta_p
        self.velocity += self.acceleration
        self.time += timestep

        self.acceleration = Vector(0.0, 0.0) # Not strictly necessary
