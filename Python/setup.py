# vim:fileencoding=utf8

import constants
import numpy, math, random

def generate_pedestrians(parameters, start_areas, num):
    """Generates a number of pedestrians placed randomly within the
    area specified by the parameters, with parameters as specified
    in the parameters file"""

    pedestrians = []

    targets = parameters['targets']

    radii = numpy.random.normal(parameters['radius_mean'], 
            parameters['radius_deviation'], num)
    max_radius = max(radii)
    velocities = numpy.random.normal(parameters['velocity_mean'], 
            parameters['velocity_deviation'], num)

    (v_max, v_min) = (max(velocities), min(velocities))
    if abs(v_max-v_min) > 3*parameters['velocity_deviation']:
        print "Warning: Large velocity deviation (%.3f, min: %.3f, max: %.3f)" % (
                abs(v_max-v_min), v_min, v_max)


    # calculate grid cells for placement of pedestrians
    grid_cell_size = max_radius*2+0.05
    grid = list()
    for i in xrange(len(start_areas)):
        (x1,y1,x2,y2) = start_areas[i]
        t = parameters['targets'][i]
        x_range = x2-x1
        y_range = y2-y1
        x_offset = (x_range % grid_cell_size)/2
        y_offset = (y_range % grid_cell_size)/2
        cells_x = int(math.floor(x_range / grid_cell_size))
        cells_y = int(math.floor(y_range / grid_cell_size))
        for i in xrange(cells_x):
            for j in xrange(cells_y):
                grid.append((i * grid_cell_size + x_offset + x1, 
                    j * grid_cell_size + y_offset + y1, t))

    if num > len(grid):
        print "Warning: asked to create %d pedestrians, but only room for %d" % (num, len(grid))

    cells = random.sample(grid, min(num,len(grid)))

    for i in xrange(len(cells)):
        radius = radii[i]
        velocity = velocities[i]
        cell = cells[i]
        free_space_x = grid_cell_size - radius*2
        free_space_y = grid_cell_size - radius*2
        x_coord = random.random() * free_space_x + cell[0] + radius
        y_coord = random.random() * free_space_y + cell[1] + radius
        position = (x_coord, y_coord)
        target = cell[2]

        pedestrians.append(dict(
            position = position,
            initial_position = position,
            acceleration = (0.0, 0.0),
            initial_desired_velocity = velocity,
            velocity = (0.0, 0.0),
            time = 0.0,
            relax_time = parameters['relax_time'],
            max_velocity = velocity * parameters['max_velocity_factor'],
            target = target,
            radius = radius))

    return pedestrians
