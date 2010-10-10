# vim:fileencoding=utf8


from drawing import Canvas
from Actor import Actor
from Wall import Wall
from Vector import Vector

def main():
    canvas = Canvas()

    actors = [
            Actor(0.0, 10.0, 2.5),
            Actor(-20.0, 40.0, 4.0, Vector(0.6, -0.6)),
            Actor(-20.0, -40.0, 4.0),
            ]
    walls = [
            Wall(-50, -50, 50, -50),
            Wall(-50, -50, -50, 50),
            Wall(-50, 50, 50, 50),
            Wall(50, -50, 50, 50),
#            Wall(-20, -20, 20, -20),
#            Wall(-20, -20, -20, 20),
#            Wall(-20, 20, 20, 20),
#            Wall(20, -20, 20, 20),
            ]

    while canvas.tick():
        
        canvas.clear_screen()

        for w in walls:
            canvas.draw_wall(w)

        for a in actors:
            if a.has_escaped():
                actors.remove(a)
            a.update_move_vector(walls, actors)
            a.update_pos()
            canvas.draw_actor(a)
            for w in walls:
                P = w.projection(a)
                canvas.draw_proj(P)
        
        canvas.update()


if __name__ == "__main__":
    main()
