# vim:fileencoding=utf8

import parameters as pm
import numpy

from Vector import Vector,Point
from Actor import Actor

if pm.random_seed is not None:
    numpy.random.seed(pm.random_seed)

def generate_actors():
    """Generates a number of actors placed randomly within the
    area specified by the parameters, with parameters as specified
    in the parameters file"""

    actors = []

    num = pm.actor.initial_number
    x_range = pm.actor.initial_x_range
    y_range = pm.actor.initial_y_range
    target = Point(pm.actor.target[0], pm.actor.target[1])

    x_range_size = x_range[1] - x_range[0]
    y_range_size = y_range[1] - y_range[0]

    radii = numpy.random.normal(pm.actor.radius_mean, 
            pm.actor.radius_deviation, num)
    velocities = numpy.random.normal(pm.actor.velocity_mean, 
            pm.actor.velocity_deviation, num)
    x_coords = numpy.random.rand(num)
    y_coords = numpy.random.rand(num)


    for i in xrange(num):
        radius = radii[i]
        velocity = velocities[i]
        x_coord = x_coords[i] * x_range_size + x_range[0]
        y_coord = y_coords[i] * y_range_size + y_range[0]
        if abs(x_coord - x_range[0]) < radius:
            x_coord = x_range[0] + radius
        if abs(x_coord - x_range[1]) < radius:
            x_coord = x_range[1] - radius
        if abs(y_coord - y_range[0]) < radius:
            y_coord = y_range[0] + radius
        if abs(y_coord - y_range[1]) < radius:
            y_coord = y_range[1] - radius
        position = Point(x_coord, y_coord)

        actors.append(Actor(
            position = position,
            desired_velocity = velocity,
            target = target,
            radius = radius))

    return actors
