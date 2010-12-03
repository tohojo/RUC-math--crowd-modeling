# vim:fileencoding=utf8

from scenario import Scenario

scenarios = {
        'square_room': Scenario({
            'name'               : 'square_room',
            'A'                  : 2.2,
            'B'                  : 0.2,
            'U'                  : 2.0,
            'lambda'             : 0.1,
            'initial_count'      : 100,
            'start_areas'        : [(-5.0,-5.0,5.0,5.0)],
            'velocity_mean'      : 1.34,
            'velocity_deviation' : 0.26,
            'max_velocity_factor': 1.3,
            'radius_mean'        : 0.2,
            'radius_deviation'   : 0.01,
            'targets'            : [(0.0,7.0)],
            'density_rectangle'  : (-1.0, 3.0, 1.0, 5.0),
            'flowrate_line'      : (-1.0, 5.1, 1.0, 5.1),
            'continuous_rate'    : None,
            'continuous_start'   : [],
            'run_time'           : 60.0,
            'walls'              : [
                                    (-5.0, -5.0,  5.0, -5.0),
                                    (-5.0, -5.0, -5.0,  5.0),
                                    ( 5.0, -5.0,  5.0,  5.0),
                                    (-5.0,  5.0, -0.5,  5.0),
                                    ( 0.5,  5.0,  5.0,  5.0),
                                   ],
            'drawing_width'      : 600,
            'drawing_height'     : 600,
            'pixel_factor'       : 30,
            'relax_time'         : 1.0,
        }),
}
