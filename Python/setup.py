# vim:fileencoding=utf8

import parameters as pm
import numpy, math, random

from Vector import Vector,Point
from Actor import Actor

if pm.random_seed is not None:
    numpy.random.seed(pm.random_seed)
    random.seed(pm.random_seed)

def generate_actors():
    """Generates a number of actors placed randomly within the
    area specified by the parameters, with parameters as specified
    in the parameters file"""

    actors = []

    num = pm.actor.initial_number
    target = Point(pm.actor.target[0], pm.actor.target[1])

    radii = numpy.random.normal(pm.actor.radius_mean, 
            pm.actor.radius_deviation, num)
    max_radius = max(radii)
    velocities = numpy.random.normal(pm.actor.velocity_mean, 
            pm.actor.velocity_deviation, num)

    # calculate grid cells for placement of actors
    grid_cell_size = max_radius*2+0.05
    grid = list()
    for r in pm.actor.initial_rectangles:
        (x1,y1,x2,y2) = r
        x_range = x2-x1
        y_range = y2-y1
        x_offset = (x_range % grid_cell_size)/2
        y_offset = (y_range % grid_cell_size)/2
        cells_x = int(math.floor(x_range / grid_cell_size))
        cells_y = int(math.floor(y_range / grid_cell_size))
        for i in xrange(cells_x):
            for j in xrange(cells_y):
                grid.append((i * grid_cell_size + x_offset + x1, 
                    j * grid_cell_size + y_offset + y1))

    if num > len(grid):
        print "Warning: asked to create %d actors, but only room for %d" % (num, len(grid))

    cells = random.sample(grid, min(num,len(grid)))

    for i in xrange(num):
        radius = radii[i]
        velocity = velocities[i]
        cell = cells[i]
        free_space_x = grid_cell_size - radius*2
        free_space_y = grid_cell_size - radius*2
        x_coord = random.random() * free_space_x + cell[0] + radius
        y_coord = random.random() * free_space_y + cell[1] + radius
        position = Point(x_coord, y_coord)
        velocity_v = (target-position).normalize()*velocity

        actors.append(Actor(
            position = position,
            desired_velocity = velocity,
            max_velocity = velocity * pm.actor.max_velocity_factor,
            target = target,
            radius = radius))

    return actors
