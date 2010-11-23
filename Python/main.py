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

def main():
    canvas = Canvas()

    if len(sys.argv) > 1 and sys.argv[1] == "trace":
        clear = False
    else:
        clear = True

    actors = setup.generate_actors()
#    [
#            Actor(
#                position = Point(-8.0, 8.0),
#                velocity = Vector(-2.5, 0.0),
#                target = Point(0.0, 0.0)),
#            Actor(
#                position = Point(8.0, 8.0),
#                velocity = Vector(-2.5, 0),
#                target = Point(0.0, 0.0)),
#            Actor(
#                position = Point(-8.0, -8.0),
#                velocity = Vector(-2.5, 0.0),
#                target = Point(0.0, 0.0)),
#            Actor(
#                position = Point(8.0, -8.0),
#                velocity = Vector(-2.5, 0),
#                target = Point(0.0, 0.0)),
#            ]
    walls = [Wall(*i) for i in pm.walls]

    if pm.use_c_ext:
        optimised.add_actors(actors)

    timestep = pm.timestep
    timer = 0.0
    time_start = time()
    frames = 0
    canvas.clear_screen()

    while canvas.tick():
        
        if clear:
            canvas.clear_screen()

        canvas.draw_text("t = %.2f" % timer)

        canvas.draw_target(pm.actor.target)

#        if actors[0].time > 10:
#            return

        for w in walls:
            canvas.draw_wall(w)

        if pm.use_c_ext:
            optimised.update_actors()
            canvas.draw_actors()
        else:
            for a in actors:
                a.calculate_acceleration(walls, actors)

            for a in actors:
                a.update_position(timestep)
                #if a.has_escaped():
                    #actors.remove(a)
                    #continue

                canvas.draw_actor(a)
#            for w in walls:
#                P = w.projection(a.position)
#                canvas.draw_proj(P)
        
        canvas.update()
        timer += timestep
        frames += 1

        if pm.stop_at is not None and timer >= pm.stop_at:
            break

    elapsed = time() - time_start
    print "%d frames in %f seconds. Avg %f fps" % (frames, elapsed, frames/elapsed)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "profile":
        import cProfile
        cProfile.run("main()")
    else:
        main()
