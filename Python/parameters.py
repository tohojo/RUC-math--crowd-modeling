# vim:fileencoding=utf8

from Vector import Vector, Point


timestep = 0.01
random_seed = 0

stop_at = None

create_images = False
image_prefix = "images/test-"

use_c_ext = True
use_threads = False

class constants:
    # From page 12 of the article
    a_2 = 3.0
    b_2 = 0.2

class actor:
    "Parameters related to actors"
    default_position = Point(0.0, 0.0)
    default_radius = 0.2
    default_velocity = Vector(1.0, 1.0)
    default_initial_desired_velocity = 0.5
    default_max_velocity = 3.0
    default_relax_time = 1.0
    default_target = Point(0.0, 10.0)

    initial_number = 100
    initial_x_range = (-10, 10)
    initial_y_range = (-10, 10)

    velocity_mean = 1.34
    velocity_deviation = 0.26

    max_speed = 1.3

    radius_mean = 0.2
    radius_deviation = 0.01

    target = (0,0)

walls = [   (-10, -10,  10, -10),
            (-10, -10, -10,  10),
            (-10,  10,  10,  10),
            ( 10, -10,  10,  10),]
