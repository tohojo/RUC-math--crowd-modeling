# vim:fileencoding=utf8


from drawing import Canvas
from Actor import Actor
from Wall import Wall
from Vector import Vector, Point

import sys

def main():
    canvas = Canvas()

    if len(sys.argv) > 1 and sys.argv[1] == "trace":
        clear = False
    else:
        clear = True

    actors = [
            Actor(
                position = Point(-8.0, -8.0),
                velocity = Vector(0.0, 0.5),
                target = Point(5.0, 5.0))
            ]
    walls = [
            Wall(-10, -10, 10, -10),
            Wall(-10, -10, -10, 10),
            Wall(-10, 10, 10, 10),
            Wall(10, -10, 10, 10),
#            Wall(-20, -20, 20, -20),
#            Wall(-20, -20, -20, 20),
#            Wall(-20, 20, 20, 20),
#            Wall(20, -20, 20, 20),
            ]

    timestep = 0.1 # for now
    canvas.clear_screen()

    while canvas.tick():
        
        if clear:
            canvas.clear_screen()

        for w in walls:
            canvas.draw_wall(w)

        for a in actors:
            a.calculate_acceleration(walls, actors)

        for a in actors:
            a.update_position(timestep)
            if a.has_escaped():
                actors.remove(a)
                continue

            canvas.draw_actor(a)
            for w in walls:
                P = w.projection(a.position)
                canvas.draw_proj(P)
        
        canvas.update()


if __name__ == "__main__":
    main()
