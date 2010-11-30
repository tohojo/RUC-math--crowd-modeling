# vim:fileencoding=utf8

from Vector import Vector, Point


timestep = 0.01
random_seed = 0

stop_at = 60.0

show_simulation = True
create_plots = False

create_images = False
image_prefix = "images/test-"

use_c_ext = True
use_threads = False

framerate_limit = 0

class constants:
    # From page 12 of the article
    a_1 = 4.0
    b_1 = 0.2
    a_2 = 4.0
    b_2 = 0.2
    u = 5.0
    lmbda = 0.75

class actor:
    "Parameters related to actors"
    default_position = Point(0.0, 0.0)
    default_radius = 0.2
    default_velocity = Vector(0.0, 0.0)
    default_initial_desired_velocity = 0.5
    default_max_velocity = 3.0
    default_relax_time = 1.0
    default_target = Point(0.0, 10.0)

    initial_number = 100
    initial_rectangles = ((-5,-5,5,5),)

    velocity_mean = 1.34
    velocity_deviation = 0.26

    # max velocity is set from desired velocity * this factor
    max_velocity_factor = 1.3

    radius_mean = 0.2
    radius_deviation = 0.01

    target = (0,7)

class plot:
    sample_frequency = 0.05

    density_rectangle = (-1,3,1,5)
    flowrate_line = (-1, 5.1, 1, 5.1)

walls = [   (-5, -5,  5, -5),
            (-5, -5, -5,  5),
            ( 5, -5,  5,  5),
            (-5,  5,  -0.5,  5),
            (0.5,  5,  5,  5),
        ]


# Bookkeeping for saving parameters

from datetime import datetime
run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
del Vector, Point, datetime

params = dict()

for k in globals().keys():
    if not k.startswith("__") and k != "params":
        class x: pass
        if type(globals()[k]) == type(x):
            params[k] = dict()
            for i in dir(globals()[k]):
                if not i.startswith("__"):
                    params[k][i] = getattr(globals()[k], i)
        else:
            params[k] = globals()[k]

del k,i
