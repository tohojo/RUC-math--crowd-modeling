import optimised
import constants, setup

from drawing import Canvas as image_canvas
from drawing_tikz import Canvas as tikz_canvas
from plotting import Plots

import pprint, os, random, math
from datetime import datetime
from time import time
import numpy as np

class Scenario:
    """Parameters:
            'A'                  : A constant (see model)
            'B'                  : B constant (see model)
            'U'                  : U constant (see model)
            'lambda'             : lambda constant (see model)
            'initial_count'      : initial number of pedestrians to spawn
            'start_areas'        : rectangles pedestrians can spawn in (as quadruplets)
            'velocity_mean'      : mean value for initial pedestrian velocity
            'velocity_deviation' : deviation for initial pedestrian velocity
            'max_velocity_factor': max_velocity = initial_velocity * max_velocity_factor
            'radius_mean'        : mean value for radii
            'radius_deviation'   : deviation for radii
            'targets'            : list of targets pedestrians should move towards (randomly 
                                   distributed between multiple targets)
            'density_rectangle'  : rectangle to measure density within (quadruplet)
            'flowrate_line'      : line to measure flow at (quadruplet start + end)
            'continuous_rate'    : rate to spawn pedestrians throughout the simulation
            'continuous_start'   : lines to spawn new pedestrians at. start line i will move
                                   towards target i
            'stop_at'            : time to end the simulation at
            'random_seed'        : seed for the random number generator
            'walls'              : list of wall quadruplets
            'drawing_width'      : width for drawing images
            'drawing_height'     : height for drawing images
            'pixel_factor'       : number of pixels pr metre
            'relax_time'         : relaxation time for pedestrians
            'vary_parameters'    : dictionary of parameter names mapped to a tuple of
                                   interval start, interval end, stepsize for running
                                   multiple simulations varying each parameter"""

    def __init__(self, parameters = {}):
        self.parameters = parameters
        if not "random_seed" in self.parameters:
            self.parameters["random_seed"] = constants.random_seed

        if not "flowrate_lines" in self.parameters:
            self.parameters["flowrate_lines"] = [self.parameters["flowrate_line"]] 

        self.timestep = constants.timestep
        self.run_time = datetime.now()
        self.parameters['run_time'] = self.run_time.strftime("%Y-%m-%d %H:%M:%S")
        self.parameters['timestep'] = self.timestep

        self.average_desired_velocity = 0.0
        self.spawn_count = 0.0

        self.create_images = False
        self.create_plots = False
        self.spawning = False

    def run(self, options):
        self.options   = options
        self.drawing   = options.create_images or options.show_simulation
        self.aggregate = options.aggregate

        if options.create_images:
            self._init_images()
        if options.create_plots:
            self._init_plots()

        if self.parameters['continuous_rate'] is not None:
            self.spawning = True

        if self.aggregate:
            self._run_aggregate()
        else:
            self._run()

    def _init_drawing(self):
        if self.options.show_simulation:
            self.show_canvas = image_canvas(
                    self.parameters['drawing_width'],
                    self.parameters['drawing_height'],
                    self.parameters['pixel_factor'],
                    os.path.join(constants.image_dir, self.parameters['name']),
                    )
        if self.options.create_images:
            if self.options.tikz:
                self.image_canvas = tikz_canvas(
                        self.parameters['drawing_width'],
                        self.parameters['drawing_height'],
                        self.parameters['pixel_factor'],
                        os.path.join(constants.image_dir, self.parameters['name']),
                        )
            else:
                if self.options.show_simulation:
                    self.image_canvas = self.show_canvas
                else:
                    self.image_canvas = image_canvas(
                            self.parameters['drawing_width'],
                            self.parameters['drawing_height'],
                            self.parameters['pixel_factor'],
                            os.path.join(constants.image_dir, self.parameters['name']),
                            )


    def _uninit_drawing(self):
        self._canvas("quit")

    def _init_images(self):
        pfile = open("%s-parameters" % os.path.join(constants.image_dir, 
            self.parameters['name']), "w")
        pfile.write(pprint.pformat(self.parameters))
        pfile.write("\n")
        pfile.close()
        self.create_images = True

    def _init_plots(self):
        self.sample_frequency = int(constants.plot_sample_frequency/self.timestep)
        self.plots = Plots(self.sample_frequency, self.parameters)
        self.create_plots = True
        self.plot_prefix = os.path.join(constants.plot_dir, self.parameters['name'])


    def _create_pedestrians(self):
        desired_velocities = []
        for a in setup.generate_pedestrians(self.parameters, 
                self.parameters['start_areas'], self.parameters['initial_count']):
            desired_velocities.append(a['initial_desired_velocity'])
            optimised.add_pedestrian(a)

        self.average_desired_velocity = np.average(desired_velocities)

    def _tick(self):
        if self.drawing:
            return self._canvas("tick", constants.framerate_limit)
        return True

    def _plot_sample(self):
        if not optimised.a_count:
            return
        (x1, y1, x2, y2) = self.parameters['density_rectangle']
        density_c = 0
        density = 0.0
        density_area = (y2-y1)*(x2-x1)
        velocities = list()
        for i in xrange(optimised.a_count):
            (x,y) = optimised.a_property(i, "position")
            r = optimised.a_property(i, "radius")
            velocities.append(optimised.a_property(i, "velocity"))
            if x+r >= x1 and x-r <= x2 and y+r >= y1 and y-r <= y2:
                density_c += 1

        flowrates = []
        for i in xrange(len(self.parameters["flowrate_lines"])):
            (x1,y1,x2,y2) = self.parameters["flowrate_lines"][i][:4]
            flow_length = math.sqrt((x2-x1)**2+(y2-y1)**2)
            flow_count = optimised.flow_count(i)
            flowrate = flow_count/constants.plot_sample_frequency/flow_length
            flowrates.append(flowrate)

        density = density_c / density_area
        self.plots.add_sample(self.time, 
                density=density,
                velocities=velocities, 
                flowrate=flowrates)

    def _canvas(self, method, *args):
        retval = True
        if self.options.create_images:
            retval = getattr(self.image_canvas, method)(*args)
        if self.options.show_simulation and (self.options.tikz or not self.options.create_images):
            return getattr(self.show_canvas, method)(*args) and retval
        return retval

    def _draw(self):
        self._canvas("clear_screen")
        for i in xrange(optimised.a_count):
            (x,y) = optimised.a_property(i, "position")
            r = optimised.a_property(i, "radius")
            t = optimised.a_property(i, "target")
            self._canvas("draw_pedestrian", x,y,r,t)

        self._canvas("draw_text", "t = %.2f" % self.time, not self.create_images)
        for t in self.parameters['targets']:
            self._canvas("draw_target", *t)
        for w in self.parameters['walls']:
            self._canvas("draw_wall", w)
        if self.options.show_simulation:
            self.show_canvas.update()
        if self.create_images:
            self.image_canvas.create_image(self.frames)

    def _aggregate(self, p_name, p_value):
        if self.create_plots:
            self.plots.add_aggregate(p_name, p_value, 
                    desired_velocity=self.average_desired_velocity,
                    leaving_time=self.time)

    def _spawn(self):
        spawn_rate = self.parameters['continuous_rate']
        self.spawn_count += self.timestep * spawn_rate
        spawn = 0
        while self.spawn_count > 1.0:
            spawn += 1
            self.spawn_count -= 1.0

        if spawn > 0:
            for a in setup.generate_pedestrians(self.parameters,
                    self.parameters['continuous_start'], spawn):
                optimised.add_pedestrian(a)


    def _done(self):
        stop_at = self.parameters['stop_at']
        return (stop_at is not None and self.time >= stop_at) or not optimised.a_count

    def _run_aggregate(self):
        for p in self.parameters['vary_parameters']:
            if not p in self.parameters:
                print "Cannot vary non-existing parameter: %s" % p
                return

            (start, stop, step) = self.parameters['vary_parameters'][p]
            print "Aggregate of %s values %.2f-%.2f" % (p, start, stop)
            orig_value = self.parameters[p]
            values = np.arange(start, stop+step, step)
            for v in values:
                print "%s=%.2f" % (p, v)
                self.parameters[p] = v
                success = self._run()
                if not success:
                    return
                self._aggregate(p,v)
            self.parameters[p] = orig_value

            if self.create_plots:
                self.plots.save_aggr(self.plot_prefix)
                self._init_plots()

    def _run(self):
        optimised.set_parameters(self.parameters)

        self.time = 0.0
        self.frames = 0
        self.start_time = time()

        if self.parameters["random_seed"] is not None:
            np.random.seed(self.parameters["random_seed"])
            random.seed(self.parameters["random_seed"])

        self._create_pedestrians()

        if self.drawing:
            self._init_drawing()

        success = False

        try:
            while self._tick():

                optimised.update_pedestrians()

                if self.spawning:
                    self._spawn()
                
                if self.drawing: 
                    self._draw()
                else:
                    output = "\r%d frames, t=%.2f" % (self.frames+1, self.time)
                    print output,

                if self.create_plots and not self.frames % self.sample_frequency:
                    self._plot_sample()

                self.time += self.timestep
                self.frames += 1

                if self._done():
                    success = True
                    break

        except KeyboardInterrupt:
            pass
        print

        elapsed = time() - self.start_time
        print "%d frames in %f seconds. Avg %f fps" % (self.frames, elapsed,
                self.frames/elapsed)

        if self.drawing:
            self._uninit_drawing()

        if self.options.create_plots and not self.aggregate:
            self.plots.save(self.plot_prefix)

        return success
