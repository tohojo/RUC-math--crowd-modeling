# vim:fileencoding=utf8

from scenario import Scenario

scenarios = {
        'square_room': Scenario({
            'name'               : 'square_room',
            'A'                  : 8.0,
            'B'                  : 0.2,
            'U'                  : 8.0,
            'lambda'             : 1.0,
            'initial_count'      : 65,
            'start_areas'        : [(-5.0,-5.0,5.0,5.0)],
            'velocity_mean'      : 2.0,
            'velocity_deviation' : 0.26,
            'max_velocity_factor': 1.3,
            'radius_mean'        : 0.2,
            'radius_deviation'   : 0.01,
            'targets'            : [(0.0,6.0)],
            'density_rectangle'  : (-1.0, 3.0, 1.0, 5.0),
            'flowrate_lines'     : [
                                        (-1.0, 5.1, 1.0, 5.1, "outside door"), 
                                        (-1.0, 4.9, 1.0, 4.9, "inside door"),
                                   ],
            'continuous_rate'    : None,
            'continuous_start'   : [],
            'stop_at'            : 10,
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
        'corridorbidirec': Scenario({
            'name'               : 'corridor',
            'A'                  : 8.0,
            'B'                  : 0.2,
            'U'                  : 12.0,
            'lambda'             : 1.0,
            'initial_count'      : 1,
            'start_areas'        : [
                                    (-10.0,-1.0,-1.0,1.0),
                                    (1.0,-1.0,10.0,1.0),
                                   ],
            'velocity_mean'      : 2.0,
            'velocity_deviation' : 0.26,
            'max_velocity_factor': 6.0,
            'radius_mean'        : 0.2,
            'radius_deviation'   : 0.01,
            'targets'            : [
                                    (500.0,0.0),
                                    (-500.0, 0.0)
                                   ],
            'density_rectangle'  : (-1.0, -.0, 1.0, 3.0),
            'flowrate_line'      : (0.0, -3.0, 0.0, 3.0),
            'continuous_rate'    : 10,
            'continuous_start'   : [
                                    (-10.0, -1.0, -9.0, 1.0),
                                    (9.0, -1.0, 10.0, 1.0),
                                   ],
            'stop_at'            : 50,
            'walls'              : [
                                    (-10.0,  1.0, 10.0,  1.0),
                                    (-10.0, -1.0, 10.0, -1.0)
                                   ],
            'drawing_width'      : 750,
            'drawing_height'     : 350,
            'pixel_factor'       : 30,
            'relax_time'         : 0.5,
            'vary_parameters'    : {
                                    #'A'            : (4.0, 6.0, 0.01),
                                    'velocity_mean': (1.5, 5.0, 0.5),
                                   },
        }),

        'corridorunidirec': Scenario({
            'name'               : 'corridor',
            'A'                  : 12.0,
            'B'                  : 0.2,
            'U'                  : 12.0,
            'lambda'             : 1.0,
            'initial_count'      : 1,
            'start_areas'        : [
                                    (-10.0,-0.7,-1.0,0.7),
                                   ],
            'velocity_mean'      : 2.0,
            'velocity_deviation' : 0.26,
            'max_velocity_factor': 3.0,
            'radius_mean'        : 0.2,
            'radius_deviation'   : 0.01,
            'targets'            : [
                                    (500.0,0.0),
                                    (-500.0, 0.0)
                                   ],
            'density_rectangle'  : (-1.0, -0.8, 1.0, 0.8),
            'flowrate_line'      : (11.0, -3.0, 11.0, 3.0),
            'continuous_rate'    : 10,
            'continuous_start'   : [
                                    (-10.0, -0.7, -9.0, 0.7),
                                   ],
            'stop_at'            : 75,
            'walls'              : [
                                    (-10.0,  1.0, 10.0,  1.0),
                                    (-10.0, -1.0, 10.0, -1.0)
                                   ],
            'drawing_width'      : 750,
            'drawing_height'     : 350,
            'pixel_factor'       : 30,
            'relax_time'         : 0.1,
            'vary_parameters'    : {
                                    #'A'            : (4.0, 6.0, 0.01),
                                    'velocity_mean': (1.5, 5.0, 0.5),
                                   },
        }),

        'widekinksbidirec': Scenario({
            'name'               : 'corridor',
            'A'                  : 12.0,
            'B'                  : 0.2,
            'U'                  : 12.0,
            'lambda'             : 1.0,
            'initial_count'      : 1,
            'start_areas'        : [
                                    (-10.0,-1.0,-1.0,1.0),
                                    (1.0,-1.0,10.0,1.0)
                                   ],
            'velocity_mean'      : 2.0,
            'velocity_deviation' : 0.5,
            'max_velocity_factor': 3.0,
            'radius_mean'        : 0.2,
            'radius_deviation'   : 0.01,
            'targets'            : [
                                    (500.0,0.0),
                                    (-500.0, 0.0)
                                   ],
            'density_rectangle'  : (-1.0, -0.8, 1.0, 0.8),
            'flowrate_line'      : (0.0, -1.0, 0.0, 1.0),
            'continuous_rate'    : 7,
            'continuous_start'   : [
                                    (-10.0, -0.7, -9.0, 0.7),
                                    (9.0, -0.7, 10.0, 0.7)
                                   ],
            'stop_at'            : 60,
            'walls'              : [
                                    (-10.0,  0.7, -5.0,  0.7),
                                    (-10.0, -0.7, -5.0, -0.7),
                                    (-5.0,  0.7, 0.0,  3.0),
                                    (-5.0, -0.7, 0.0, -3.0),
                                    (0.0,  3.0, 5.0,  0.7),
                                    (0.0, -3.0, 5.0, -0.7),
                                    (5.0,  0.7, 10.0,  0.7),
                                    (5.0, -0.7, 10.0, -0.7),
                                   ],
            'drawing_width'      : 750,
            'drawing_height'     : 350,
            'pixel_factor'       : 30,
            'relax_time'         : 0.1,
            'vary_parameters'    : {
                                    #'A'            : (4.0, 6.0, 0.01),
                                    'velocity_mean': (1.5, 5.0, 0.5),
                                   },
        }),
        'widekinksunidirec': Scenario({
            'name'               : 'corridor',
            'A'                  : 12.0,
            'B'                  : 0.2,
            'U'                  : 12.0,
            'lambda'             : 1.0,
            'initial_count'      : 1,
            'start_areas'        : [
                                    (-10.0,-1.0,-1.0,1.0),
                                   ],
            'velocity_mean'      : 2.0,
            'velocity_deviation' : 0.5,
            'max_velocity_factor': 3.0,
            'radius_mean'        : 0.2,
            'radius_deviation'   : 0.01,
            'targets'            : [
                                    (500.0,0.0),
                                    (-500.0, 0.0)
                                   ],
            'continuous_rate'    : 10,
            'density_rectangle'  : (-1.0, -3.0, 1.0, 3.0),
            'flowrate_line'      : (0.0, -1.0, 0.0, 1.0),
            'continuous_start'   : [
                                    (-10.0,-1.0,-9.0,1.0),
                                    ],
            'stop_at'            : 60,
            'walls'              : [
                                    (-10.0,  1.0, -5.0,  1.0),
                                    (-10.0, -1.0, -5.0, -1.0),
                                    (-5.0,  1.0, 0.0,  3.0),
                                    (-5.0, -1.0, 0.0, -3.0),
                                    (0.0,  3.0, 5.0,  1.0),
                                    (0.0, -3.0, 5.0, -1.0),
                                    (5.0,  1.0, 10.0,  1.0),
                                    (5.0, -1.0, 10.0, -1.0),
                                   ],
            'drawing_width'      : 750,
            'drawing_height'     : 350,
            'pixel_factor'       : 30,
            'relax_time'         : 0.1,
            'vary_parameters'    : {
                                    #'A'            : (4.0, 6.0, 0.01),
                                    'velocity_mean': (1.5, 5.0, 0.5),
                                   },
        }),

        'bottleneckbidirec': Scenario({
            'name'               : 'corridor',
            'A'                  : 12.0,
            'B'                  : 0.2,
            'U'                  : 22.0,
            'lambda'             : 1.0,
            'initial_count'      : 1,
            'start_areas'        : [
                                    (-10.0,-1.0,-1.0,1.0),
                                    (1.0,-1.0,10.0,1.0)
                                   ],
            'velocity_mean'      : 2.0,
            'velocity_deviation' : 0.26,
            'max_velocity_factor': 3.0,
            'radius_mean'        : 0.2,
            'radius_deviation'   : 0.01,
            'targets'            : [
                                    (500.0,0.0),
                                    (-500.0, 0.0)
                                   ],
            'density_rectangle'  : (-1.0, -0.8, 1.0, 0.8),
            'flowrate_lines'      : [
                                    (-11.0, -3.0, -11.0, 3.0,"Left flow"),     
                                    (11.0, -3.0, 11.0, 3.0,"Right flow"),
                                    ],
            'continuous_rate'    : 10,
            'continuous_start'   : [
                                    (-10.0, -1.0, -9.0, 1.0),
                                    (9.0, -1.0, 10.0, 1.0)
                                   ],
            'stop_at'            : 300,
            'walls'              : [
                                    (-10.0,  3.0, -5.0,  3.0),
                                    (-10.0, -3.0, -5.0, -3.0),
                                    (-5.0,  3.0, 0.0,  0.5),
                                    (-5.0, -3.0, 0.0, -0.5),
                                    (0.0,  0.5, 5.0,  3.0),
                                    (0.0, -0.5, 5.0, -3.0),
                                    (5.0,  3.0, 10.0,  3.0),
                                    (5.0, -3.0, 10.0, -3.0),
                                   ],
            'drawing_width'      : 750,
            'drawing_height'     : 350,
            'pixel_factor'       : 30,
            'relax_time'         : 0.1,
            'vary_parameters'    : {
                                    #'A'            : (4.0, 6.0, 0.01),
                                    'velocity_mean': (1.0, 4.0, 0.5),
                                   },
        }),

        'bottleneckunidirec': Scenario({
            'name'               : 'bottleneck',
            'A'                  : 12.0,
            'B'                  : 0.2,
            'U'                  : 12.0,
            'lambda'             : 1.0,
            'initial_count'      : 1,
            'start_areas'        : [
                                    (-10.0,-1.0,-1.0,1.0),
                                   ],
            'velocity_mean'      : 2.0,
            'velocity_deviation' : 0.26,
            'max_velocity_factor': 3.0,
            'radius_mean'        : 0.2,
            'radius_deviation'   : 0.01,
            'targets'            : [
                                    (500.0,0.0),
                                    (-500.0, 0.0)
                                   ],
            'density_rectangle'  : (-1.0, -0.8, 1.0, 0.8),
            'flowrate_line'      : (-11.0, -3.0, 11.0, 3.0),
            'continuous_rate'    : 10,
            'continuous_start'   : [
                                    (-10.0, -1.0, -9.0, 1.0),
                                   ],
            'stop_at'            : 75,
            'walls'              : [
                                    (-10.0,  3.0, -5.0,  3.0),
                                    (-10.0, -3.0, -5.0, -3.0),
                                    (-5.0,  3.0, 0.0,  0.5),
                                    (-5.0, -3.0, 0.0, -0.5),
                                    (0.0,  0.5, 5.0,  3.0),
                                    (0.0, -0.5, 5.0, -3.0),
                                    (5.0,  3.0, 10.0,  3.0),
                                    (5.0, -3.0, 10.0, -3.0),
                                   ],
            'drawing_width'      : 750,
            'drawing_height'     : 350,
            'pixel_factor'       : 30,
            'relax_time'         : 0.1,
            'vary_parameters'    : {
                                    #'A'            : (4.0, 6.0, 0.01),
                                    'velocity_mean': (1.5, 5.0, 0.5),
                                   },
        }),
}

for i in scenarios:
    scenarios[i].parameters["name"] = i
