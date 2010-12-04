import optimised
import constants, setup
from drawing import Canvas
from plotting import Plots

import pprint
from datetime import datetime
from time import time
import os

class Scenario:
    """Parameters:
            'A'                  : A constant (see model)
            'B'                  : B constant (see model)
            'U'                  : U constant (see model)
            'lambda'             : lambda constant (see model)
            'initial_count'      : initial number of actors to spawn
            'start_areas'        : rectangles actors can spawn in (as quadruplets)
            'velocity_mean'      : mean value for initial actor velocity
            'velocity_deviation' : deviation for initial actor velocity
            'max_velocity_factor': max_velocity = initial_velocity * max_velocity_factor
            'radius_mean'        : mean value for radii
            'radius_deviation'   : deviation for radii
            'targets'            : list of targets actors should move towards (randomly 
                                   distributed between multiple targets)
            'density_rectangle'  : rectangle to measure density within (quadruplet)
            'flowrate_line'      : line to measure flow at (quadruplet start + end)
            'continuous_rate'    : rate to spawn actors throughout the simulation
            'continuous_start'   : lines to spawn new actors at. start line i will move
                                   towards target i
            'stop_at'            : time to end the simulation at
            'walls'              : list of wall quadruplets
            'drawing_width'      : width for drawing images
            'drawing_height'     : height for drawing images
            'pixel-factor'       : number of pixels pr metre
            'relax_time'         : relaxation time for actors
            'vary_parameters'    : dictionary of parameter names mapped to a tuple of
                                   interval start, interval end, stepsize for running
                                   multiple simulations varying each parameter"""

    def __init__(self, parameters = {}):
        self.parameters = parameters
        self.timestep = constants.timestep
        self.run_time = datetime.now()
        self.parameters['run_time'] = self.run_time.strftime("%Y-%m-%d %H:%M:%S")
        self.parameters['timestep'] = self.timestep

        self.create_images = False
        self.create_plots = False

    def run(self, options):
        optimised.set_parameters(self.parameters)
        self.options = options
        self.drawing = options.create_images or options.show_simulation

        self.time = 0.0
        self.frames = 0
        self.start_time = time()

        if self.drawing:
            self._init_drawing()
        if options.create_images:
            self._init_images()
        if options.create_plots:
            self._init_plots()

        self._create_actors()

        self._run()

    def _init_drawing(self):
        self.canvas = Canvas(
                self.parameters['drawing_width'],
                self.parameters['drawing_height'],
                self.parameters['pixel_factor'],
                os.path.join(constants.image_dir, self.parameters['name']),
                )

    def _uninit_drawing(self):
        self.canvas.quit()

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

    def _create_actors(self):
        for a in setup.generate_actors(self.parameters):
            optimised.add_actor(a)

    def _tick(self):
        if self.drawing:
            return self.canvas.tick(constants.framerate_limit) and not self._done()
        return not self._done()

    def _plot_sample(self):
        if not optimised.a_count:
            return
        (x1, y1, x2, y2) = self.parameters['density_rectangle']
        density = 0.0
        flow_count = 0
        velocities = list()
        for i in xrange(optimised.a_count):
            (x,y) = optimised.a_property(i, "position")
            r = optimised.a_property(i, "radius")
            velocities.append(optimised.a_property(i, "velocity"))
            if x+r >= x1 and x-r <= x2 and y+r >= y1 and y-r <= y2:
                density += 1
            if optimised.a_property(i, "flowline_time") > 0:
                flow_count += 1

        if self.time > 0:
            flowrate = flow_count/self.time
        else:
            flowrate = 0.0
        self.plots.add_sample(self.time, 
                density=density,
                velocities=velocities, 
                flowrate=flowrate)

    def _draw(self):
        self.canvas.clear_screen()
        for i in xrange(optimised.a_count):
            (x,y) = optimised.a_property(i, "position")
            r = optimised.a_property(i, "radius")
            self.canvas.draw_actor(x,y,r)

        self.canvas.draw_text("t = %.2f" % self.time, not self.create_images)
        for t in self.parameters['targets']:
            self.canvas.draw_target(*t)
        for w in self.parameters['walls']:
            self.canvas.draw_wall(w)
        if self.options.show_simulation:
            self.canvas.update()
        if self.create_images:
            self.canvas.create_image(self.frames)


    def _done(self):
        stop_at = self.parameters['stop_at']
        return (stop_at is not None and self.time >= stop_at) or not optimised.a_count

    def _run(self):
        try:
            while self._tick():

                optimised.update_actors()
                
                if self.drawing: 
                    self._draw()
                else:
                    output = "\r%d frames, t=%.2f" % (self.frames+1, self.time)
                    print output,

                if self.create_plots and not self.frames % self.sample_frequency:
                    self._plot_sample()

                self.time += self.timestep
                self.frames += 1


        except KeyboardInterrupt:
            pass
        print

        elapsed = time() - self.start_time
        print "%d frames in %f seconds. Avg %f fps" % (self.frames, elapsed,
                self.frames/elapsed)

        if self.drawing:
            self._uninit_drawing()

        if self.options.create_plots:
            self.plots.save(os.path.join(constants.plot_dir, self.parameters['name']))
