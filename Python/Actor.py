# vim:fileencoding=utf8

from Vector import Vector, Point
import numpy
import parameters as pm

EPSILON = 10e-5
CALC_RANGE = 20

class Actor:

    def __init__(self, **kwargs):

        if kwargs.has_key("position"):
            self.position = kwargs["position"]
        else:
            self.position = pm.actor.default_position.clone()

        self.initial_position = self.position

        if kwargs.has_key("radius"):
            self.radius = kwargs["radius"]
        else:
            self.radius = pm.actor.default_radius

        if kwargs.has_key("velocity"):
            self.velocity = kwargs["velocity"]
        else:
            self.velocity = pm.actor.default_velocity.clone()

        if kwargs.has_key("desired_velocity"):
            self.initial_desired_velocity = kwargs["desired_velocity"]
        else:
            self.initial_desired_velocity = pm.actor.default_initial_desired_velocity

        if kwargs.has_key("max_velocity"):
            self.max_velocity = kwargs["max_velocity"]
        else:
            self.max_velocity = pm.actor.default_max_velocity

        if kwargs.has_key("relax_time"):
            self.relax_time = kwargs["relax_time"]
        else:
            self.relax_time = pm.actor.default_relax_time

        self.initial_velocity = self.velocity

        if kwargs.has_key("target"):
            self.target = kwargs["target"]
        else:
            self.target = pm.actor.default_target.clone()

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

        repelling_forces = list()

        for b in actors:
            if self == b:
                continue
            radius_sum = b.radius + self.radius
            distance = self.position.distance_to(b.position)


            norm_vector = (self.position-b.position).normal()

            print radius_sum - distance

            repelling_forces.append(norm_vector * pm.constants.a_2 * \
                    numpy.exp((radius_sum-distance)/pm.constants.b_2))

        self.acceleration = desired_acceleration

        for f in repelling_forces:
            self.acceleration += f


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
