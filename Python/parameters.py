# vim:fileencoding=utf8

from scenario import Scenario

scenarios = {
        'square_room': Scenario({
            'name'               : 'square_room',
            'A'                  : 9.0,
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
            'targets'            : [(0.0,6.0)],
            'density_rectangle'  : (-1.0, 3.0, 1.0, 5.0),
            'flowrate_line'      : (-1.0, 5.1, 1.0, 5.1),
            'continuous_rate'    : None,
            'continuous_start'   : [],
            'stop_at'            : None,
            'walls'              : [
                                    (-5.0, -5.0,  5.0, -5.0),
                                    (-5.0, -5.0, -5.0,  5.0),
                                    ( 5.0, -5.0,  5.0,  5.0),
                                    (-5.0,  5.0, -0.5,  5.0),
                                    ( 0.5,  5.0,  5.0,  5.0),
                                   ],
            'drawing_width'      : 450,
            'drawing_height'     : 450,
            'pixel_factor'       : 30,
            'relax_time'         : 1.0,
            'vary_parameters'    : {
                                    'A'            : (1.0, 3.0, 0.1),
                                    #'velocity_mean': (1.0, 5.0, 0.1),
                                   },
        }),
        'corridor': Scenario({
            'name'               : 'corridor',
            'A'                  : 2.2,
            'B'                  : 0.2,
            'U'                  : 2.0,
            'lambda'             : 0.1,
            'initial_count'      : 20,
            'start_areas'        : [
                                    (-10.0,-3.0,-1.0,3.0),
                                    (1.0,-3.0,10.0,3.0)
                                   ],
            'velocity_mean'      : 0.74,
            'velocity_deviation' : 0.26,
            'max_velocity_factor': 4.0,
            'radius_mean'        : 0.3,
            'radius_deviation'   : 0.01,
            'targets'            : [
                                    (500.0,0.0),
                                    (-500.0, 0.0)
                                   ],
            'density_rectangle'  : (-2.0, -3.0, 2.0, 3.0),
            'flowrate_line'      : (0.0, -3.0, 0.0, 3.0),
            'continuous_rate'    : 1,
            'continuous_start'   : [
                                    (-10.0, -2.5, -9.0, 2.5),
                                    (9.0, -2.5, 10.0, 2.5)
                                   ],
            'stop_at'            : None,
            'walls'              : [
                                    (-10.0,  3.0, 10.0,  3.0),
                                    (-10.0, -3.0, 10.0, -3.0),
                                   ],
            'drawing_width'      : 750,
            'drawing_height'     : 350,
            'pixel_factor'       : 30,
            'relax_time'         : 0.5,
            'vary_parameters'    : {
                                    'A'            : (4.0, 6.0, 0.01),
                                    #'velocity_mean': (1.0, 5.0, 0.1),
                                   },
        }),
}
