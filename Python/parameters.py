# vim:fileencoding=utf8

from Vector import Vector, Point


timestep = 0.02

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

