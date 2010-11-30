#!/usr/bin/python2
# vim:fileencoding=utf8


from drawing import Canvas
from Actor import Actor
from Wall import Wall
from Vector import Vector, Point
import setup
import parameters as pm
from threadworkers import run_in_threads
from time import time

if pm.use_c_ext:
    import optimised

import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--show-simulation", 
        default=pm.show_simulation, action="store_true", dest="show_simulation",
        help="show the simulation while running")
parser.add_option("-S", "--hide-simulation", 
        action="store_false", dest="show_simulation",
        help="hide the simulation while running")
parser.add_option("-i", "--create-images",
        default=pm.create_images, action="store_true", dest="create_images",
        help="store images of each frame")
parser.add_option("-I", "--no-create-images",
        action="store_false", dest="create_images",
        help="do not store images of each frame")
parser.add_option("-p", "--create-plots",
        default=pm.create_plots, action="store_true", dest="create_plots",
        help="create plots")
parser.add_option("-P", "--no-create-plots",
        action="store_false", dest="create_plots",
        help="do not create plots")
parser.add_option("", "--trace",
        action="store_true", dest="trace", default=False,
        help="enable trace when drawing")
parser.add_option("", "--profile",
        action="store_true", dest="profile", default=False,
        help="enable profiling of code")


def main(options):

    drawing = options.create_images or options.show_simulation

    def tick():
        return True

    if drawing:
        canvas = Canvas()
        canvas.clear_screen()
        tick = canvas.tick

    actors = setup.generate_actors()
    walls = [Wall(*i) for i in pm.walls]

    if pm.use_c_ext:
        optimised.add_actors(actors)

    timestep = pm.timestep
    timer = 0.0
    time_start = time()
    frames = 0

    if options.create_images:
        import pprint
        pfile = open("%sparameters" % pm.image_prefix, "w")
        pfile.write(pprint.pformat(pm.params))
        pfile.write("\n")
        pfile.close()

    if options.create_plots:
        sample_frequency = int(pm.plot.sample_frequency/timestep)
        densities = list()

    try:
        while tick():
            
            if drawing and not options.trace:
                canvas.clear_screen()

            if pm.use_c_ext:
                optimised.update_actors()
                actor_coords = optimised.get_actors()
                if drawing:
                    canvas.draw_actors(actor_coords)
            else:
                actor_coords = list()
                for a in actors:
                    a.calculate_acceleration(walls, actors)

                for a in actors:
                    a.update_position(timestep)
                    if a.has_escaped():
                        actors.remove(a)
                        continue
                    
                    actor_coords.append((a.position.x, a.position.y, a.radius,
                        a.velocity.length()))

                    if drawing:
                        canvas.draw_actor(a)

            

            if options.create_plots and not frames % sample_frequency:
                (x1, y1, x2, y2) = pm.plot.density_rectangle
                density = 0.0
                for (x,y,r,v) in actor_coords:
                    if x+r >= x1 and x-r <= x2 and y+r >= y1 and y-r <= y2:
                        density += 1
                densities.append(density)

            timer += timestep
            frames += 1

            if drawing:
                canvas.draw_text("t = %.2f" % timer, options.create_images)
                canvas.draw_target(pm.actor.target)
                for w in walls:
                    canvas.draw_wall(w)
                if options.show_simulation:
                    canvas.update(frames)
                if options.create_images:
                    canvas.create_image()
            else:
                output = "\r%d frames, t=%.2f" % (frames, timer)
                print output,

            if pm.stop_at is not None and timer >= pm.stop_at:
                break
    except KeyboardInterrupt:
        print

    if options.create_plots:
        import matplotlib.pyplot as plt
        import numpy as np
        t = np.arange(0.0, timer, pm.plot.sample_frequency)
        plt.plot(t, densities)
        plt.xlabel("t")
        plt.ylabel("actors in area")
        plt.title("Density")
        plt.show()

    elapsed = time() - time_start
    print "%d frames in %f seconds. Avg %f fps" % (frames, elapsed, frames/elapsed)


if __name__ == "__main__":
    (options, args) = parser.parse_args()
    if options.profile:
        import cProfile
        cProfile.run("main(options)")
    else:
        main(options)
